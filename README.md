# Error Webhook Dispatcher

Forward Python `ERROR` and `CRITICAL` log records to a Discord webhook using a standard-library `logging.Handler`. The handler is opt-in, has bounded network timeouts and retries, and truncates messages to Discord's content limit.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
copy .env.example .env  # Windows PowerShell: Copy-Item .env.example .env
# Add a Discord webhook URL to .env, then run:
error-webhook-demo
```

Keep `.env` private. Never commit an actual webhook URL: anyone who gets it can post to that Discord channel. The demo only sends its own generated warning/error lines.

## Learning notes

`logging.Handler.emit` is the extension point that makes a custom destination behave like a normal logger. The handler owns its `requests.Session`, sends a timeout on every call, and uses bounded retry delays for rate limiting and transient server failures.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
