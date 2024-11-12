import subprocess
import base64
client_id = "555395fa580f41ff939897aff379da60"
client_secret = "98764b2630864555a86d119661a5736a"
authorization_code = "AQB0hFCPe-17jbAOWOLg_0RzATtdwQtpPLJD_yxVWY5IvFEyQ1zabpGCBTiLLJcadMnIQLgaWS_qUOpR3DV6LtMpWCO9S5UtJ6GF3iyXjpU2QHqpDkMGRiP8Dx5av22X3c99cke2s9-01vOk_BAT_ITlEoS9CaU-9etj1N0Me-EXPf083E0m6I2jHTlw710rCzc-mRux_JHOsA"
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