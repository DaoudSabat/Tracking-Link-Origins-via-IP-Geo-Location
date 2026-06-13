"""Resolves a URL to its origin server's geographic location."""
from __future__ import annotations

import socket
from urllib.parse import urlparse

import requests


class LinkTracer:
    """Traces a URL to its IP address and geographic location.

    Uses the free ipinfo.io API — no key required for basic usage.
    """

    GEO_API_URL = "https://ipinfo.io/{ip}/json"
    REQUEST_TIMEOUT = 5

    def trace(self, url: str) -> dict | None:
        """Full trace: URL → domain → IP → geo-location dict.

        Returns a dict with keys: url, domain, ip, city, region,
        country, location, isp — or None if resolution fails.
        """
        domain = self.extract_domain(url)
        if not domain:
            return None
        ip = self.resolve_ip(domain)
        if not ip:
            return None
        geo = self.get_geo_info(ip)
        if not geo:
            return None
        return {"url": url, "domain": domain, **geo}

    @staticmethod
    def extract_domain(url: str) -> str | None:
        """Extract the bare domain name from a URL."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            return domain.removeprefix("www.")
        except Exception as e:
            print(f"URL parse error: {e}")
            return None

    @staticmethod
    def resolve_ip(domain: str) -> str | None:
        """Resolve a domain name to its IPv4 address."""
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror as e:
            print(f"DNS resolution failed for {domain}: {e}")
            return None

    def get_geo_info(self, ip: str) -> dict | None:
        """Fetch geographic metadata for an IP from ipinfo.io."""
        try:
            response = requests.get(
                self.GEO_API_URL.format(ip=ip),
                timeout=self.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "ip": ip,
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "location": data.get("loc"),
                "isp": data.get("org"),
            }
        except requests.RequestException as e:
            print(f"Geo lookup failed: {e}")
            return None
