"""
Run this script once to generate your OAuth2 refresh token.
It will open a browser window asking you to authorize the app.

Usage:
    export GOOGLE_ADS_CLIENT_ID=your_client_id
    export GOOGLE_ADS_CLIENT_SECRET=your_client_secret
    pip install -r requirements.txt
    python get_refresh_token.py
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = os.environ["GOOGLE_ADS_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_ADS_CLIENT_SECRET"]
SCOPES = ["https://www.googleapis.com/auth/adwords"]

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
credentials = flow.run_local_server(port=0)

print("\n=== Copy this refresh token into google-ads.yaml ===")
print(f"refresh_token: {credentials.refresh_token}")
