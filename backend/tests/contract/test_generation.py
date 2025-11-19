"""Contract tests for the generation endpoint specification."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

SPEC_PATH = (
    Path(__file__).resolve().parents[3]
    / "contracts"
    / "generation-api.yaml"
)


@pytest.fixture(scope="module")
def generation_spec() -> dict:
    """Load the OpenAPI document once per test module."""
    if not SPEC_PATH.exists():
        raise FileNotFoundError(f"Spec not found at {SPEC_PATH}")
    with SPEC_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_path_and_method_defined(generation_spec: dict) -> None:
    paths = generation_spec.get("paths", {})
    assert "/generate-materials" in paths, "Endpoint path missing"
    assert "post" in paths["/generate-materials"], "POST method missing"


def test_request_body_requires_job_and_profile(generation_spec: dict) -> None:
    request_body = (
        generation_spec["paths"]["/generate-materials"]["post"]["requestBody"]
    )
    schema = request_body["content"]["application/json"]["schema"]
    # The schema is a ref, so we need to resolve it or check the ref name
    assert "$ref" in schema
    ref_name = schema["$ref"].split("/")[-1]
    
    component_schema = generation_spec["components"]["schemas"][ref_name]
    assert "job" in component_schema["required"]
    assert "profile" in component_schema["required"]


def test_generated_assets_schema_has_expected_fields(generation_spec: dict) -> None:
    assets_schema = generation_spec["components"]["schemas"]["GeneratedAssets"]
    expected_fields = {
        "cv",
        "coverLetter",
        "networking",
        "insights",
        "matchScore",
        "generatedAt",
    }
    assert expected_fields.issubset(assets_schema.get("required", []))
    
    assert assets_schema["properties"]["matchScore"]["type"] == "integer"
    assert assets_schema["properties"]["matchScore"]["minimum"] == 0
    assert assets_schema["properties"]["matchScore"]["maximum"] == 100


def test_error_responses_reference_common_schema(generation_spec: dict) -> None:
    responses = generation_spec["paths"]["/generate-materials"]["post"]["responses"]
    error_ref = "#/components/schemas/ErrorResponse"
    for status in ("400", "422", "500"):
        schema = responses[status]["content"]["application/json"]["schema"]
        assert schema.get("$ref") == error_ref
