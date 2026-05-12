"""
Google Ads API client — lists accessible campaigns for a given customer ID.
Requires google-ads.yaml to be configured with a valid refresh_token.

Usage:
    python google_ads_client.py --customer-id 1234567890
"""
import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def list_campaigns(client: GoogleAdsClient, customer_id: str) -> None:
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type
        FROM campaign
        ORDER BY campaign.id
    """
    response = ga_service.search_stream(customer_id=customer_id, query=query)

    print(f"\nCampaigns for customer {customer_id}:")
    print("-" * 60)
    for batch in response:
        for row in batch.results:
            c = row.campaign
            print(f"  ID: {c.id}  |  {c.name}  |  Status: {c.status.name}  |  Type: {c.advertising_channel_type.name}")


def main():
    parser = argparse.ArgumentParser(description="List Google Ads campaigns")
    parser.add_argument("--customer-id", required=True, help="Google Ads customer ID (digits only)")
    parser.add_argument("--config", default="google-ads.yaml", help="Path to google-ads.yaml")
    args = parser.parse_args()

    customer_id = args.customer_id.replace("-", "")

    try:
        client = GoogleAdsClient.load_from_storage(args.config)
    except FileNotFoundError:
        print(f"ERROR: Config file '{args.config}' not found.")
        print("  1. Copy google-ads.yaml.template to google-ads.yaml")
        print("  2. Run python get_refresh_token.py to get your refresh token")
        print("  3. Fill in your developer_token and refresh_token")
        sys.exit(1)

    try:
        list_campaigns(client, customer_id)
    except GoogleAdsException as ex:
        for error in ex.failure.errors:
            print(f"Google Ads API error: {error.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
