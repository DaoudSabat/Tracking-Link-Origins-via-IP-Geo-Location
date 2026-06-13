# 🌐 Link Origin Tracker

CLI tool that resolves any URL to the physical location of its origin server using IP and geo-location APIs.

## Overview

Given a URL, the tool extracts the domain name, performs a DNS lookup to find the server's IP address, then queries the ipinfo.io API to retrieve geographic metadata — city, region, country, coordinates, and ISP. The result is a full trace chain: URL → domain → IP → geo-location, useful for verifying CDN origins, detecting redirects, or investigating suspicious links.

## Architecture

```
Tracking-Link-Origins/
├── core/
│   └── link_tracer.py    # LinkTracer — URL → domain → IP → geo-location chain
├── utils/                # Reserved for future helpers
├── tests/
│   └── test_link_tracer.py  # pytest unit tests (network fully mocked)
├── main.py               # CLI entry point
└── requirements.txt
```

## Design Patterns

- **Chain of Responsibility** — `trace()` calls `extract_domain()` → `resolve_ip()` → `get_geo_info()` in sequence; each step validates its output before passing to the next, short-circuiting on failure
- **Facade** — `LinkTracer.trace()` unifies three separate I/O concerns (URL parsing, DNS, HTTP API) behind a single public method

## Tech Stack

- **Python 3.10+**
- **socket** — standard library DNS resolution
- **requests** — ipinfo.io geo-location API calls
- **pytest** — unit testing

## Installation

```bash
git clone https://github.com/DaoudSabat/Tracking-Link-Origins-via-IP-Geo-Location.git
cd Tracking-Link-Origins-via-IP-Geo-Location
pip install -r requirements.txt
```

## Usage

```bash
python main.py
# Enter a URL to trace: https://github.com

--- Trace Result ---
Url: https://github.com
Domain: github.com
Ip: 140.82.121.4
City: San Francisco
Region: California
Country: US
Location: 37.7697,-122.3933
Isp: AS36459 GitHub, Inc.
```

## Tests

```bash
pytest tests/ -v
```

All network calls are mocked — no internet connection required.

## License

MIT
