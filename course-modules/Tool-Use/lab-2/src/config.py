"""Configuration for the email-assistant lab.

The email server's base URL is read by ``email_tools`` from the
``M3_EMAIL_SERVER_API_URL`` environment variable (set it in .env), e.g.
``http://127.0.0.1:8000``.
"""

MODEL = "openai:gpt-4.1"

USER_EMAIL = "you@email.com"
