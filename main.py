from spotify import *
from logger import *
from models import track
from extract import *
from transform import *

song_files = read_all_files('Music-Test')
for file in song_files:
    # parse song into track object
    track_obj = transform(file)
    
    # something went wrong with this file and it SHOULD be quaratined to review later
    if (track_obj == None):
        continue

    # move it to the dropbox
    move(root() + track_obj.filepath, "dropbox")

    # use the track object to create a request obj


    # use request obj to search for the song in spotify

    # if we get an OKAY response look through the object for the song

    # if we don't get an okay response, quarantine the track

    # if we do get an okay response but can't find the song in the response, quarantine the track

    # if we are able to find the song save the ID

    # use the response ID to save the song to spotify

    # delete the track from the dropbox