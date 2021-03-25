import os

# read files of the given file path and return in an array
def read_all_files(filepath):
    file_list = []
    for root, dirs, files, in os.walk(filepath):
        for file in files:
            file_list.append(file)
    return file_list