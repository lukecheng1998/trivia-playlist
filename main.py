# This is a sample Python script.
import getsongs
import getTokenFromScript
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# FIELDS
url = 'https://en.wikipedia.org/wiki/List_of_Billboard_Year-End_number-one_singles_and_albums'
authURL = 'https://accounts.spotify.com/api/token'
contentType = 'application/x-www-form-urlencoded'
grantType = 'client_credentials'
clientId = '555395fa580f41ff939897aff379da60'
clientSecret = '98764b2630864555a86d119661a5736a'
endpointURL = 'https://api.spotify.com/v1'
username = '1256375693'
scope = 'playlist-modify-public'
auth_code = 'AQC825eUf3qUJ1-AJZEBB8YObDE4BEqWabHBh0qPLlLjfurNdm6PQ4i7AqNq8ZFlIl2tgbLHkQyMoDG8O8ndMjmwqgbZMnY4aBc-_raG3fgsdTT8EwYkOcpj-20unNg15o4D_1WXr57UZXh0_3p5W3sHCuri5WZLf4lXTSt7I6gGgBPqMjzz7n0kZsdsLHRCeWlgXnGWeTOkUw'
content_type_2 = 'application/x-www-form-urlencoded'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    songNames = getsongs.beginProcess(url)
    token = getTokenFromScript.get_token().stdout
    if token.__contains__("error"):
        print("Error in token ", token)
    print("token obtained from script: ", token)
    access_token = token["access_token"]
    playlistId = getsongs.getPlaylistFromId(endpointURL, username, token)
    getsongs.updateOrModifyPlaylist(endpointURL, playlistId, token, songNames, access_token)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
