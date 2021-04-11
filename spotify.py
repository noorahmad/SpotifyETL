import json

import requests

from extract import move
from logger import logger
from transform import dropbox, parse_search_response


class spotify_req:
    """
        spotify request and response methods
    """
    class auth_request:
        def auth_url(self):
            return 'https://accounts.spotify.com/api/token'
        def grant_type(self):
            return 'grant_type=client_credentials'
        def headers(self):
            return {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'Authorization': 'Basic ' + read_auth_code()
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
                logger.logging.error('Couldnt find song in spotify: [' + song_query + ']')

            return search_obj_arr

        except Exception as ex:
            logger.logging.error('Error searching in Spotify for [' + song_query + '] | ' + str(ex))


# read authentication code from text file
def read_auth_code():
    auth_code = open('auth_code.txt', 'r')
    return auth_code.read()

# authenticate with spotify api and return response
def authenticate():
    try:
        auth_response = requests.request("POST", spotify_req.auth_request.auth_url(""), 
                                                 data=spotify_req.auth_request.grant_type(""), 
                                                 headers=spotify_req.auth_request.headers(""))
        logger.logging.info('Successfully authenticated with Spotify:' + auth_response.text)
        return json.loads(auth_response.text)
    except Exception as ex:
        logger.logging.error('Error authenticating with Spotify: ' + ex)

