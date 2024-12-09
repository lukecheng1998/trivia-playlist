# This is a sample Python script.
import getsongs
import getTokenFromScript
import remove_songs

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
auth_code = 'AQCmvu59l-qPviMja9ChXSQtDqe63XqaXELauZKIbvUk-S1Rt5DM3CSocyLZ87mBhid9fG5C66PmpGGecrsgdOJy1zUoHmCPt86wt5nsqaYSlRpOpZs8PRBN78sWj-9MSyW-6Xp3IJFcLqJVoaM60QCXrdjLsDV-6nx6RlrWo381hV_7SACnKnBiEREp8WnANPT2Uxset3rAeA'
content_type_2 = 'application/x-www-form-urlencoded'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    songNames = getsongs.beginProcess(url)
    token = getTokenFromScript.get_token().stdout
    access_token = "Bearer BQD_zkmZB6SgE9sn1UKS8_GDwKPX7yApN3j_jNyh15W_AQ_tOY-mx1yGma55Oa8D2u0K4FswQoPukbFORBev_A7qgpsrXvP8FpBc90uz9U5Iu0_dQ3_dPXOcrsMJBynvj2x-m8iiLbnJEb8pofo7NS3N1tWmoOG6fgWSuFzr2al3mhb-JK2VNwisrciOsZeR_UXxFYreD602npp2epZUz0ArGQ"
    playlistId = getsongs.getPlaylistFromId(endpointURL, username, access_token)
    getsongs.updateOrModifyPlaylist(endpointURL, playlistId, access_token, songNames)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
