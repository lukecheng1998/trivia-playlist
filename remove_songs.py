import requests
# global response


def remove_songs(url, auth_token, songs):
    global response
    response = ""
    for song in songs:
        song_data = {
            "tracks": [
                {
                    song
                }
            ]
        }
        response = requests.post(url, headers={"Authorization": auth_token, "Content-Type": "application/json"}, json=song_data)
        if response.status_code < 200 or response.status_code > 299:
            error = response.json()
            print(error)
            continue
    print("Successfully cleared playlist")
    return response