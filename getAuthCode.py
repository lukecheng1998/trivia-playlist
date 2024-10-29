import base64

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
# def callback():
#     print(request.json)
#     code = request.args.get('code')
#     state = request.args.get('state')
#     if state is None:
#         return redirect('/#?error=state_mismatch')
#     token_url = 'https://accounts.spotify.com/api/token'
#     form_data = {
#         'code': code,
#         'redirect_uri': redirect_uri,
#         'grant_type': 'authorization_code'
#     }
#     client_credentials = f'{client_id}:{client_secret}'
#     encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
#
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Authorization': f'Basic {encoded_credentials}'
#     }
#
#     response = requests.post(token_url, data=form_data, headers=headers)
#
#     if response.status_code == 200:
#         token_info = response.json()
#         return jsonify(token_info)
#     else:
#         return jsonify({'error': "Failed to fetch token", 'status': response.status_code})
def callback():
    authorization_code = request.args.get('code')
    print(request.args.get('state'))
    if authorization_code:
        return f"Authorization code: {authorization_code}"
    else:
        return "Authorization failed"


if __name__ == '__main__':
    app.run(port=8080)
