"""Ace Data Cloud's Chat Completions provider for Hermes Agent."""

from providers import register_provider
from providers.base import ProviderProfile


class AceDataCloudProfile(ProviderProfile):
    """Offer only models verified for this plugin's agent transport."""

    def fetch_models(self, *, api_key=None, base_url=None, timeout=8.0):
        models = super().fetch_models(
            api_key=api_key, base_url=base_url, timeout=timeout
        )
        if models is None:
            return None
        # The shared catalog also includes image and Messages-only models.
        return [model for model in models if model in self.fallback_models]


register_provider(
    AceDataCloudProfile(
        name="acedatacloud",
        display_name="Ace Data Cloud",
        description="Ace Data Cloud — GPT models with streaming and tool calling",
        signup_url="https://platform.acedata.cloud/console/applications",
        env_vars=("ACEDATACLOUD_API_KEY",),
        base_url="https://api.acedata.cloud/openai",
        api_mode="chat_completions",
        auth_type="api_key",
        fallback_models=("gpt-4.1-mini", "gpt-4.1"),
        model_capabilities={
            "gpt-4.1-mini": {"supports_tools": True, "supports_reasoning": False},
            "gpt-4.1": {"supports_tools": True, "supports_reasoning": False},
        },
    )
)
