from flask import Flask, jsonify, request, redirect
import os
import sys
import traceback
from strava_auth import get_oauth_url, exchange_code_for_token, refresh_access_token
from strava_fetch import fetch_strava_data

app = Flask(__name__)

# Load environment variables
CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI')
FRONTEND_URL = os.getenv('FRONTEND_URL')

# OAuth: Start login
@app.route('/login')
def login():
    auth_url = get_oauth_url(CLIENT_ID, REDIRECT_URI)
    print(f"🔗 Redirecting to Strava OAuth: {auth_url}")
    return redirect(auth_url)

# OAuth: Callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"🪝 Callback received! Code: {code}")

    try:
        token_response = exchange_code_for_token(code, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

        access_token = token_response['access_token']
        refresh_token = token_response.get('refresh_token')
        expires_at = token_response.get('expires_at')

        print(f"✅ Access token: {access_token}")
        print(f"🔄 Refresh token: {refresh_token}")
        print(f"⏳ Expires at: {expires_at}")

        # Optionally: Store refresh token securely (if you implement DB/cache)
        return redirect(f"{FRONTEND_URL}?access_token={access_token}&refresh_token={refresh_token}&expires_at={expires_at}")

    except Exception as e:
        print(f"❌ Error exchanging code for token: {e}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'error': 'Failed to fetch access token'}), 400

# API: Fetch Strava data
@app.route('/fetch-data')
def fetch_data():
    access_token = request.args.get('access_token')
    refresh_token = request.args.get('refresh_token')
    expires_at = int(request.args.get('expires_at', 0))

    if not access_token:
        return jsonify({'error': 'Access token is required'}), 400

    try:
        import time
        current_time = int(time.time())
        if current_time >= expires_at:
            print("♻️ Access token expired, refreshing...")
            token_response = refresh_access_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
            access_token = token_response['access_token']
            print(f"✅ New access token: {access_token}")

        data = fetch_strava_data(access_token)
        return jsonify(data), 200

    except Exception as e:
        print(f"🔥 Error fetching Strava data: {e}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({"error": str(e)}), 500

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"🔥 Uncaught exception: {e}")
    traceback.print_exc(file=sys.stdout)
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)


