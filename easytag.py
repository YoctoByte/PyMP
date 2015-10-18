import os
import mutagen

"""
Uses mutagen to read (and maybe write in the future) audiofile tags in a more easy way.

".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac", ".m4a"
"""

class easytag(object):
    def __init__(self, path):
        self.ext = os.path.splitext(path)[1].lower()
        try:
            self.metadata = mutagen.File(path)
        except:
            self.metadata = None

    def getattribute(self, attribute):
        for attr in attribute:
            try:
                if self.ext == ".mp3":
                    return self.metadata[attr].text[0]
                else:
                    return self.metadata[attr][0]
            except:
                continue
        return None

    def getartist(self):
        return self.getattribute(["ARTIST", "©ART", "TPE1", "IART"])

    def gettitle(self):
        return self.getattribute(["TITLE", "©nam", "TIT2", "INAM"])

    def getalbum(self):
        return self.getattribute(["ALBUM", "©alb", "TALB", "IPRD"])

    def getyear(self):
        return self.getattribute(["DATE", "TDRC", "ICRD"])

    def getgenre(self):
        return self.getattribute(["GENRE", "TCON", "IGNR"])

    def gettracknr(self):
        return self.getattribute(["TRCK"])
