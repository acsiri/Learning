#!/usr/bin/env python3
"""
Email Filter Agent

Reads filter rules from a TXT file, searches emails via IMAP, and deletes matching messages.

Usage example:
    python email_filter_agent.py --imap-host imap.gmail.com --username you@gmail.com

Credentials can be passed with --password or environment variable EMAIL_AGENT_PASSWORD.
"""

from __future__ import annotations

import argparse
import email
import imaplib
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import List, Optional


@dataclass
class FilterRuleSet:
    from_contains: List[str] = field(default_factory=list)
    subject_contains: List[str] = field(default_factory=list)
    body_contains: List[str] = field(default_factory=list)
    from_regex: List[re.Pattern] = field(default_factory=list)
    subject_regex: List[re.Pattern] = field(default_factory=list)
    body_regex: List[re.Pattern] = field(default_factory=list)
    older_than_days: Optional[int] = None


def decode_mime_header(value: Optional[str]) -> str:
    if not value:
        return ""

    parts = decode_header(value)
    decoded = []
    for chunk, enc in parts:
        if isinstance(chunk, bytes):
            try:
                decoded.append(chunk.decode(enc or "utf-8", errors="replace"))
            except LookupError:
                decoded.append(chunk.decode("utf-8", errors="replace"))
        else:
            decoded.append(chunk)
    return "".join(decoded)


def parse_rules_file(path: str) -> FilterRuleSet:
    rules = FilterRuleSet()
    line_no = 0

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line_no += 1
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if ":" not in line:
                raise ValueError(f"Invalid rule format at line {line_no}: {line}")

            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if not value:
                continue

            if key == "from_contains":
                rules.from_contains.append(value.lower())
            elif key == "subject_contains":
                rules.subject_contains.append(value.lower())
            elif key == "body_contains":
                rules.body_contains.append(value.lower())
            elif key == "from_regex":
                rules.from_regex.append(re.compile(value, re.IGNORECASE))
            elif key == "subject_regex":
                rules.subject_regex.append(re.compile(value, re.IGNORECASE))
            elif key == "body_regex":
                rules.body_regex.append(re.compile(value, re.IGNORECASE))
            elif key == "older_than_days":
                try:
                    days = int(value)
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid integer for older_than_days at line {line_no}: {value}"
                    ) from exc
                if days < 0:
                    raise ValueError("older_than_days must be >= 0")
                rules.older_than_days = days
            else:
                raise ValueError(f"Unknown rule '{key}' at line {line_no}")

    return rules


def extract_text_body(msg: Message) -> str:
    if msg.is_multipart():
        body_chunks: List[str] = []
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            if content_type == "text/plain" and "attachment" not in disposition.lower():
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                try:
                    body_chunks.append(payload.decode(charset, errors="replace"))
                except LookupError:
                    body_chunks.append(payload.decode("utf-8", errors="replace"))
        return "\n".join(body_chunks)

    payload = msg.get_payload(decode=True) or b""
    charset = msg.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def is_older_than(msg_date_header: str, days: int) -> bool:
    if not msg_date_header:
        return False

    try:
        dt = parsedate_to_datetime(msg_date_header)
    except (TypeError, ValueError):
        return False

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    return dt < threshold


def matches_rules(msg: Message, rules: FilterRuleSet) -> bool:
    sender = decode_mime_header(msg.get("From", ""))
    subject = decode_mime_header(msg.get("Subject", ""))
    body = extract_text_body(msg)

    sender_l = sender.lower()
    subject_l = subject.lower()
    body_l = body.lower()

    if rules.older_than_days is not None:
        if is_older_than(msg.get("Date", ""), rules.older_than_days):
            return True

    if any(fragment in sender_l for fragment in rules.from_contains):
        return True
    if any(fragment in subject_l for fragment in rules.subject_contains):
        return True
    if any(fragment in body_l for fragment in rules.body_contains):
        return True

    if any(rx.search(sender) for rx in rules.from_regex):
        return True
    if any(rx.search(subject) for rx in rules.subject_regex):
        return True
    if any(rx.search(body) for rx in rules.body_regex):
        return True

    return False


def search_all_messages(client: imaplib.IMAP4_SSL) -> List[bytes]:
    status, data = client.search(None, "ALL")
    if status != "OK":
        return []

    ids = data[0].split() if data and data[0] else []
    return ids


def process_mailbox(
    host: str,
    username: str,
    password: str,
    rules_path: str,
    mailbox: str,
    dry_run: bool,
) -> int:
    rules = parse_rules_file(rules_path)

    deleted_count = 0
    with imaplib.IMAP4_SSL(host) as client:
        client.login(username, password)
        status, _ = client.select(mailbox)
        if status != "OK":
            raise RuntimeError(f"Unable to select mailbox '{mailbox}'")

        msg_ids = search_all_messages(client)
        print(f"Found {len(msg_ids)} emails in '{mailbox}'.")

        for msg_id in msg_ids:
            fetch_status, msg_data = client.fetch(msg_id, "(RFC822)")
            if fetch_status != "OK" or not msg_data or not msg_data[0]:
                continue

            raw_email = msg_data[0][1]
            if not raw_email:
                continue

            msg = email.message_from_bytes(raw_email)
            if matches_rules(msg, rules):
                subject = decode_mime_header(msg.get("Subject", "(no subject)"))
                sender = decode_mime_header(msg.get("From", "(unknown sender)"))

                if dry_run:
                    print(f"[DRY RUN] Would delete: From='{sender}' Subject='{subject}'")
                else:
                    client.store(msg_id, "+FLAGS", "\\Deleted")
                    print(f"Deleted: From='{sender}' Subject='{subject}'")
                deleted_count += 1

        if not dry_run and deleted_count > 0:
            client.expunge()

        client.logout()

    return deleted_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Filter and delete emails using rules from a TXT file."
    )
    parser.add_argument(
        "--imap-host",
        default=os.getenv("EMAIL_AGENT_IMAP_HOST", "imap.gmail.com"),
        help="IMAP host (default: imap.gmail.com or EMAIL_AGENT_IMAP_HOST)",
    )
    parser.add_argument(
        "--username",
        default=os.getenv("EMAIL_AGENT_USERNAME"),
        required=os.getenv("EMAIL_AGENT_USERNAME") is None,
        help="Email username/login (or set EMAIL_AGENT_USERNAME)",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("EMAIL_AGENT_PASSWORD"),
        required=os.getenv("EMAIL_AGENT_PASSWORD") is None,
        help="Email password/app password (or set EMAIL_AGENT_PASSWORD)",
    )
    parser.add_argument(
        "--rules",
        default="email_filters.txt",
        help="Path to TXT rules file (default: email_filters.txt)",
    )
    parser.add_argument(
        "--mailbox",
        default="INBOX",
        help="Mailbox/folder to scan (default: INBOX)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview deletions without deleting anything",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not os.path.exists(args.rules):
        print(f"Rules file not found: {args.rules}")
        return 1

    try:
        deleted = process_mailbox(
            host=args.imap_host,
            username=args.username,
            password=args.password,
            rules_path=args.rules,
            mailbox=args.mailbox,
            dry_run=args.dry_run,
        )
    except imaplib.IMAP4.error as exc:
        print(f"IMAP error: {exc}")
        return 2
    except Exception as exc:  # Keep top-level failure handling user friendly.
        print(f"Error: {exc}")
        return 3

    action = "matched" if args.dry_run else "deleted"
    print(f"Done. Total emails {action}: {deleted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
