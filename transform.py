import json
import shutil

from extract import move
from logger import logger
from models import track


def root():
    return "music/"

def dropbox():
    return "dropbox/"

def quarantine():
    return "quarantine/"


class search_obj_response:
        """
            the parsed response object from searching in spotify
            song="",    artist="",  album="",   id=""
        """
        def __init__(self, song="", artist="", album="", id=""):
            self.song = song
            self.artist = artist,
            self.album = album,
            self.id = id

def transform(song_file):
    """
        When given a filename, transform it into a Track object
    """

    # take this path when we have a song with no album
    if (len(song_file) == 1):
        file_split = parse_song_file(song_file[0])
        if (file_split != None):
            track_obj = track.Track(clean(file_split[1]),
                                    file_split[0],
                                    "",
                                    song_file[0], 
                                    song_file[0])
            # TODO: Python is really fucking stupid and this is only a temporary solution
            track_obj.artist = file_split[0]
            return track_obj
        else: 
            # Log and quarantine
            move(root() + song_file[0], "quarantine")
            logger.error("Couldn't parse the song: " + song_file[0])
            return None

    # this song came from a subfolder so it most likely has an album
    elif(len(song_file) == 2):
        file_split = parse_song_file(song_file[1])
        if (file_split != None):
            track_obj = track.Track(clean(file_split[1]),
                                    file_split[0],
                                    "",
                                    song_file[1], 
                                    song_file[0] + "/" + song_file[1])
            # TODO: Python is really fucking stupid and this is only a temporary solution
            track_obj.artist = file_split[0]
            return track_obj
        else: 
            # Log and quarantine
            move(root() + song_file[0] + "//" + song_file[1], "quarantine")
            logger.error("Couldn't parse the song: " + song_file[0])
            return None

    # too many subfolders, we will deal with these later
    else:
        move(root() + song_file[0], "quarantine")


def clean(that_part):
    """
        Clean that track up yo
    """

    # since shit could get lost in translation keep a copy of the file before
    before = that_part
    that_part = that_part.replace('[www.slider.kz]', '')
    that_part = that_part.replace('.mp3', '')
    that_part = that_part.replace('.wav', '')
    that_part = that_part.replace('myfreemp3.vip', '')

    logger.info("Before [{before}] - After [{after}]".format(before=before,after=that_part))
    return that_part

def parse_song_file(song_file):
    """
        90% percent of the time the song is split like so (artist) - (song)
        TODO: This should be extended to include edge cases
    """

    # one dash means the song is split between song and artist
    if (song_file.count('-') == 1):
        return song_file.split("-")
    else:
        return None

def parse_search_response(search_response):
    """
        Parse response from Spotify Search API call
    """
    search_obj_arr = []
    search_obj = json.loads(search_response)

    # api search returned no results
    if (search_obj['tracks']['total'] == 0):
        return None
    try:
        logger.info('Attempting to parse search response')
        items = search_obj['tracks']['items']
        for item in items:
            album=""
            if (item['album']['album_type'] != 'single'):
                album=item['album']['album_type']
            artist=item['artists'][0]['name']
            song=item['name']
            id=item['id']
            search_response_object = search_obj_response(song, "", album, id)
            search_response_object.artist = artist
            search_obj_arr.append(search_response_object)
        return search_obj_arr
    except Exception as ex:
        logger.error('Error parsing response: ' + ex)
