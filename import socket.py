import socket
import requests
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc or parsed_url.path
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"Error resolving domain to IP: {e}")
        return None

def get_geo_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            return {
                "IP": ip,
                "City": data.get("city"),
                "Region": data.get("region"),
                "Country": data.get("country"),
                "Location": data.get("loc"),
                "ISP": data.get("org")
            }
        else:
            print(f"Failed to fetch geo info: {response.status_code}")
            return None
    except Exception as e:
        print(f"Geo info error: {e}")
        return None

def trace_link(url):
    print(f"Tracing: {url}")
    domain = extract_domain(url)
    if not domain:
        print("Invalid URL")
        return

    ip = get_ip(domain)
    if not ip:
        print("Could not resolve IP")
        return

    geo_info = get_geo_info(ip)
    if geo_info:
        print("\n--- Geo-location Info ---")
        for key, value in geo_info.items():
            print(f"{key}: {value}")
    else:
        print("Geo-location data not available")

# Example usage
if __name__ == "__main__":
    link = input("Enter a URL to trace: ")
    trace_link(link)
