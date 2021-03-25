import os
"""
    TODO: Add directory to the file array in case we need to grab album 
          in order to verify correct song is returned from spotify
          Can also be extended so that songs may be added to specific playlists
"""
def read_all_files(filepath):
    "Reads files of the given file path and return in an array"
    file_list = []
    for root, dirs, files, in os.walk(filepath):
        for file in files:
            file_list.append(file)
    return file_list