# Google Ads & Analytics Integration

## Google Ads Setup

### 1. Get a Developer Token
Go to [Google Ads API Center](https://developers.google.com/google-ads/api/docs/get-started/dev-token) and apply for a developer token from your Google Ads manager account.

### 2. Get a Refresh Token
```bash
export GOOGLE_ADS_CLIENT_ID="your-client-id"
export GOOGLE_ADS_CLIENT_SECRET="your-client-secret"
python get_refresh_token.py
```

### 3. Create your config file
```bash
cp google-ads.yaml.template google-ads.yaml
# Fill in: developer_token, client_id, client_secret, refresh_token
```

### 4. List campaigns
```bash
python google_ads_client.py --customer-id YOUR_CUSTOMER_ID
```

---

## Google Analytics (GA4) Setup

### 1. Get a Refresh Token
```bash
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
python get_analytics_token.py
```

### 2. Find your GA4 Property ID
Google Analytics → Admin → Property Settings → Property ID (a plain number, e.g. `123456789`)

### 3. Create your config file
```bash
cp analytics-config.yaml.template analytics-config.yaml
# Fill in: client_id, client_secret, refresh_token, property_id
```

### 4. Query your data
```bash
# Last 30 days (default)
python analytics_client.py

# Custom date range
python analytics_client.py --start-date 2024-01-01 --end-date 2024-01-31
```

---

> `google-ads.yaml` and `analytics-config.yaml` are in `.gitignore` and will never be committed.
