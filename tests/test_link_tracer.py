"""Unit tests for LinkTracer — mocks socket and requests."""
import pytest
from unittest.mock import MagicMock, patch

from core.link_tracer import LinkTracer


@pytest.fixture
def tracer():
    return LinkTracer()


def test_extract_domain_full_url(tracer):
    assert tracer.extract_domain("https://www.google.com/search") == "google.com"


def test_extract_domain_no_www(tracer):
    assert tracer.extract_domain("https://github.com") == "github.com"


def test_extract_domain_invalid_returns_none(tracer):
    result = tracer.extract_domain("")
    assert result is None or result == ""


@patch("core.link_tracer.socket.gethostbyname", return_value="142.250.80.46")
def test_resolve_ip_success(mock_dns, tracer):
    assert tracer.resolve_ip("google.com") == "142.250.80.46"


@patch("core.link_tracer.socket.gethostbyname", side_effect=Exception("DNS fail"))
def test_resolve_ip_failure_returns_none(mock_dns, tracer):
    assert tracer.resolve_ip("invalid.invalid") is None


@patch("core.link_tracer.requests.get")
def test_get_geo_info_success(mock_get, tracer):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "city": "Mountain View", "region": "California",
        "country": "US", "loc": "37.4056,-122.0775", "org": "AS15169 Google LLC"
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response
    result = tracer.get_geo_info("142.250.80.46")
    assert result["city"] == "Mountain View"
    assert result["country"] == "US"


@patch("core.link_tracer.requests.get", side_effect=Exception("timeout"))
def test_get_geo_info_failure_returns_none(mock_get, tracer):
    assert tracer.get_geo_info("0.0.0.0") is None
