#!/usr/bin/env python3
"""Fetch a YouTube transcript with Supadata and save it to a local file."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.supadata.ai/v1/transcript"
DEFAULT_VIDEO_URL = "https://www.youtube.com/watch?v=_U0UQsah3Pc"
DEFAULT_OUTPUT = Path("research/youtube-transcripts")


def request_json(url: str, api_key: str) -> tuple[int, dict[str, Any]]:
    request = Request(url, headers={"x-api-key": api_key, "Accept": "application/json"})

    try:
        with urlopen(request, timeout=90) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"error": body}
        raise RuntimeError(f"Supadata returned HTTP {error.code}: {payload}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach Supadata: {error}") from error


def fetch_transcript(
    video_url: str,
    api_key: str,
    lang: str,
    mode: str,
    poll_interval: float,
    max_polls: int,
) -> dict[str, Any]:
    params = urlencode({"url": video_url, "lang": lang, "text": "true", "mode": mode})
    status, payload = request_json(f"{API_BASE}?{params}", api_key)

    if status == 200:
        return payload

    if status != 202 or "jobId" not in payload:
        raise RuntimeError(f"Unexpected Supadata response HTTP {status}: {payload}")

    job_id = payload["jobId"]
    job_url = f"{API_BASE}/{job_id}"

    for _ in range(max_polls):
        time.sleep(poll_interval)
        _, job_payload = request_json(job_url, api_key)
        job_status = job_payload.get("status")

        if job_status == "completed":
            return job_payload
        if job_status == "failed":
            raise RuntimeError(f"Supadata transcript job failed: {job_payload.get('error')}")

    raise TimeoutError(f"Supadata transcript job did not finish after {max_polls} polls")


def normalize_content(payload: dict[str, Any]) -> str:
    content = payload.get("content")

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        lines = []
        for item in content:
            if isinstance(item, dict) and item.get("text"):
                lines.append(str(item["text"]).strip())
        return "\n".join(line for line in lines if line)

    raise RuntimeError(f"Supadata response did not include transcript content: {payload}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_VIDEO_URL, help="YouTube video URL")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output file path")
    parser.add_argument("--lang", default="en", help="Preferred transcript language")
    parser.add_argument(
        "--mode",
        choices=("native", "auto", "generate"),
        default="auto",
        help="Supadata transcript mode",
    )
    parser.add_argument("--poll-interval", type=float, default=1.0, help="Seconds between job polls")
    parser.add_argument("--max-polls", type=int, default=180, help="Maximum async job polls")
    args = parser.parse_args()

    api_key = os.environ.get("SUPADATA_API_KEY")
    if not api_key:
        print("Set SUPADATA_API_KEY before running this script.", file=sys.stderr)
        return 2

    payload = fetch_transcript(
        video_url=args.url,
        api_key=api_key,
        lang=args.lang,
        mode=args.mode,
        poll_interval=args.poll_interval,
        max_polls=args.max_polls,
    )
    transcript = normalize_content(payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(transcript + "\n", encoding="utf-8")

    print(f"Saved transcript to {args.output}")
    if payload.get("lang"):
        print(f"Transcript language: {payload['lang']}")
    if payload.get("availableLangs"):
        print(f"Available languages: {', '.join(payload['availableLangs'])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
