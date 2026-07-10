#!/usr/bin/env python3
"""Preview a manual-review SEI message draft.

This script renders a template against a prospect through the M7 structured API.
It does not send email, create Communications, create CRM records, or change
prospect lifecycle status.
"""

from __future__ import annotations

import argparse

from _client import call


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview an SEI message draft")
    parser.add_argument("prospect", help="SEI Prospect name")
    parser.add_argument("template", help="SEI Message Template name")
    args = parser.parse_args()

    result = call(
        "sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_message_draft",
        prospect=args.prospect,
        template=args.template,
    )
    print(result)


if __name__ == "__main__":
    main()
