import logging
import pytest

from error_webhook.handler import DiscordWebhookHandler


def test_rejects_non_discord_webhook_url():
    with pytest.raises(ValueError):
        DiscordWebhookHandler("https://example.com/webhook")


def test_handler_only_accepts_error_or_higher():
    handler = DiscordWebhookHandler("https://discord.com/api/webhooks/123/token")
    assert handler.level == logging.ERROR
    handler.close()
