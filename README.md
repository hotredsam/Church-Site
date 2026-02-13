# Kaleo Website Bot & Content Archive

This repository contains a collection of tools and scripts used to crawl, process, and archive content from the legacy Kaleo Church website. It also includes a Next.js based web interface for viewing processed content.

## Features

- **Web Crawler**: Python-based crawler to extract content and identify broken links.
- **Content Processor**: Scripts to clean up frontmatter and fix titles in migrated markdown files.
- **Sitemap Generator**: Tool to generate updated sitemaps for the new site structure.
- **Next.js Web Viewer**: A simple web application located in `kaleo-web/` to browse processed church content.
- **Migration Map**: A comprehensive JSON map tracking legacy-to-new URL transitions.

## Prerequisites

- **Python 3.10+**: For running the crawling and processing scripts.
- **Node.js 18+**: For running the `kaleo-web` application.
- **npm**: For dependency management.

## Quick Start

### Tools and Scripts
1. Navigate to the root directory.
2. Install Python dependencies (if any, check `crawler.py` imports).
3. Run the crawler:
   ```bash
   python crawler.py
   ```

### Web Viewer (kaleo-web)
1. Navigate to the `kaleo-web/` directory:
   ```bash
   cd kaleo-web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Build for Production (kaleo-web)

To build the web viewer for production:
```bash
cd kaleo-web
npm run build
```

## Repository Structure

- `crawler.py`: Legacy site crawler.
- `process_content.py`: Markdown cleaning script.
- `migration_map.json`: URL mapping data.
- `kaleo-web/`: Next.js frontend application.
- `processed_content/`: Output directory for cleaned markdown files.
- `site_archive/`: Raw archived data from the legacy site.
