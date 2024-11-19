import os
import subprocess
import base64
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
authorization_code = ""
redirect_uri = "http://localhost:8080/callback"

client_credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(client_credentials.encode()).decode()

#curl_command
curl_command = [
    "curl", "-X", "POST", "https://accounts.spotify.com/api/token",
    "-H", f"Authorization: Basic {encoded_credentials}",
    "-H", "Content-Type: application/x-www-form-urlencoded",
    "-d", f"grant_type=authorization_code",
    "-d", f"code={authorization_code}",
    "-d", f"redirect_uri={redirect_uri}"
]

def get_token():
    result = subprocess.run(curl_command, capture_output=True, text=True)
    if result.returncode == 0:
        return result
    else:
        print("Error: ", result.stderr)