import requests

def fetch_strava_data(access_token):
    print(f"Using access token: {access_token}")

    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("✅ Data fetched successfully")
        print(data)  # Log the data
    except Exception as e:
        print(f"❌ Error fetching Strava data: {e}")
        data = None

    return data
