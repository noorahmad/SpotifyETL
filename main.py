from extract import find_match, read_all_files, move, delete
from spotify import authenticate, spotify_req
from transform import transform, root, dropbox
from bottle import route, run, request
import spotipy
from spotipy import oauth2
import json

##############################################################

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
PLAYLIST_ID = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:' + PORT_NUMBER
SCOPE = 'playlist-modify-private playlist-modify-public'
CACHE = '.spotipyoauthcache'

# uris to add to spotify
URIS = []  

ACCESS_TOKEN = ""


##############################################################

def run_workflow(ACCESS_TOKEN):
    # retrieve all of the song files
    song_files = read_all_files('music')

    # authenticate with spotify
    auth = authenticate(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    

    for file in song_files:
        # parse song into track object
        track_obj = transform(file)

        is_last_song = song_files[len(song_files) - 1] == file
    
        skip = none_check(track_obj, is_last_song)

        if skip == True:
            continue

        # move it to the dropbox
        move(root() + track_obj.filepath, "dropbox")

        # use request obj to search for the song in spotify
        response_items = spotify_req.search("",track_obj, auth['access_token'])

        skip = none_check(track_obj, is_last_song)
        if skip == True:
            continue

        # take parsed response find best match
        match = find_match(track_obj, response_items)

        URIS.append("spotify:track:" + match.id)

        # delete the track from the dropbox
        delete(dropbox() + track_obj.filepath)

        if (len(URIS) == 99 or is_last_song == True):
            spotify_req.add_to_spotify(URIS, PLAYLIST_ID, ACCESS_TOKEN)
            URIS = []

##############################################################

def none_check(obj, bool):
    skip = False

    if (obj == None and bool != True):
        return True
    elif (obj == None and bool == True):
        spotify_req.add_to_spotify(URIS, PLAYLIST_ID, ACCESS_TOKEN)
        URIS = []
        return True
    else:
        return False


sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

@route('/')

# TODO: This needs to be moved and logged

def index():

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        ACCESS_TOKEN = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != ('http://localhost:' + str(PORT_NUMBER) + '/'):
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            ACCESS_TOKEN = token_info['access_token']

    if access_token != "":
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(ACCESS_TOKEN)
        results = sp.current_user()
        run_workflow(ACCESS_TOKEN)

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='', port=PORT_NUMBER)
