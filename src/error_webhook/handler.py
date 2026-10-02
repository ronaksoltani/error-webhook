from __future__ import annotations

import logging
import time

import requests

DISCORD_LIMIT = 2000


class DiscordWebhookHandler(logging.Handler):
    """Send error records with bounded timeouts and a small retry budget."""

    def __init__(self, webhook_url: str, timeout: float = 5.0, retries: int = 2):
        super().__init__(level=logging.ERROR)
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("webhook URL must be an official Discord HTTPS webhook URL")
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.retries = max(0, retries)
        self.session = requests.Session()

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        body = f"**{record.levelname} · {record.name}**\n```\n{message}\n```"
        body = body[:DISCORD_LIMIT]
        for attempt in range(self.retries + 1):
            try:
                response = self.session.post(self.webhook_url, json={"content": body}, timeout=self.timeout)
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt < self.retries:
                        delay = min(float(response.headers.get("Retry-After", 0.5 * (2 ** attempt))), 3.0)
                        time.sleep(max(delay, 0))
                        continue
                response.raise_for_status()
                return
            except requests.RequestException as error:
                if isinstance(error, requests.HTTPError) and error.response is not None:
                    if error.response.status_code < 500 and error.response.status_code != 429:
                        self.handleError(record)
                        return
                if attempt >= self.retries:
                    self.handleError(record)
                else:
                    time.sleep(min(0.25 * (2 ** attempt), 1.0))
