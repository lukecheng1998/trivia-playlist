import requests
from bs4 import BeautifulSoup
import json
import time

# This file will get the songs and convert to a json file
# Make a GET request to the URL
triviaPlaylist = "Trivia Playlist"
def beginProcess(url):
    response = requests.get(url)
    songArray = scrapeArticle(response)
    print(songArray)
    return songArray

def getTokenFromSpotifyNew(authURL, code, content_type_2):
    print("inside getting token obtaining token now")
    tokenResponse = requests.post(authURL, headers={"Content-Type": content_type_2, "Authorization": "Basic $(echo -n '555395fa580f41ff939897aff379da60:98764b2630864555a86d119661a5736a' | base64)"}, data={'grant_type': "authorization_code", "code": code, "redirect_uri": "http://localhost:8080/callback"})
    print("Token Response: ", tokenResponse)
    return tokenResponse

def getTokenFromSpotify(authURL, clientId, clientSecrets, grantType, contentType, scope):
    # make a request here, obtains the auth token that is needed to execute commands in the spotify env
    tokenResponse = requests.post(authURL, headers= {"Content-Type": contentType}, data={"grant_type": grantType, "client_id": clientId, "client_secret": clientSecrets, "scope": scope}).json()
    token = tokenResponse["access_token"]
    token_type = tokenResponse["token_type"]
    # retToken = token_type + " " + token
    retToken = token
    return retToken
def getPlaylistFromId(endpointURL, id, authHeader):
    # method to get the ID of the playlist
    # TODO: return errors properly rather than from methods
    newEndpointURL = endpointURL + "/users/" + id + "/playlists"
    print(newEndpointURL)
    response = requests.get(newEndpointURL, headers= {"Authorization": authHeader})
    if response.status_code != 200:
        error = "Could not get successful response for getting playlist, here is the error"
        return error
    playlists = response.json()["items"]
    # iterate through the playlist body to find the Trivia playlist
    for playlist in playlists:
        if playlist["name"] == triviaPlaylist:
            print(playlist["id"])
            return playlist["id"]
    error = "Playlist does not exist, please create the playlist"
    return error

def updateOrModifyPlaylist(endpointURL, playlistId, authHeader, songNames):
    # after getting the playlist we need to see if the playlist needs to be changed or if songs need to be added to it
    newEndpointURL = endpointURL + "/playlists/" + playlistId
    response = requests.get(newEndpointURL, headers= {"Authorization": authHeader}).json()
    tracks = response["tracks"]
    if len(tracks["items"]) > 0:
        # delete the tracks and reset
        print("To be deleted")
    # search for song ids here
    searchedSongIds = searchAndReturnSongIds(endpointURL, authHeader, songNames)
    #TODO: add songs here AND continue from here Luke C.
    adjustedSongs = adjustSongURLAndGetList(searchedSongIds)
    print(adjustedSongs)
    newEndpointURL = endpointURL + "/playlists/" + playlistId + "/tracks"
    print("New Endpoint URL: " + newEndpointURL)
    #TODO: create a query here
    for song in adjustedSongs:
        song_data = {
            "uris": [song],
            "position": 0
        }
        response = requests.post(newEndpointURL, headers={"Authorization": authHeader, "Content-Type": "application/json", "Accept": "application/json"}, json=song_data)
        print(type(response)) #TODO: FIRST add here
        if response.status_code < 200 or response.status_code > 299:
            # VERY IMPORTANT: You need to set a scope in order for songs to be added. Client credentials will not work
            # for this authorization Also note, from this link,
            # https://developer.spotify.com/documentation/web-api/concepts/playlists public playlists can not be
            # collaborative and vice versa
            error = response.json()
            print(error)
            continue
        responseDict = response.json()
        print(responseDict)
    print("Successfully added stuff to playlists")
    return response

def searchAndReturnSongIds(endpointURL, authHeader, songNames):
    # searches for spotify's song Ids from the song/artist names listed
    convertedSongNames = []
    print("In search and return")
    for i in range(0, len(songNames) - 1):
        songName = songNames[i]
        artistName = songNames[i + 1]
        songArtistQuery = convertedSongNamesWithArtists(songName, artistName)
        songArtistQuery += "&type=track&market=US"
        convertedSongNames.append(songArtistQuery)
        i += 1
    # TODO: change this URL
    print("extracted songs")
    arrayOfSongIds = []
    print("length of convertSongNames: ", len(convertedSongNames))
    for i in range(1, len(convertedSongNames)):
        newEndpointURL = endpointURL + "/search?q=" + convertedSongNames[i]
        response = requests.get(newEndpointURL, headers={"Authorization": authHeader})
        # time.sleep(1)
        if response.status_code < 200 or response.status_code > 299:
            error = "didn't get a successful response please check the request"
            print(error)
            continue
        #print(response.json())
        # TODO: add the song here!
        result = extractSongIdFromSearch(response)
        if result != -1:
            arrayOfSongIds.append(result)
    print("successfully obtained array of songIds: ", arrayOfSongIds)
    return arrayOfSongIds

def extractSongIdFromSearch(responseJson):
    # gets the song ID which is what we need to insert it into our playlist
    tracks = responseJson.json()["tracks"]
    items = tracks["items"]
    if len(items) < 1:
        return -1
    album = items[0]
    songId = album["id"]
    return songId
def adjustSongURLAndGetList (songIDs):
    # get the song and add it to playlist
    #TODO FROM HERE: This is the proper link https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
    urlSongs = []
    for song in songIDs:
        urlSong = "spotify:track:" + song
        urlSongs.append(urlSong)
    # response = requests.post(newEndpointURL, headers={"Authorization": authHeader})
    return urlSongs

def convertedSongNamesWithArtists(songName, artistName):
    #makes song names and artist name much more compatible with a URL request
    songName = songName.replace(" ", "%2520")
    songName = songName.replace("(", "%2528")
    songName = songName.replace(")", "%2529")
    songName = songName.replace("!", "%2521")
    songName = songName.replace("+", "%252B")
    songName = songName.replace("-", "%252D")
    songName = songName.replace("'", "%2527")
    artistName = artistName.replace(" ", "%2520")
    artistName = artistName.replace("(", "%2528")
    artistName = artistName.replace(")", "%2529")
    artistName = artistName.replace("!", "%2521")
    artistName = artistName.replace("+", "%252B")
    artistName = artistName.replace("-", "%252D")
    artistName = artistName.replace("'", "%2527")
    retQuery = "track%253A" + songName + "artist%253A" + artistName
    return retQuery

def convertArrayToJson(songArray):
    with open('output.json', 'w', encoding='utf-8') as outfile:
        json.dump(songArray, outfile, ensure_ascii=False, indent=4)
    return json.dumps(songArray)


def scrapeArticle(response):
    # Check if the request was successful (status code 200)
    html = ""
    if response.status_code == 200:
        # Print the content of the webpage
        print("successfully obtained response")
        html = response.text
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
    soup = BeautifulSoup(html, 'html.parser')
    # Get the td value as the list of songs are in that section
    td = soup.body.find_all(['td'])
    if (td == None):
        return []
    # standardize the strings and then remove all the special characters
    strings = str(td).lower()
    strings = strings.replace("\\r", "")
    strings = strings.replace("\\n", "")
    stringArray = strings.split("\"")
    # Get the song titles by obtaining the index next to the title=
    indicies = [i + 1 for i, x in enumerate(stringArray) if x == ' title=']
    songTitles = []
    # Get the song titles
    for i in indicies:
        if 'billboard year-end ' in stringArray[i]:
            continue
        else:
            songTitles.append(stringArray[i])
    return songTitles
