# SpotifyETL

## Add logging!

### How it will work
* Create file list
* Iterate through the list
* Take file and turn it into class
* Use class to create request object
* Use request object to search for song using Spotify API
  * If we are not able to find the song, move the file into a quarantine folder
* Use the response ID from the API call to add the song to Spotify
* Delete song file

## TODO
1. Support for playlists - maybe by genre?
