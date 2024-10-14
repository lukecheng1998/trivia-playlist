# This is a sample Python script.
import getsongs
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
auth_code = 'AQC2CdrM0guE7N7E2j8vsytdmRa7oQOB5GLmkqpMRo5qnYpRy6-TVuZgCsxBclZB_4OzeIJnp2I8QZhSAifMNwRl5x7_iJVBKlJbI1Yw4slHoICbSyfLGjXUjtMp0ydiJEnFT2CtHwZ-asPtMB2YYMfPY0sdSocFNKki5vmuk9zmK5RW9G2TW-9DKXcDy2yMcb9eD5Gvh8QOmg'
content_type_2 = 'localhost:8080/callback'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    songNames = getsongs.beginProcess(url)
    token = getsongs.getTokenFromSpotify(authURL, clientId, clientSecret, grantType, contentType, scope)
    print("Token from spotify new: ", getsongs.getTokenFromSpotifyNew(authURL, clientId, clientSecret, auth_code, content_type_2, contentType, scope))
    playlistId = getsongs.getPlaylistFromId(endpointURL, username, token)
    getsongs.updateOrModifyPlaylist(endpointURL, playlistId, token, songNames)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
