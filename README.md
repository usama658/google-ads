# Google Ads Integration

## Setup

### 1. Get a Developer Token
Go to [Google Ads API Center](https://developers.google.com/google-ads/api/docs/get-started/dev-token) and apply for a developer token from your Google Ads manager account.

### 2. Get a Refresh Token
Run the OAuth2 helper script — it will open a browser for you to authorize access:
```bash
python get_refresh_token.py
```
Copy the printed refresh token.

### 3. Create your config file
```bash
cp google-ads.yaml.template google-ads.yaml
```
Edit `google-ads.yaml` and fill in:
- `developer_token` — from step 1
- `refresh_token` — from step 2

`google-ads.yaml` is in `.gitignore` and will never be committed.

### 4. List campaigns
```bash
python google_ads_client.py --customer-id YOUR_CUSTOMER_ID
```
