"""
Run this script once to generate your OAuth2 refresh token.
Starts a local server on port 8080 to capture the OAuth callback.

Usage:
    export GOOGLE_ADS_CLIENT_ID=your_client_id
    export GOOGLE_ADS_CLIENT_SECRET=your_client_secret
    python get_refresh_token.py
"""

import json
import os
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

CLIENT_ID = os.environ["GOOGLE_ADS_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_ADS_CLIENT_SECRET"]
SCOPE = "https://www.googleapis.com/auth/adwords"
REDIRECT_URI = "http://localhost:8080"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"

auth_code_holder = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code_holder["code"] = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this tab.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing authorization code.")

    def log_message(self, format, *args):
        pass  # suppress request logs


auth_params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": SCOPE,
    "access_type": "offline",
    "prompt": "consent",
}

auth_url = AUTH_URI + "?" + urllib.parse.urlencode(auth_params)
print("\n=== Open this URL in your browser to authorize ===")
print(auth_url)
print("\nWaiting for authorization...")

server = HTTPServer(("localhost", 8080), CallbackHandler)
server.handle_request()

code = auth_code_holder.get("code")
if not code:
    raise RuntimeError("No authorization code received.")

token_data = urllib.parse.urlencode({
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}).encode()

req = urllib.request.Request(TOKEN_URI, data=token_data, method="POST")
with urllib.request.urlopen(req) as resp:
    tokens = json.loads(resp.read())

print("\n=== Copy this refresh token into google-ads.yaml ===")
print(f"refresh_token: {tokens['refresh_token']}")
