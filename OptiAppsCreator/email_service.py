#!/usr/bin/env python3
"""Email helpers for OptiAppsCreator authentication flows."""

from __future__ import annotations

import os
import smtplib
import socket
from email.message import EmailMessage
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False


SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")


def app_base_url() -> str:
    return os.getenv("APP_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def build_reset_link(token: str) -> str:
    return f"{app_base_url()}/ui/reset_password.html?token={token}"


def send_email(to_email: str, subject: str, body: str) -> None:
    host = os.getenv("SMTP_HOST", "")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    sender = os.getenv("SMTP_FROM", user)
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes", "on"}
    timeout = float(os.getenv("SMTP_TIMEOUT", "10"))

    if not host or not sender:
        print(f"[email disabled] To: {to_email}\nSubject: {subject}\n\n{body}")
        return

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(host, port, timeout=timeout) as smtp:
            if use_tls:
                smtp.starttls()
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg)
    except (OSError, smtplib.SMTPException, socket.timeout) as exc:
        print(f"[email error] Could not send email to {to_email}: {exc}")
        print(f"[email fallback] Subject: {subject}\n\n{body}")


def send_password_reset_email(to_email: str, token: str, first_login: bool = False) -> None:
    link = build_reset_link(token)
    if first_login:
        subject = "OptiHexx password update required"
        intro = "Your OptiHexx account requires a password update before you can access the system."
    else:
        subject = "OptiHexx password reset"
        intro = "A password reset was requested for your OptiHexx account."
    body = f"{intro}\n\nOpen this link to set a new password:\n{link}\n\nIf you did not request this, ignore this message."
    send_email(to_email, subject, body)
