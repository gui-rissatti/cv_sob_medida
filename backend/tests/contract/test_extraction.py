"""Contract tests for the extraction endpoint specification."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

SPEC_PATH = (
    Path(__file__).resolve().parents[3]
    / "contracts"
    / "extraction-api.yaml"
)


@pytest.fixture(scope="module")
def extraction_spec() -> dict:
    """Load the OpenAPI document once per test module."""
    if not SPEC_PATH.exists():  # pragma: no cover - defensive guard
        raise FileNotFoundError(f"Spec not found at {SPEC_PATH}")
    with SPEC_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_path_and_method_defined(extraction_spec: dict) -> None:
    paths = extraction_spec.get("paths", {})
    assert "/extract-job-details" in paths, "Endpoint path missing"
    assert "post" in paths["/extract-job-details"], "POST method missing"


def test_request_body_requires_url(extraction_spec: dict) -> None:
    request_body = (
        extraction_spec["paths"]["/extract-job-details"]["post"]["requestBody"]
    )
    schema = request_body["content"]["application/json"]["schema"]
    assert "url" in schema.get("required", []), "url must be required"
    url_field = schema["properties"]["url"]
    assert url_field["type"] == "string"
    assert url_field["format"] == "uri"


def test_job_schema_has_expected_fields(extraction_spec: dict) -> None:
    job_schema = extraction_spec["components"]["schemas"]["Job"]
    expected_fields = {
        "id",
        "url",
        "title",
        "company",
        "description",
        "skills",
        "createdAt",
    }
    assert expected_fields.issubset(job_schema.get("required", []))
    assert job_schema["properties"]["skills"]["type"] == "array"
    skills_items = job_schema["properties"]["skills"]["items"]
    assert skills_items["type"] == "string"


def test_error_responses_reference_common_schema(extraction_spec: dict) -> None:
    responses = extraction_spec["paths"]["/extract-job-details"]["post"]["responses"]
    error_ref = "#/components/schemas/ErrorResponse"
    for status in ("400", "422", "500"):
        schema = responses[status]["content"]["application/json"]["schema"]
        assert schema.get("$ref") == error_ref