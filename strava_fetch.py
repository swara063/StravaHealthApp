import requests

def fetch_strava_data(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        activities = response.json()

        if not activities:
            return {'error': 'No activities found'}

        latest_activity = activities[0]
        return {
            'distance': latest_activity.get('distance', 0) / 1000,  # meters to km
            'heart_rate': latest_activity.get('average_heartrate', 'N/A'),
            'calories_burned': latest_activity.get('kilojoules', 'N/A')
        }
    except requests.RequestException as e:
        return {'error': str(e)}
