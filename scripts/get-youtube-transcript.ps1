param(
    [string]$Url = "https://www.youtube.com/watch?v=_U0UQsah3Pc",
    [string]$Output = "research/youtube-transcripts",
    [string]$Lang = "en",
    [ValidateSet("native", "auto", "generate")]
    [string]$Mode = "auto",
    [double]$PollIntervalSeconds = 1,
    [int]$MaxPolls = 180
)

$ErrorActionPreference = "Stop"

if (-not $env:SUPADATA_API_KEY) {
    throw "Set SUPADATA_API_KEY before running this script."
}

Add-Type -AssemblyName System.Net.Http

$headers = @{
    "x-api-key" = $env:SUPADATA_API_KEY
    "Accept" = "application/json"
}

$httpClient = [System.Net.Http.HttpClient]::new()
$httpClient.DefaultRequestHeaders.Add("x-api-key", $env:SUPADATA_API_KEY)
$httpClient.DefaultRequestHeaders.Accept.ParseAdd("application/json")

function Invoke-SupadataJson {
    param([string]$RequestUrl)

    $httpResponse = $httpClient.GetAsync($RequestUrl).GetAwaiter().GetResult()
    $body = $httpResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult()

    if (-not $httpResponse.IsSuccessStatusCode) {
        throw "Supadata returned HTTP $([int]$httpResponse.StatusCode): $body"
    }

    return @{
        StatusCode = [int]$httpResponse.StatusCode
        Payload = $body | ConvertFrom-Json
    }
}

$query = @{
    url = $Url
    lang = $Lang
    text = "true"
    mode = $Mode
}

$queryString = ($query.GetEnumerator() | ForEach-Object {
    "{0}={1}" -f [uri]::EscapeDataString($_.Key), [uri]::EscapeDataString($_.Value)
}) -join "&"

$apiBase = "https://api.supadata.ai/v1/transcript"
$response = Invoke-SupadataJson -RequestUrl "$apiBase`?$queryString"
$payload = $response.Payload

if ($response.StatusCode -eq 202) {
    if (-not $payload.jobId) {
        throw "Supadata returned HTTP 202 without a jobId."
    }

    $jobUrl = "$apiBase/$($payload.jobId)"

    for ($i = 0; $i -lt $MaxPolls; $i++) {
        Start-Sleep -Seconds $PollIntervalSeconds
        $jobResponse = (Invoke-SupadataJson -RequestUrl $jobUrl).Payload

        if ($jobResponse.status -eq "completed") {
            $payload = $jobResponse
            break
        }

        if ($jobResponse.status -eq "failed") {
            throw "Supadata transcript job failed: $($jobResponse.error)"
        }

        if ($i -eq ($MaxPolls - 1)) {
            throw "Supadata transcript job did not finish after $MaxPolls polls."
        }
    }
}

if ($payload.content -is [string]) {
    $transcript = $payload.content.Trim()
} elseif ($payload.content) {
    $transcript = ($payload.content | ForEach-Object { $_.text.Trim() }) -join [Environment]::NewLine
} else {
    throw "Supadata response did not include transcript content."
}

$outputPath = Join-Path (Get-Location) $Output
$outputDirectory = Split-Path -Parent $outputPath
if ($outputDirectory) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}

Set-Content -Path $outputPath -Value $transcript -Encoding UTF8

Write-Host "Saved transcript to $Output"
if ($payload.lang) {
    Write-Host "Transcript language: $($payload.lang)"
}
if ($payload.availableLangs) {
    Write-Host "Available languages: $($payload.availableLangs -join ', ')"
}
