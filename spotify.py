import requests
import json

class spotify_settings:
    def auth_url():
        return 'https://accounts.spotify.com/api/token'
    def payload():
        return 'grant_type=client_credentials'
    def headers():
        return {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'Authorization': 'Basic ' + read_auth_code()
        }

def read_auth_code():
    auth_code = open('auth_code.txt', 'r')
    return auth_code.read()

def authenticate():
    auth_response = requests.request("POST", spotify_settings.auth_url(), data=spotify_settings.payload(), headers=spotify_settings.headers())
    return json.loads(auth_response.text)
