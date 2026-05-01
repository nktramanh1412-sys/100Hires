# 100Hires
# 100Hires Portfolio Project - Initial Setup

## 1. Tools Installed
- **Cursor IDE**: The primary AI-powered code editor used for this environment setup.
- **Claude Code (for VS Code)**: Integrated as an extension for advanced AI assistance (verified via high download count of 16M+).
- **Codex (OpenAI’s coding agent)**: Added for intelligent code suggestions and task automation (verified via 4.7M+ downloads).
- **Git & GitHub**: Configured for version control and remote repository management.

## 2. Steps Completed
1. Downloaded and installed the **Cursor IDE**.
2. Searched and added **Claude Code** and **Codex** extensions from the marketplace.
3. Created a public repository on **GitHub** to host the project.
4. Installed **Git** on the local system to enable repository synchronization.
5. Connected the local project folder to GitHub and initialized the documentation process.

## 3. Issues and Solutions

- **Issue: Technical Onboarding (Extensions)**
  - *Challenge*: Initially unfamiliar with the process of adding and managing extensions within a new IDE.
  - *Solution*: Performed a targeted search on YouTube for "how to install Cursor extensions." Following a video tutorial allowed me to successfully locate the Marketplace and install the correct tools.

- **Issue: Repository Connection & Git Requirements**
  - *Challenge*: The `Git: Clone` command was missing from the Command Palette, and I was looking for a more "convenient" way to sync without complex installations.
  - *Solution*: Consulted **Gemini AI** to explore alternative methods. Through the discussion, I realized that installing Git is a fundamental requirement for professional version control. I proceeded to download and install Git, which successfully enabled the synchronization features.

- **Issue: Extension Authentication (Paywall)**
  - *Challenge*: Upon attempting to log in to Claude Code, I encountered a notification stating that a "Claude Max or Pro" subscription is required.
  - *Solution*: I documented this restriction as part of the research process. I focused on completing the technical setup and environment integration, ensuring the tools are properly installed and ready for use once access is granted.

---
*This README documents my ability to research, utilize AI tools for problem-solving, and adapt to new technical environments.*


# Phase 2: AI-Powered SEO Research Project

## 1. Project Overview
This project focuses on **AI-powered SEO content production for B2B SaaS**. The goal is to research and document high-signal strategies from industry practitioners to build a future-ready content playbook.

## 2. Technical Workflow & AI Integration
To ensure data accuracy and scalability, I utilized an automated workflow to collect and process research materials:

### **YouTube Transcript Extraction**
- **Tool:** Supadata API.
- **Process:** Extracted the raw transcript from [Koray Tuğberk GÜBÜR's Semantic SEO Revolution](https://www.youtube.com/watch?v=_U0UQsah3Pc).
- **AI Processing:** Fed the raw transcript into **Codex (within Cursor IDE)** to clean the data, remove promotional filler, and structure it into a readable Markdown format in `/research/youtube-transcripts/`.

### **LinkedIn Data Scraping**
- **Tool:** Apify (LinkedIn Profile Posts Scraper).
- **Process:** Scraped the 10 most recent posts from **Kevin Indig's** profile to capture real-time market insights and salary data.
- **Data Synthesis:** I extracted the raw **JSON** dataset from Apify and utilized **Codex** to architect a structured Markdown table, converting raw data into actionable insights located in `/research/linkedin-posts/`.

## 3. Expert Selection Rationale
I selected these 10 experts (documented in `sources.md`) based on their focus on **practical frameworks** rather than theoretical SEO. 

- **Kevin Indig:** Chosen for his data-driven insights into the "AI Premium" in the job market and AEO (Answer Engine Optimization).
- **Koray Tuğberk GÜBÜR:** Selected for his groundbreaking work in **Semantic SEO** and topical authority, which are critical for scaling B2B SaaS content without losing quality.

## 4. Repository Structure
- `/research/sources.md`: List of 10 experts with links and annotations.
- `/research/linkedin-posts/`: Scraped posts and tables (Kevin Indig).
- `/research/youtube-transcripts/`: Processed transcripts (Koray Tuğberk GÜBÜR).
