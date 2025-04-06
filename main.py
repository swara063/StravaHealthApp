from flask import Flask, jsonify, request, redirect
import os
from strava_auth import get_oauth_url, get_access_token
from strava_fetch import fetch_strava_data

app = Flask(__name__)

# Environment variables for Strava API
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
FRONTEND_URL = os.getenv('FRONTEND_URL')

# Start Strava OAuth
@app.route('/login')
def login():
    auth_url = get_oauth_url(CLIENT_ID, REDIRECT_URI)
    return redirect(auth_url)

# OAuth callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    access_token = get_access_token(code, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if access_token:
        # ✅ Redirect back to Streamlit with token
        return redirect(f"{FRONTEND_URL}?access_token={access_token}")
    return jsonify({'error': 'Failed to fetch access token'}), 400

# Fetch Strava data
@app.route('/fetch-data')
def fetch_data():
    access_token = request.args.get('access_token')
    if access_token:
        data = fetch_strava_data(access_token)
        return jsonify(data), 200
    return jsonify({'error': 'Access token is required'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

