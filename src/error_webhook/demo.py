import logging
import os

from dotenv import load_dotenv

from .handler import DiscordWebhookHandler


def main() -> int:
    load_dotenv()
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "")
    if not webhook_url or webhook_url.endswith("replace-me"):
        print("Set DISCORD_WEBHOOK_URL in .env before running the demo.")
        return 2
    logger = logging.getLogger("demo-service")
    logger.setLevel(os.getenv("LOG_LEVEL", "ERROR").upper())
    handler = DiscordWebhookHandler(webhook_url)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.error("Example error notification from the local demo.")
    print("Demo error sent to the configured Discord webhook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
