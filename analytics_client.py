"""
Google Analytics Data API (GA4) client.
Lists top pages, sessions, and users for a given date range.

Usage:
    python analytics_client.py --start-date 30daysAgo --end-date today
    python analytics_client.py --start-date 2024-01-01 --end-date 2024-01-31
"""
import argparse
import sys

import yaml
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2.credentials import Credentials

CONFIG_FILE = "analytics-config.yaml"


def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Config file '{path}' not found.")
        print("  1. Copy analytics-config.yaml.template to analytics-config.yaml")
        print("  2. Run python get_analytics_token.py to get your refresh token")
        print("  3. Fill in client_id, client_secret, refresh_token, and property_id")
        sys.exit(1)


def build_client(config: dict) -> BetaAnalyticsDataClient:
    credentials = Credentials(
        token=None,
        refresh_token=config["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config["client_id"],
        client_secret=config["client_secret"],
    )
    return BetaAnalyticsDataClient(credentials=credentials, transport="rest")


def run_report(client: BetaAnalyticsDataClient, property_id: str, start_date: str, end_date: str) -> None:
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="activeUsers"),
            Metric(name="screenPageViews"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=20,
        order_bys=[{"metric": {"metric_name": "sessions"}, "desc": True}],
    )
    response = client.run_report(request)

    print(f"\nTop pages ({start_date} → {end_date})  |  Property {property_id}")
    print("-" * 80)
    print(f"{'Page':<45} {'Sessions':>10} {'Users':>10} {'Pageviews':>10}")
    print("-" * 80)
    for row in response.rows:
        page = row.dimension_values[0].value[:44]
        sessions = row.metric_values[0].value
        users = row.metric_values[1].value
        views = row.metric_values[2].value
        print(f"{page:<45} {sessions:>10} {users:>10} {views:>10}")


def main():
    parser = argparse.ArgumentParser(description="Query Google Analytics GA4 data")
    parser.add_argument("--start-date", default="30daysAgo", help="Start date (YYYY-MM-DD or e.g. 30daysAgo)")
    parser.add_argument("--end-date", default="today", help="End date (YYYY-MM-DD or 'today')")
    parser.add_argument("--config", default=CONFIG_FILE, help="Path to analytics-config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    property_id = str(config["property_id"])

    client = build_client(config)

    try:
        run_report(client, property_id, args.start_date, args.end_date)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
