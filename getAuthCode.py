from flask import Flask, request, redirect
import requests

app = Flask(__name__)
scope = 'playlist-modify-public'
redirect_uri = 'http://localhost:8080/callback'
auth_url= 'https://accounts.spotify.com/authorize'
client_id = '555395fa580f41ff939897aff379da60'
client_secret = '98764b2630864555a86d119661a5736a'

@app.route('/')
def login():
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope
    }
    auth_request_url = requests.Request('GET', auth_url, headers={'Content-Type': 'application/json'}, params=params).prepare().url
    return redirect(auth_request_url)


@app.route('/callback')
def callback():
    authorization_code = request.args.get('code')
    print(request.args.get('state'))
    if authorization_code:
        return f"Authorization code: {authorization_code}"
    else:
        return "Authorization failed"

@app.route("/callback-more")
def callback_more():
    print("this works")

if __name__ == '__main__':
    app.run(port=8080)
#auth-code:  AQA8fgNL5bkS1tSQvMfkRiWzOANvgmvO2cfbFccYuVT-psOKFJMmRhL6VwPm-bnWN_7JIRSKqHeqZioY6y7UtSvO6VGPl5xdtkpSD3pmb3y0n6Nd6eDooaZQeggZyZg6vPge6hGleAHDPh8X_aO_F8OLNgcO5r5EZttmScW2Jq6xea0rqT_AUFRoD4hk8Dz030g8HoFgfP1Kvw
