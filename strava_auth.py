import requests

def get_oauth_url(client_id, redirect_uri):
    return (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
        f"&approval_prompt=force&scope=read,activity:read"
    )

def exchange_code_for_token(code, client_id, client_secret, redirect_uri):
    print(f"📡 Exchanging code for token: {code}")
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(token_url, data=payload, timeout=10)
    print(f"🧩 Token response: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json()  # Includes access_token, refresh_token, expires_at

def refresh_access_token(refresh_token, client_id, client_secret):
    print(f"🔄 Refreshing access token with refresh token: {refresh_token}")
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(token_url, data=payload, timeout=10)
    print(f"🔄 Refresh token response: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json()  # New access_token and refresh_token

