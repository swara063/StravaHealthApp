import requests

# Fetch activity data from Strava API
def fetch_strava_data(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": 1, "page": 1}  # Fetch the most recent activity

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        activity = response.json()[0]
        data = {
            'distance': activity['distance'] / 1000,  # Convert meters to kilometers
            'heart_rate': activity.get('average_heartrate', 'N/A'),
            'calories_burned': activity.get('calories', 'N/A')
        }
        return data
    return {'error': 'Failed to fetch data'}
