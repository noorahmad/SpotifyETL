from models import track
from logger import *
from extract import *
import reprlib


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
            logger.info("Couldn't parse the song: " + song_file[0])
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
            logger.info("Couldn't parse the song: " + song_file[0])
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
    that_part = that_part.replace('(Original Mix)', '').replace('[www.slider.kz]', '')
    that_part = that_part.replace('Original Mix', '')
    that_part = that_part.replace('.mp3', '')
    that_part = that_part.replace('.wav', '')
    that_part = that_part.replace('myfreemp3.vip', '')

    logger.info("Before {before} - After {after}".format(before=before,after=that_part))
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

