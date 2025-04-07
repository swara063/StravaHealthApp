import requests

def get_oauth_url(client_id, redirect_uri):
    return (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
        f"&approval_prompt=force&scope=read,activity:read"
    )

def get_access_token(code, client_id, client_secret, redirect_uri):
    print(f"📡 Starting token exchange with code: {code}")

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    try:
        response = requests.post(token_url, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Token data: {data}")
        return data  # Return full token data: access_token, refresh_token, expires_at

    except Exception as e:
        print(f"❌ Error fetching access token: {e}")
        return None

def refresh_access_token(refresh_token, client_id, client_secret):
    print(f"🔄 Refreshing access token using refresh_token: {refresh_token}")
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    try:
        response = requests.post(token_url, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Refreshed token data: {data}")
        return data

    except Exception as e:
        print(f"❌ Error refreshing access token: {e}")
        return None


