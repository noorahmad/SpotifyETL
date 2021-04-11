import os
import shutil

from fuzzywuzzy import fuzz, process

from logger import logger


def read_all_files(filepath):
    """
        Reads files of the given file path and return in an array
    """

    file_list = []
    try:
        for root, dirs, files, in os.walk(filepath):
            for file in files:
                with open(os.path.join(root, file), "r") as auto:
                    file_list.append(auto.name.split('\\')[1:])
        logger.info('Total songs read: ' + str(len(file_list)))
        return file_list
    except Exception as ex:
        logger.error('Error Reading Files: ' + str(ex))

def move(source, destination):
    """
        Move a file to another folder
    """
    try:
        shutil.move(source, destination)
        logger.info('Moved: [' + source + '] to [' + destination + ']')
    except Exception as ex:
        logger.error('Error moving file from: [{source}] to [{destination}] | {ex}'.format(source=source, desination=destination, ex=str(ex)))

def delete(source):
    """
        Delete a file from a given folder
    """
    try:
        os.remove(source)
        logger.info('Deleted: [' + source +']')
    except Exception as ex:
        logger.error('Error deleting file from [{source}] | {ex}'.format(source=source, ex=ex))

def find_match(track_obj, search_responses):
    matching_index = 0
    song_ratio = 0
    artist_ratio = 0
    index = 0

    if (len(search_responses) == 1):
        logger.info('Source: [{source_track} - {source_artist}], Match: [{match_track} - {match_artist}]'.format(source_track=track_obj.song,
                                                                                                                 source_artist=track_obj.artist,
                                                                                                                 match_track=search_responses[0].song,
                                                                                                                 match_artist=search_responses[0].artist))
        return search_responses[0]

    for resp in search_responses:
        this_song_ratio = fuzz.partial_ratio(track_obj.song, resp.song)
        this_artist_ratio = fuzz.partial_ratio(track_obj.artist, resp.artist)

        if (this_song_ratio >= song_ratio and this_artist_ratio >= artist_ratio):
            song_ratio = this_song_ratio
            artist_ratio = this_artist_ratio
            matching_index = index

        index += 1

    match = search_responses[matching_index]

    logger.info('Source: [{source_track} - {source_artist}], Match: [{match_track} - {match_artist}]'.format(source_track=track_obj.song,
                                                                                                             source_artist=track_obj.artist,
                                                                                                             match_track=match.song,
                                                                                                             match_artist=match.artist))
    return match
