import os
from easytag import EasyTag


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
                metadata["tracknr"] = tag.gettracknr
                self._files.append(dict(metadata))
            elif os.path.isdir(item):
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

    def reorder(self, files):
        for metadata in files:
            if metadata["artist"] is not None:
                try:
                    os.makedirs(self.path + "/" + metadata["artist"].replace("/", " "))
                except:
                    pass
                newpath = self.path + "/" + metadata["artist"].replace("/", " ")
                if metadata["album"] is not None:
                    newpath += "/" + metadata["album"]
                    try:
                        os.makedirs(self.path + "/" + metadata["artist"].replace("/", " ") + "/" + metadata["album"].replace("/", " "))
                    except:
                        pass
                if metadata["title"] is not None:
                    newpath += "/" + metadata["artist"].replace("/", " ") + " - " + metadata["title"].replace("/", " ") + metadata["ext"]
                else:
                    newpath += "/" + os.path.basename(metadata["path"])

            else:
                newpath = self.path + "/" + os.path.basename(metadata["path"])

            if metadata["path"] != newpath:
                os.replace(metadata["path"], newpath)
                metadata["path"] = newpath
        self.remove_empty_dirs(self.path)


def is_supported(file):
    if os.path.splitext(file)[1] in [".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac", ".m4a"]:
        return True
    else:
        return False
