import requests
import json

#Globals
playlistSongIds = []
playlistDict = {}
songImportErrors = {}
apiToken = ""
user_id = ""

def importFile():
    file = open('tunes.txt','r')
    return file

def stringFormat(inputString):
    returnString = inputString.replace('w/','')
    returnString = returnString.replace('\n','')
    returnString = returnString.lstrip()
    return returnString

def readTunes(importedTunes):
    tunesDict = {}
    for i in importedTunes:
        split = i.split('-')
        artist = stringFormat(split[0])
        song = stringFormat(split[1])

        if artist not in tunesDict.keys():
            tunesDict[artist] = song
       
    print(tunesDict)
    return(tunesDict)

def getSpotifySongIds(tunes):
    trackIds = []
    endpoint_url = "https://api.spotify.com/v1/search?"
    for key, value in tunes.items():
        artist = (f'{key}')
        track = (f'{value}')
        print("Currently Searching for:")
        print("{:<8} {:<15} {:<10}".format('Success','Artist','Track'))
        print("{:<8} {:<15} {:<10}".format('...',artist,track))
        print(artist,track)
        query = f"{endpoint_url}q=name:'{track}%20'artist:'{artist}'&type=track&limit=2&offset=0&include_external=no"
        headers = {
        "Accept": "application/json",
        "Content-Type":"application/json",
        "Authorization": "Bearer " + apiToken
        }
        
        track_id = requests.get(url = query, headers=headers)

        try:
            trackIds.append(track_id.json()['tracks']['items'][0]['id'])
            print("{:<8} {:<15} {:<10}".format('Success',artist,track))
        
        except:
            songImportErrors[artist] = track
            print("There was an error with this track:", artist, track)
            print('\n Let\'s attempt to find this using another method')
            print

            
    for x in trackIds:
        print(x)
    return trackIds
           # print(trackId)

def createSpotifyPlaylist():

    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
    "Content-Type":"application/json",
    "Authorization": "Bearer " + apiToken
    }
    request_body = json.dumps({
            "name": "Club Hitz 2009-2019",
            "description": "Few throwbacks innit",
            "public": False # let's keep it between us - for now
            })

    response = requests.post(url = endpoint_url, data = request_body, headers=headers)
    playlist_id = response.json()['id']
    print(playlist_id)
    return playlist_id

def getPlaylistSongs(playlist_id):
    songIds = []
    user_id = "cavioj"
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
    "Content-Type":"application/json",
    "Authorization": "Bearer " + apiToken
    }
    try:
        response = requests.get(url = endpoint_url, headers=headers)
        for x in response.json()['tracks']['items']:
            songIds.append(x['track']['id'])
        return songIds
    except:
        print("There was an error with the API when trying to obtain the songs within the playlist:", playlist_id )
        print(response.status_code)
        return False


def checkSpotifyPlaylist():
    playlist_name = "Club Hitz 2009-2019"
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists?limit=10"
    headers = {
    "Content-Type":"application/json",
    "Authorization": "Bearer " + apiToken
    }
    try:
        response = requests.get(url = endpoint_url, headers=headers)
    except:
        print("There was an error with the API when trying to obtain the playlists of user: ", user_id )
        print(response.status_code)

    for x in response.json()['items']:
        if x['name'] == playlist_name:
            print("We already have a playlist with that name: ", playlist_name )
            playlist_id = x['id']
            playlistSongIds = getPlaylistSongs(playlist_id)
            playlistDict[playlist_id] = playlistSongIds
            return playlist_id
        else:
            print("No playlist was found")
            createSpotifyPlaylist()

def addToSpotifyPlaylist(spotifyPlaylistId, trackIds):
    uriString = ""
    print("Adding: ", len(trackIds)," tracks")
    for x in range(len(trackIds)):
        if (trackIds[x] not in playlistDict[spotifyPlaylistId]):
            song_id = trackIds[x]
            if x == len(trackIds)-1:
                uricreator = f"spotify:track:{song_id}"
            else:
                uricreator = f"spotify:track:{song_id},"
            uriString += uricreator

    endpoint_url = f"https://api.spotify.com/v1/playlists/{spotifyPlaylistId}/tracks?uris={uriString}"
    headers = {
    "Content-Type":"application/json",
    "Authorization": "Bearer " + apiToken
    }
    request_body = json.dumps({
            "uris" : uriString
            })
    print(request_body)
    response = requests.post(url = endpoint_url, headers=headers)
    print(response.status_code)

importedTunes = importFile()
tunes = readTunes(importedTunes)
trackIds = getSpotifySongIds(tunes)
playlist_id = checkSpotifyPlaylist()
#print("Show me the playlist!!!")
#print(playlistDict[playlist_id])
addToSpotifyPlaylist(playlist_id,trackIds)
if len(songImportErrors.items()) >= 1:
    print("We had issues importing the following tracks")
    print("{:<8} {:<15} {:<10}".format('Number','Artist','Track'))
    num = 0 
    for k, v in songImportErrors.items():
        print("{:<8} {:<15} {:<10}".format(num, k, v))
        num = num + 1
