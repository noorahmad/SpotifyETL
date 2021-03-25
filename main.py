from spotify import *
from logger import *
from models import track
from extract import *
from transform import *

song_files = read_all_files('Music-Test')
for file in song_files:
    transform(file)