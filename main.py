from flask import Flask, jsonify, request, redirect
import os
from strava_auth import get_oauth_url, get_access_token, refresh_access_token
from strava_fetch import fetch_strava_data
import sys
import time
import requests

print("✅ Imports successful, proceeding to app setup...")

# Initialize Flask app
app = Flask(__name__)

# Flush logs immediately
def flush():
    sys.stdout.flush()
    sys.stderr.flush()

# Home route for sanity check
@app.route('/')
def home():
    return '🚂 Server is running. Try /login to start authentication.'

@app.route('/health')
def health():
    return '✅ Healthy', 200

print("🚀 App is starting...")
flush()

# Environment variables
CLIENT_ID = os.getenv('CLIENT_ID') or os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET') or os.getenv('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI') or os.getenv('STRAVA_REDIRECT_URI')
FRONTEND_URL = os.getenv('FRONTEND_URL')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')or os.getenv('STRAVA_REFRESH_TOKEN')
BACKEND_URL = "https://stravahealthapp-production.up.railway.app"
response = requests.get(f"{BACKEND_URL}/refresh")

@app.route('/refresh')
def refresh():
    print(f"🌟 CLIENT_ID: {CLIENT_ID}")
    print(f"🌟 CLIENT_SECRET: {CLIENT_SECRET}")
    print(f"🌟 REFRESH_TOKEN: {REFRESH_TOKEN}")
    flush()

    refresh_token = REFRESH_TOKEN
    if not refresh_token:
        return jsonify({'error': 'No refresh token found in environment'}), 400

    token_data = refresh_access_token(
        refresh_token,
        CLIENT_ID,
        CLIENT_SECRET
    )

    if token_data and token_data.get('access_token'):
        return jsonify(token_data), 200
    else:
        return jsonify({'error': 'Failed to refresh token'}), 500


# Route: Start OAuth process
@app.route('/login')
def login():
    auth_url = get_oauth_url(CLIENT_ID, REDIRECT_URI)
    print(f"🔗 Redirecting to: {auth_url}")
    flush()
    return redirect(auth_url)

# Route: OAuth callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"🪝 Callback received! Code: {code}")
    flush()

    if not code:
        return jsonify({'error': 'No code parameter in callback'}), 400

    token_data = get_access_token(code, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    if not token_data:
        return jsonify({'error': 'Failed to retrieve token data'}), 500

    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')

    if not access_token:
        return jsonify({'error': 'No access token found'}), 500

    # Fetch athlete data
    athlete_data = fetch_strava_data(access_token)

    if athlete_data is None:
        return jsonify({'error': 'Failed to fetch athlete data'}), 500

    # Optionally, redirect to frontend with token info
    if FRONTEND_URL:
        redirect_url = f"{FRONTEND_URL}?access_token={access_token}&refresh_token={refresh_token}"
        print(f"➡️ Redirecting to frontend: {redirect_url}")
        flush()
        return redirect(redirect_url)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'athlete_data': athlete_data
    })

# Optional: Background token refresh loop
def background_token_refresher():
    while True:
        try:
            print("🔄 Background token refresher running...")
            flush()
            if REFRESH_TOKEN:
                token_data = refresh_access_token(
                    REFRESH_TOKEN,
                    CLIENT_ID,
                    CLIENT_SECRET
                )
                if token_data and token_data.get('access_token'):
                    print("✅ Token refreshed successfully in background.")
                    flush()
                else:
                    print("⚠️ Failed to refresh token in background.")
                    flush()
            time.sleep(3600)  # Sleep for 1 hour
        except Exception as e:
            print(f"❌ Exception in background refresher: {e}")
            flush()
            time.sleep(3600)

# Start the background refresher in a separate thread if you want
import threading
threading.Thread(target=background_token_refresher, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))



