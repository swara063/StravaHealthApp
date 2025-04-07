from flask import Flask, jsonify, request, redirect
import os
from strava_auth import get_oauth_url, get_access_token, refresh_access_token
from strava_fetch import fetch_strava_data

import sys

def flush():
    sys.stdout.flush()
    sys.stderr.flush()

print("🚀 App is starting...")
flush()


app = Flask(__name__)

CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI')
FRONTEND_URL = os.getenv('FRONTEND_URL')


@app.route('/login')
def login():
    auth_url = get_oauth_url(CLIENT_ID, REDIRECT_URI)
    print(f"🔗 Redirecting to: {auth_url}")
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"🪝 Callback received! Code: {code}")

    token_data = get_access_token(code, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if token_data and token_data.get('access_token'):
        params = (
            f"?access_token={token_data['access_token']}"
            f"&refresh_token={token_data['refresh_token']}"
            f"&expires_at={token_data['expires_at']}"
        )
        return redirect(f"{FRONTEND_URL}{params}")

    return jsonify({'error': 'Failed to fetch access token'}), 400


@app.route('/fetch-data')
def fetch_data():
    access_token = request.args.get('access_token')
    if access_token:
        data = fetch_strava_data(access_token)
        return jsonify(data), 200
    return jsonify({'error': 'Access token is required'}), 400


@app.route('/refresh-token')
def refresh_token():
    refresh_token = request.args.get('refresh_token')
    if refresh_token:
        new_tokens = refresh_access_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
        return jsonify(new_tokens), 200
    return jsonify({'error': 'Refresh token is required'}), 400


import sys
import traceback

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"🔥 Exception: {e}")
    traceback.print_exc(file=sys.stdout)
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

