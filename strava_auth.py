import requests

def get_oauth_url(client_id, redirect_uri):
    return (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
        f"&approval_prompt=force&scope=read,activity:read"
    )

import requests

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
    print(f"📦 Payload for token request: {payload}")

    try:
        response = requests.post(token_url, data=payload, timeout=10)  # ⏰ Add timeout!
        print(f"🧩 Token response status: {response.status_code}")
        print(f"🧩 Token response body: {response.text}")
        response.raise_for_status()  # raises an error if not 200
        return response.json().get('access_token')
    except Exception as e:
        print(f"❌ Error fetching access token: {e}")
        return None


