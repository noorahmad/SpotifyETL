from spotify import *
from logger import *
from models import track
from extract import *
from transform import *

# retrieve all of the song files
song_files = read_all_files('music')

# authenticate with spotify
auth = authenticate()

for file in song_files:
    # parse song into track object
    track_obj = transform(file)
    
    # something went wrong with this file and it SHOULD be quaratined to review later
    if (track_obj == None):
        continue

    # move it to the dropbox
#    move(root() + track_obj.filepath, "dropbox")

    # use request obj to search for the song in spotify
    response_items = spotify_req.search("",track_obj, auth['access_token'])
    if (response_items == None):
        continue

    # take parsed response find best match
    match = find_match(track_obj, response_items)

    # use the response ID to save the song to spotify
    url="https://api.spotify.com/v1/playlists/6X2Bt8i7kmf0LQsLr1FSER/tracks?uris=" + match.id
    headers = {
                'Content-Type': "application/json",
                'Accept': "application/json",
                'Authorization': "Bearer " + auth['access_token'],
                'cache-control': "no-cache",
              }
    response = requests.request("POST", url, data="",
                                            headers=headers,
                                            params="")
    print(response.text)
    # delete the track from the dropbox