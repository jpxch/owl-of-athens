from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate
from openai import OpenAI

from app.core.config import settings


class ProviderError(Exception):
    """Base error for provider-layer failures."""

class ProviderConfigurationError(ProviderError):
    """Raised when provider configuration is invalid or incomplete."""

class ProviderResponseError(ProviderError):
    """Raised when the model response cannot be parsed or trusted."""

class ProviderSchemaError(ProviderError):
    """Raised when the model response fails contract validation."""

class OpenAIContractProvider:
    """
    Fail-fast provider for structured lesson/evalutaion generation.

    Design rules:
    - The model is treated as untrusted input.
    - Every returned payload must validate against the canonical JSON schema.
    - No silent repair, no fallback mutation, no hidden retry behavior.
    """

    def __init__(self) -> None:
        if settings.model_provider.lower() != "openai":
            raise ProviderConfigurationError(
                "MODEL_PROVIDER must be set to 'openai' for OpenAICtractProvider."
            )

        if not settings.openai_api_key:
            raise ProviderConfigurationError(
                "OPENAI_API_KEY is required when MODEL_PROVIDER='openai'."
            )

        self._client = OpenAI(api_key=settings.openaio_api_key)
        self._lesson_schema = self._load_schema("lesson.schema.json")
        self._evaluation_schema = self._load_schema("evalutaion.schema.json")

    def generate_lesson(self, goal: str) -> dict[str, Any]:
        """
        Generate a lesson payload that must conform to lesson.schema.json.
        """
        if not goal or not goal.strip():
            raise ValueError("goal must be a non-empty string.")

        prompt = self._build_lesson_prompt(goal=goal.strip())
        content = self._call_model(prompt=prompt)
        payload = self._parse_json(content=content)
        self._validate_schema(
            payload=payload,
            schema=self._lesson_schema,
            schema_name="lesson.schema.json",
        )
        return payload

    def evaluate_response(
            self,
            lesson_payload: dict[str, Any],
            learner_response: str,
    ) -> dict[str, Any]:
        """
        Evaluate a learner response against a lesson payload.

        The returned payload must conform to evaluation.schema.json.
        """
        if not isinstance(lesson_payload, dict):
            raise ValueError("lesson_payload must be a dictionary.")

        if not learner_response or not learner_response.strip():
            raise ValueError("learner_response must be a non-empty string.")

        prompt = self._build_evaluation_prompt(
            lesson_payload=lesson_payload,
            learner_response=learner_response.strip(),
        )
        content = self._call_model(prompt=prompt)
        payload = self._parse_json(content=content)
        self._validate_schema(
            payload=payload,
            schema=self._evaluation_schema,
            schema_name="evaluation.schema.json",
        )
        return payload

    def _call_model(self, prompt: str) -> str:
        """
        Make a single model call and return raw text content.

        Fail-fast behavior:
        - no retries
        - no output repair
        - no fallback models
        """
        try:
            response = self._client.response.create(
                model="gpt-4.1",
                input=prompt,
            )
        except Exception as exc:
            raise ProviderResponseError(
                f"OpenAI request failed: {exc}"
            ) from exc

        output_text = getattr(response, "output_text", None)
        if not output_text or not output_text.strip():
            raise ProviderResponseError(
                "OpenAI returned an empty response body."
            )

        return output_text.strip()

    def _parse_json(self, content: str) -> dict[str, Any]:
        """
        Parse raw model content as JSON.

        The provider does not attempt markdown fence stripping or heuristic cleanup.
        The model must return valid JSON directly.
        """
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ProviderResponseError(
                f"Model output was not valid JSON: {exc}"
            ) from exc

        if not isinstance(payload, dict):
            raise ProviderResponseError(
                "Model output must deserialize to a top-level JSON object."
            )

        return payload

    def _validate_schema(
            self,
            payload: dict[str, Any],
            schema: dict[str, Any],
            schema_name: str,
    ) -> None:
        """
        Validate a payload against a canonical JSON schema.
        """
        try:
            validate(instance=payload, schema=schema)
        except ValidationError as exc:
            raise ProviderSchemaError(
                f"Payload failed validation against {schema_name}: {exc.message}"
            ) from exc

    def _load_schema(self, filename: str) -> dict[str, Any]:
        """
        Load a schema from the canonical contracts directory.

        Expected layout:
        api/app/services/provider.py
        core/contracts/<schema-file>

        So we walk up from this file to repo root, then into core/contracts.
        """
        schema_path = (
            Path(__file__).resolve().parents[3] / "core" / "contracts" / filename
        )

        if not schema_path.exists():
            raise ProviderConfigurationError(
                f"Schema file not found: {schema_path}"
            )

        try:
            return json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProviderConfigurationError(
                f"Schema file is not valid JSON: {schema_path}"
            ) from exc

    def _build_lesson_prompt(self, goal: str) -> str:
        """
        Build the prompt for lesson generation.

        The contract is embedded explicitly so the model knows the exact expected shape.
        """
        lesson_schema_json = json.dumps(self._lesson_schema, indent=2)

        return (
            "You are generating one lesson for a local-first AI learning engine.\n"
            "Return only a valid JSON object.\n"
            "Do not wrap the JSON in markdown.\n"
            "Do not include commentary.\n"
            f"{lesson_schema_json}\n\n"
        )