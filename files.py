import os
from easytag import EasyTag

SUPPORTED_EXTENSIONS = [".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac", ".m4a"]


class Files(object):
    def __init__(self, path):
        self._files = []
        self.scan_dir(path)
        self.path = path

    def __iter__(self):
        return iter(self._files)

    def scan_dir(self, path):
        metadata = {}
        for item in os.listdir(path):
            if is_supported(item):
                metadata["path"] = (path + "/" + item)
                tag = EasyTag(metadata["path"])
                metadata["ext"] = os.path.splitext(metadata["path"])[1]
                metadata["title"] = tag.gettitle()
                metadata["artist"] = tag.getartist()
                metadata["album"] = tag.getalbum()
                metadata["year"] = tag.getyear()
                metadata["genre"] = tag.getgenre()
                metadata["tracknr"] = tag.gettracknr()
                metadata["bitrate"] = tag.getbitrate()
                metadata["length"] = tag.getlength()
                self._files.append(dict(metadata))
            elif os.path.isdir(path + "/" + item):
                self.scan_dir(path + "/" + item)

    def remove_nonempty_dir(self, path):
        for item in os.listdir(path):
            try:
                self.remove_nonempty_dir(path + "/" + item)
            except:
                pass
        try:
            os.remove(path)
        except OSError:
            os.rmdir(path)

    def remove_empty_dirs(self, path):
        for item in os.listdir(path):
            try:
                self.remove_empty_dirs(path + "/" + item)
            except:
                pass

        if os.path.basename(path) == ".mediaartlocal":
            self.remove_nonempty_dir(path)

        try:
            os.rmdir(path)
        except OSError:
            pass

    def reorder(self):
        for metadata in self._files:
            artist = metadata["artist"]
            album = metadata["album"]
            title = metadata["title"]
            print(metadata["path"])
            tag = EasyTag(metadata["path"])
            print(tag.metadata)
            if artist is not None:
                artist = artist.replace("/", " ")
            if album is not None:
                album = album.replace("/", " ")
            if title is not None:
                title = title.replace("/", " ")

            if artist is not None:
                new_path = self.path + "/" + artist
                try:
                    os.makedirs(self.path + "/" + artist)
                except OSError:
                    pass
                if album is not None:
                    new_path += "/" + album
                    try:
                        os.makedirs(self.path + "/" + artist + "/" + album)
                    except OSError:
                        pass
                if title is not None:
                    new_path += "/" + artist + " - " + title + metadata["ext"]
                else:
                    new_path += "/" + os.path.basename(metadata["path"])

            else:
                new_path = self.path + "/" + os.path.basename(metadata["path"])

            if metadata["path"] != new_path:
                os.replace(metadata["path"], new_path)
                metadata["path"] = new_path
        self.remove_empty_dirs(self.path)


def is_supported(file):
    if os.path.splitext(file)[1] in SUPPORTED_EXTENSIONS:
        return True
