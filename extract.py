import os
from logger import *

def read_all_files(filepath):
    "Reads files of the given file path and return in an array"
    file_list = []
    try:
        for root, dirs, files, in os.walk(filepath):
            for file in files:
                with open(os.path.join(root, file), "r") as auto:
                    file_list.append(auto.name.split('\\')[1:])
        logger.info('Total songs read: ' + str(len(file_list)))
        return file_list
    except Exception as ex:
        logger.error(ex)