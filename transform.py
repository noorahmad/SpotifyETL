from models import track
from logger import *
import reprlib

def transform(song_file):
    "When given a filename, transform it into a Track object"
    # take this path when we have a song with no album
    if (len(song_file) == 1):
        # one dash means the song is split between song and artist
        if (song_file[0].count('-') == 1):
            # 90% percent of the time the song is split like so (artist) - (song)
            file_split = song_file[0].split("-")
            track_obj = track.Track(clean(file_split[1]),
                                    "",
                                    "",
                                    song_file[0], 
                                    song_file[0])
            
            # TODO: Python is really fucking stupid and this is only a temporary solution
            track_obj.artist = file_split[0]
            
        # if there's more than one dash then deal with it later
        else:
            logger.info('Too many dashes -- ' + song_file[0])


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
