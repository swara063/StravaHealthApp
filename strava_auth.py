import requests

def get_oauth_url(client_id, redirect_uri):
    return f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=read,activity:read"

def get_access_token(code, client_id, client_secret, redirect_uri):
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    return None
