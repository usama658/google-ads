"""
Run this script once to get your OAuth2 refresh token for Google Analytics.
Uses the same OAuth2 client credentials as Google Ads.

Usage:
    export GOOGLE_CLIENT_ID="your-client-id"
    export GOOGLE_CLIENT_SECRET="your-client-secret"
    python get_analytics_token.py
"""
import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
]

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables first.")
    print("  export GOOGLE_CLIENT_ID='your-client-id'")
    print("  export GOOGLE_CLIENT_SECRET='your-client-secret'")
    sys.exit(1)

CLIENT_CONFIG = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}


def main():
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)

    print("\n=== Google Analytics OAuth2 Setup ===")
    print("Opening browser for authorization...\n")

    try:
        credentials = flow.run_local_server(port=0)
    except Exception:
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
        auth_url, _ = flow.authorization_url(prompt="consent")
        print(f"Visit this URL to authorize:\n\n  {auth_url}\n")
        code = input("Paste the authorization code here: ").strip()
        flow.fetch_token(code=code)
        credentials = flow.credentials

    print("\n=== SUCCESS ===")
    print(f"Refresh Token: {credentials.refresh_token}")
    print("\nAdd this to analytics-config.yaml under 'refresh_token:'")


if __name__ == "__main__":
    main()
