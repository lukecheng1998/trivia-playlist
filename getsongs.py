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

def getTokenFromSpotify(authURL, clientId, clientSecrets, grantType, contentType):
    # make a request here, obtains the auth token that is needed to execute commands in the spotify env
    tokenResponse = requests.post(authURL, headers= {"Content-Type": contentType}, data={"grant_type": grantType, "client_id": clientId, "client_secret": clientSecrets}).json()
    token = tokenResponse["access_token"]
    token_type = tokenResponse["token_type"]
    retToken = token_type + " " + token
    return retToken
def getPlaylistFromId(endpointURL, id, authHeader):
    # method to get the ID of the playlist
    # TODO: return errors properly rather than from methods
    newEndpointURL = endpointURL + "/users/" + id + "/playlists"
    response = requests.get(newEndpointURL, headers= {"Authorization": authHeader})
    if response.status_code != 200:
        error = "Could not get successful response for getting playlist"
        return error
    playlists = response.json()["items"]
    # iterate through the playlist body to find the Trivia playlist
    for playlist in playlists:
        if playlist["name"] == triviaPlaylist:
            print(playlist)
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
        print(len(tracks["items"].length))
    else:
        # search for song ids here
        searchAndReturnSongIds(endpointURL, authHeader, songNames)
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
    print(convertedSongNames)
    for i in range(1, len(convertedSongNames)):
        newEndpointURL = endpointURL + "/search?q=" + convertedSongNames[i]
        print(newEndpointURL)
        response = requests.get(newEndpointURL, headers={"Authorization": authHeader})
        time.sleep(1)
        if response.status_code != 200:
            error = "didn't get a successful response please check the request"
            print(error)
            continue
        print(response.json())
        #tracks = response.json()["tracks"]
        #id = extractSongIdFromSearch(tracks)
        #TODO: add the song here!

def extractSongIdFromSearch(responseJson):
    print(responseJson)
    tracks = responseJson["items"]
    if tracks.length > 0:
        track = tracks[0]
        id = track["id"]
        return id
    else:
        print("No songs available, getting next song")
def addSongsToPlaylist(endpointURL, authHeaders, songTitle):
    # get the song and add it to playlist
    newEndpointURL = endpointURL + "" #TODO: figure out what this error is here
    print(newEndpointURL)
    # response = requests.post(newEndpointURL, headers={"Authorization": authHeader})
    return

def convertedSongNamesWithArtists(songName, artistName):
    #adds space between the song names
    songName = songName.replace(" ", "%20")
    songName = songName.replace("(", "%28")
    songName = songName.replace(")", "%29")
    songName = songName.replace("!", "%21")
    songName = songName.replace("+", "%2B")
    songName = songName.replace("-", "%2D")
    songName = songName.replace("'", "%27")
    artistName = artistName.replace(" ", "%20")
    artistName = artistName.replace("(", "%28")
    artistName = artistName.replace(")", "%29")
    artistName = artistName.replace("!", "%21")
    artistName = artistName.replace("+", "%2B")
    artistName = artistName.replace("-", "%2D")
    artistName = artistName.replace("'", "%27")
    retQuery = "track%3A" + songName + "artist%3A" + artistName
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
