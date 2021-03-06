import os
import mutagen

"""
Uses mutagen to read (and maybe write in the future) audiofile tags in a more easy way.

".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac", ".m4a"
"""


class EasyTag(object):
    def __init__(self, path):
        self.ext = os.path.splitext(path)[1].lower()
        try:
            self.metadata = mutagen.File(path)
        except KeyError:
            self.metadata = None

    def getattribute(self, attribute):
        if self.metadata is None:
            return None
        for attr in attribute:
            try:
                if self.ext == ".mp3":
                    return self.metadata[attr].text[0]
                if self.ext == ".wma":
                    return str(self.metadata[attr][0])
                return self.metadata[attr][0]
            except KeyError:
                continue
        return None

    def getartist(self):
        return self.getattribute(["ARTIST", "©ART", "TPE1", "IART", "Author", "WM/AlbumArtist"])

    def gettitle(self):
        return self.getattribute(["TITLE", "©nam", "TIT2", "INAM", "Title"])

    def getalbum(self):
        return self.getattribute(["ALBUM", "©alb", "TALB", "IPRD", "WM/AlbumTitle"])

    def getyear(self):
        return self.getattribute(["DATE", "TDRC", "ICRD", "WM/Year"])

    def getgenre(self):
        return self.getattribute(["GENRE", "TCON", "IGNR", "WM/Genre"])

    def gettracknr(self):
        return self.getattribute(["TRCK", "WM/TrackNumber"])

    def getbitrate(self):
        try:
            return self.metadata.info.bitrate
        except AttributeError:
            return None

    def getlength(self):
        try:
            return self.metadata.info.length
        except AttributeError:
            return None
