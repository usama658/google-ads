"""
Google Ads API connection test.
Lists all campaigns for the configured customer account.

Usage:
    pip install -r requirements.txt
    python main.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "3693492303"


def list_campaigns(client: GoogleAdsClient, customer_id: str) -> None:
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM campaign
        ORDER BY campaign.name
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    print(f"\nCampaigns for account {customer_id}:\n")
    for batch in response:
        for row in batch.results:
            campaign = row.campaign
            metrics = row.metrics
            cost = metrics.cost_micros / 1_000_000

            print(
                f"  [{campaign.id}] {campaign.name}"
                f" | Status: {campaign.status.name}"
                f" | Impressions: {metrics.impressions}"
                f" | Clicks: {metrics.clicks}"
                f" | Cost: ${cost:.2f}"
            )


def main() -> None:
    client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    try:
        list_campaigns(client, CUSTOMER_ID)
    except GoogleAdsException as ex:
        for error in ex.failure.errors:
            print(f"Error: {error.message}")
        raise


if __name__ == "__main__":
    main()
