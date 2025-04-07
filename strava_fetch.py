import requests

def fetch_strava_data(access_token):
    print(f"🔑 Fetching data with token: {access_token}")
    headers = {'Authorization': f'Bearer {access_token}'}
    url = "https://www.strava.com/api/v3/athlete/activities"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"❌ Error fetching Strava data: {e}")
        return {"error": str(e)}

