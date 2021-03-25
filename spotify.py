import requests
import json

class spotify:
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

# read authentication code from text file
def read_auth_code():
    auth_code = open('auth_code.txt', 'r')
    return auth_code.read()

# authenticate with spotify etl and return response
def authenticate():
    auth_response = requests.request("POST", spotify.auth_url(), data=spotify.grant_type(), headers=spotify.headers())
    return json.loads(auth_response.text)
