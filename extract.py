import os
from logger import *
import shutil

def root():
    return "music/"

def dropbox():
    return "dropbox/"

def quarantine():
    return "quarantine/"

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
        logger.error('Error Reading Files: ' + ex)

def move(source, destination):
    """
        Move a file to another folder
    """

    try:
        shutil.move(source, destination)
        logger.info('Moved: [' + source + '] to [' + destination + ']')
    except Exception as ex:
        logger.error('Error moving file from: [{source}] to [{destination}] | {ex}'.format(source, destination, ex))

def delete(source):
    """
        Delete a file from a given folder
    """
    try:
        os.remove(source)
        logger.info('Deleted: [' + source +']')
    except Exception as ex:
        logger.error('Error deleting file from [{source}] | {ex}'.format(source, ex))

def match(track_obj, search_responses):
    return None
            