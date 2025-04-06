import requests

def get_oauth_url(client_id, redirect_uri):
    return (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
        f"&approval_prompt=force&scope=read,activity:read"
    )

def get_access_token(code, client_id, client_secret, redirect_uri):
    url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException:
        return None

