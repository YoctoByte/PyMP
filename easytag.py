import os

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.m4a import M4A

"""
Uses mutagen to read (and maybe write in the future) audiofile tags in a more easy way.
"""

class easytag(object):
    def __init__(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".mp3":
            self.audio = MP3(path)
            print("mp3 file")
            print(self.audio.tags)
        elif ext in [".mp4", ".m4a"]:
            self.audio = MP4(path)
            print("mp4/m4a file")
            print(self.audio.tags)
        elif ext == ".flac":
            self.audio = FLAC(path)
            print("flac file")
            print(self.audio.tags)
        # if ext == "wav":
        #     from mutagen.wavpack import WavPack as mutagen
        # if ext == "ogg":
        #     from mutagen.ogg import OggFileType as mutagen
        self.ext = ext

    def getartist(self):
        if self.ext == ".flac":
            try:
                return self.audio["ARTIST"][0]
            except:
                return None
        elif self.ext == ".mp3":
            try:
                return self.audio["TPE1"].text[0]
            except:
                return None
        return None

    def gettitle(self):
        if self.ext == ".flac":
            try:
                return self.audio["TITLE"][0]
            except:
                return None
        elif self.ext == ".mp3":
            try:
                return self.audio["TIT2"].text[0]
            except:
                return None
        return None

# ".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac"
