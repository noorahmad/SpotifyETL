class Track:
    """
        song="", artist="", album="", filename="", filepath=""
        Model for songs with album, artist, song name, filename, filepath
        File name is stored to extract song name and artist
        File path is stored to potentially extract the album
        Album can be used to verify song from Spotify Search API call
    """
    def __init__(self, song="", artist="", album="", filename="", filepath=""):
        self.song = song
        self.artist = artist,
        self.album = album,
        self.filename = filename
        self.filepath = filepath