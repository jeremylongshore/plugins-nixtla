#!/usr/bin/env python3
"""
Nixtla Inventory Emailer (Resend)

Send CSV inventory files with attachments via Resend API.

Usage:
    python send_inventory.py --to jeremy@intentsolutions.io
    python send_inventory.py --to jeremy@intentsolutions.io --subject "Custom Subject"
    python send_inventory.py --dry-run  # Preview without sending

Requirements:
    pip install resend python-dotenv

Setup:
    Create .env file in this directory:
    RESEND_API_KEY=re_xxxxxxxxxxxx

Created: 2025-12-12
"""

import argparse
import base64
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import resend
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Missing dependencies. Run:")
    print("  pip install resend python-dotenv")
    sys.exit(1)

# Load .env from this directory
EMAILER_DIR = Path(__file__).parent
load_dotenv(EMAILER_DIR / ".env")

# Configuration
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "jeremy@intentsolutions.io")

# Repo root (parent of emailer/)
REPO_ROOT = EMAILER_DIR.parent


def get_csv_files():
    """Get inventory CSV files from repo root."""
    plugins_csv = REPO_ROOT / "plugins_inventory.csv"
    skills_csv = REPO_ROOT / "skills_inventory.csv"

    files = []
    if plugins_csv.exists():
        files.append(plugins_csv)
    if skills_csv.exists():
        files.append(skills_csv)

    return files


def count_csv_rows(filepath):
    """Count data rows in CSV (excluding header)."""
    with open(filepath) as f:
        return sum(1 for _ in f) - 1


def create_attachments(csv_files):
    """Create Resend attachment objects from CSV files."""
    attachments = []
    for csv_file in csv_files:
        with open(csv_file, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        attachments.append({"filename": csv_file.name, "content": content, "type": "text/csv"})

    return attachments


def create_email_html(csv_files):
    """Create HTML email body."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows_html = ""
    for f in csv_files:
        row_count = count_csv_rows(f)
        rows_html += f"<li><strong>{f.name}</strong>: {row_count} items</li>\n"

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2563eb;">Nixtla Inventory Report</h2>
        <p>Generated: {timestamp}</p>

        <h3>Attached Files:</h3>
        <ul>
            {rows_html}
        </ul>

        <h3>CSV Columns:</h3>
        <table style="border-collapse: collapse; width: 100%; font-size: 14px;">
            <tr style="background: #f3f4f6;">
                <th style="border: 1px solid #d1d5db; padding: 8px; text-align: left;">Column</th>
                <th style="border: 1px solid #d1d5db; padding: 8px; text-align: left;">Description</th>
            </tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Name</td><td style="border: 1px solid #d1d5db; padding: 8px;">Plugin/skill identifier</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Who</td><td style="border: 1px solid #d1d5db; padding: 8px;">Target user persona</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">What</td><td style="border: 1px solid #d1d5db; padding: 8px;">Core functionality</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">When</td><td style="border: 1px solid #d1d5db; padding: 8px;">Use case triggers</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Where</td><td style="border: 1px solid #d1d5db; padding: 8px;">Implementation context</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Definition_of_Success_Technical</td><td style="border: 1px solid #d1d5db; padding: 8px;">Technical success criteria</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Definition_of_Success_Business</td><td style="border: 1px solid #d1d5db; padding: 8px;">Business success criteria</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Target_Goal</td><td style="border: 1px solid #d1d5db; padding: 8px;">Measurable target metrics</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Production</td><td style="border: 1px solid #d1d5db; padding: 8px;">true/false/partial status</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Category</td><td style="border: 1px solid #d1d5db; padding: 8px;">Functional category</td></tr>
            <tr><td style="border: 1px solid #d1d5db; padding: 8px;">Path</td><td style="border: 1px solid #d1d5db; padding: 8px;">Repository path</td></tr>
        </table>

        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
        <p style="color: #6b7280; font-size: 12px;">
            Sent from Nixtla Claude Plugins Repo
        </p>
    </body>
    </html>
    """


def create_email_text(csv_files):
    """Create plain text email body."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    files_text = ""
    for f in csv_files:
        row_count = count_csv_rows(f)
        files_text += f"  - {f.name}: {row_count} items\n"

    return f"""Nixtla Inventory Report
Generated: {timestamp}

Attached Files:
{files_text}
CSV Columns:
  - Name: Plugin/skill identifier
  - Who: Target user persona
  - What: Core functionality
  - When: Use case triggers
  - Where: Implementation context
  - Definition_of_Success_Technical: Technical success criteria
  - Definition_of_Success_Business: Business success criteria
  - Target_Goal: Measurable target metrics
  - Production: true/false/partial status
  - Category: Functional category
  - Path: Repository path

---
Sent from Nixtla Claude Plugins Repo
"""


def send_email(to_address, subject=None):
    """Send email with CSV attachments via Resend."""
    if not RESEND_API_KEY:
        print("ERROR: Missing RESEND_API_KEY")
        print("Create emailer/.env with:")
        print("  RESEND_API_KEY=re_xxxxxxxxxxxx")
        sys.exit(1)

    resend.api_key = RESEND_API_KEY

    csv_files = get_csv_files()
    if not csv_files:
        print("ERROR: No CSV files found in repo root")
        sys.exit(1)

    if subject is None:
        subject = f"Nixtla Inventory CSVs - {datetime.now().strftime('%Y-%m-%d')}"

    attachments = create_attachments(csv_files)
    html_content = create_email_html(csv_files)
    text_content = create_email_text(csv_files)

    try:
        print(f"Sending to {to_address}...")

        response = resend.Emails.send(
            {
                "from": FROM_EMAIL,
                "to": [to_address],
                "subject": subject,
                "html": html_content,
                "text": text_content,
                "attachments": attachments,
            }
        )

        print(f"\nSUCCESS: Email sent to {to_address}")
        print(f"Attachments: {', '.join(f.name for f in csv_files)}")
        if isinstance(response, dict) and "id" in response:
            print(f"Email ID: {response['id']}")
        return True

    except Exception as e:
        print(f"ERROR: Failed to send email: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Send Nixtla inventory CSVs via Resend")
    parser.add_argument(
        "--to",
        default="jeremy@intentsolutions.io",
        help="Recipient email (default: jeremy@intentsolutions.io)",
    )
    parser.add_argument("--subject", help="Custom email subject")
    parser.add_argument("--dry-run", action="store_true", help="Preview without sending")

    args = parser.parse_args()

    csv_files = get_csv_files()

    if args.dry_run:
        print("DRY RUN - Would send:")
        print(f"  To: {args.to}")
        print(f"  From: {FROM_EMAIL}")
        print(f"  Subject: {args.subject or 'Nixtla Inventory CSVs - DATE'}")
        print(f"  Attachments: {', '.join(f.name for f in csv_files)}")
        print("\nEmail body preview:")
        print("-" * 50)
        print(create_email_text(csv_files))
        return

    send_email(args.to, args.subject)


if __name__ == "__main__":
    main()
