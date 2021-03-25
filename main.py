from spotify import *
from extract import *

files = read_all_files('Music-Test')
for file in files:
    print(file)