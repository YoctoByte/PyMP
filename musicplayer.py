from ExtendedAudioSegment import ExtendedAudioSegment as AudioSegment
import pyaudio
import time
import os
import random
import threading as thr
from files import Files

"""
self.queue is a list of metadata dictionaries. The dictionaries contain an id, the pathname and data like
artist and title.
"""
SLEEP_TIME = 0.05


class MusicPlayer(object):

    def __init__(self):
        self.pause = False
        self.next = False
        self.stop = False
        self.pause_at_end = False
        self.reverse = False
        # self.ready = True
        self.speed = 1
        self.directory = os.environ['HOME'] + "/testmusic"
        self._files = Files(self.directory)
        self.queue = list(self._files)
        random.shuffle(self.queue)
        self._load_next()

    def toggle_pause(self):
        self.pause = not self.pause
        return self.pause

    def toggle_reverse(self):
        self.speed = -self.speed
        return self.speed < 0

    def next_song(self):
        self.next = True
        self.pause = False

    def pause_at_end_of_song(self):
        self.pause_at_end = True

    def set_speed(self, play_speed):
        self.speed = play_speed

    def play_song(self):
        # self.ready = False
        thr_load = thr.Thread(target=self._load_next())
        thr_play = thr.Thread(target=self._play_next_song)

        thr_play.start()
        thr_load.start()

        thr_load.join()
        thr_play.join()

        if self.pause_at_end:
            self.pause = True
            self.pause_at_end = False

    def _load_next(self):
        while not self.queue:
            time.sleep(SLEEP_TIME)
        # while not self.ready:
        #    time.sleep(SLEEP_TIME)
        metadata = self.queue.pop()
        self.nextsong = AudioSegment.from_file(metadata["path"])
        self.nextsong.metadata = metadata
        print(metadata)

    def _play_next_song(self):
        print("play next song")
        song = self.nextsong
        # self.ready = True

        if self.speed > 0:
            chunk_index = 0
            speed = self.speed
            data = song.readframes(chunk_index)
        else:
            chunk_index = int(len(song._data)/1024/song.frame_width)
            speed = -self.speed
            data = song.readframesreverse(chunk_index)

        print(self.namestring(song.metadata))
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(song.sample_width),
                        channels=song.channels,
                        rate=int(song.frame_rate*speed),
                        output=True)

        while data != '':
            if self.next:
                stream.close()
                p.terminate()
                self.next = False
                return
            if not self.pause:
                stream.write(data)
                if self.speed > 0:
                    data = song.readframes(chunk_index)
                    chunk_index += 1
                else:
                    data = song.readframesreverse(chunk_index)
                    chunk_index -= 1
            else:
                time.sleep(SLEEP_TIME)
        stream.close()
        p.terminate()

    def search_music(self, searchterm):
        songs_found = 0
        self.queue = []
        for file in self._files:
            if searchterm.lower() in file["path"].lower():
                print(self.namestring(file))
                self.queue.append(file)
                songs_found += 1
        print(songs_found, " songs found")

    def reorder(self):
        self._files.reorder()

    def namestring(self, metadata):
        title = metadata["title"]
        artist = metadata["artist"]
        length = metadata["length"]
        str_length = ""
        if length is not None:
            str_length = " (" + str("%.1f" % metadata["length"]) + " seconds)"
        if title is not None and artist is not None:
            return artist + " - " + title + str_length
        else:
            return "filename: " + os.path.splitext(os.path.basename(metadata["path"]))[0] + str_length
