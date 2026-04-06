from types import SimpleNamespace

import pytest

from app.services import provider as provider_module
from app.services.provider import OpenAIContractProvider, ProviderConfigurationError


class _DummyResponses:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def create(self, *, model: str, input: str) -> SimpleNamespace:
        self.calls.append({"model": model, "input": input})
        return SimpleNamespace(output_text='{"ok": true}')


class _DummyOpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.responses = _DummyResponses()


def test_provider_uses_configured_openai_model(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_client: _DummyOpenAIClient | None = None

    def fake_openai(*, api_key: str) -> _DummyOpenAIClient:
        nonlocal captured_client
        captured_client = _DummyOpenAIClient(api_key=api_key)
        return captured_client

    monkeypatch.setattr(provider_module, "OpenAI", fake_openai)
    monkeypatch.setattr(
        provider_module,
        "settings",
        SimpleNamespace(
            MODEL_PROVIDER="openai",
            OPENAI_API_KEY="test-key",
            OPENAI_MODEL="gpt-4.1-mini",
        ),
    )

    provider = OpenAIContractProvider()
    result = provider._call_model(prompt="hello")

    assert result == '{"ok": true}'
    assert captured_client is not None
    assert captured_client.api_key == "test-key"
    assert captured_client.responses.calls == [
        {"model": "gpt-4.1-mini", "input": "hello"}
    ]


def test_provider_requires_openai_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        provider_module,
        "settings",
        SimpleNamespace(
            MODEL_PROVIDER="openai",
            OPENAI_API_KEY="test-key",
            OPENAI_MODEL="   ",
        ),
    )

    with pytest.raises(ProviderConfigurationError, match="OPENAI_MODEL is required"):
        OpenAIContractProvider()
