import json

import requests
import base64

from extract import move
from logger import logger
from transform import dropbox, parse_search_response


class spotify_req:
    """
        spotify request and response methods
    """
    class auth_request:
        def auth_url():
            return 'https://accounts.spotify.com/api/token'
        def grant_type():
            return 'grant_type=client_credentials'
        def headers(auth_code):
            return {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'Authorization': 'Basic ' + auth_code
            } 

    def search(self, track_obj, access_token):
        """
            song_name="",   artist="",  access_token=""
            Searches for a song using the Spotify API and parses the response
        """
        try:
            # use the track object to create a request obj
            url = "https://api.spotify.com/v1/search"
            song_query = track_obj.song.strip() + ' - ' + track_obj.artist.strip()
            query_string = { 
                            "q": song_query, 
                            "type": "track" 
                           }
            payload=""
            headers = {
                        'Content-Type': "application/json",
                        'Accept': "application/json",
                        'Authorization': "Bearer " + access_token,
                        'cache-control': "no-cache",
                      }
            response = requests.request("GET", url, data=payload,
                                                    headers=headers,
                                                    params=query_string)

            # parse the response
            search_obj_arr = parse_search_response(response.text)
            if (search_obj_arr == None):
                move(dropbox() + track_obj.filepath, "quarantine")
                logger.error('Couldnt find song in spotify: [' + song_query + ']')
                logger.error(response.text)
            return search_obj_arr

        except Exception as ex:
            logger.error('Error searching in Spotify for [' + song_query + '] | ' + str(ex))
    
    def add_to_spotify(uris, playlist_id, access_token):
        # use the response ID to save the song to spotify
        try:
            url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks?"

            payload = json.dumps({'uris':uris})

            headers = {
                        'Content-Type': "application/json",
                        'Accept': "application/json",
                        'Authorization': "Bearer " + access_token,
                        'cache-control': "no-cache",
                        }
            response = requests.request("POST", url, data=payload,
                                                    headers=headers,
                                                    params="")
            print(response.text)
            logger.info('Sending ' + str(len(uris)) + ' songs to spotify')
        except Exception as ex:
            logger.error('Error adding to spotify | ' + str(ex))


# read authentication code from text file
def read_auth_code(id, secret):
    return base64.b64encode(id + ':' + secret)

# authenticate with spotify api and return response
def authenticate(id, secret):

    auth_code = read_auth_code(id, secret)

    try:
        auth_response = requests.request("POST", spotify_req.auth_request.auth_url(), 
                                                 data=spotify_req.auth_request.grant_type(), 
                                                 headers=spotify_req.auth_request.headers(auth_code))
        logger.info('Successfully authenticated with Spotify:' + auth_response.text)
        return json.loads(auth_response.text)
    except Exception as ex:
        logger.error('Error authenticating with Spotify: ' + ex)

