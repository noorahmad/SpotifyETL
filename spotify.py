import requests
import json

class spotify:
    """
        put spotify request and response methods in here
    """
    def auth_request():
        def auth_url():
            return 'https://accounts.spotify.com/api/token'
        def grant_type():
            return 'grant_type=client_credentials'
        def headers():
            return {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'Authorization': 'Basic ' + read_auth_code()
            } 

    # search obj
    def search(song_name, artist):
        url = "https://api.spotify.com/v1/search"
        query_string = { 
                        "q": "{song_name} - {artist}".format(song_name, artist), 
                        "type": "track" 
                       }

# read authentication code from text file
def read_auth_code():
    auth_code = open('auth_code.txt', 'r')
    return auth_code.read()

# authenticate with spotify api and return response
def authenticate():
    auth_response = requests.request("POST", spotify.auth_request().auth_url(), 
                                             data=spotify.auth_request().grant_type(), 
                                             headers=spotify.auth_request().headers())
    return json.loads(auth_response.text)
