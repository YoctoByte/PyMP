import os

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC

class easytag(object):
    def __init__(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".mp3":
            self.audio = MP3(path)
            print("mp3 file")
            print(self.audio.tags)
        elif ext == ".mp4":
            self.audio = MP4(path)
            print("mp4 file")
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
        try:
            print(self.audio.tags["TPE1"].text[0])
            return self.audio.tags["TPE1"].text[0]
        except:
            return None

    def gettitle(self):
        try:
            print(self.audio["TIT2"].text[0])
            return self.audio["TIT2"].text[0]
        except:
            return None

# ".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac"
