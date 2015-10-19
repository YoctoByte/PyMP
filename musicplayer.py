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


class MusicPlayer(object):

    def __init__(self):
        self.pause = False
        self.next = False
        self.stop = False
        self.pause_at_end = False
        self.reverse = False
        self.speed = 1
        self.directory = os.environ['HOME'] + "/Music"
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
        thr_load = thr.Thread(target=self._load_next())
        thr_play = thr.Thread(target=self._play_next_song)
        thr_load.start()
        thr_play.start()
        thr_load.join()
        thr_play.join()
        if self.pause_at_end:
            self.pause = True
            self.pause_at_end = False

    def _load_next(self):
        while not self.queue:
            time.sleep(0.05)
        metadata = self.queue.pop()
        self.nextsong = AudioSegment.from_file(metadata["path"])
        self.nextsong.metadata = metadata

    def _play_next_song(self):
        song = self.nextsong

        if self.speed > 0:
            chunk_index = 0
            speed = self.speed
            data = song.readframes(chunk_index)
        else:
            chunk_index = int(len(song._data)/1024/song.frame_width)
            speed = -self.speed
            data = song.readframesreverse(chunk_index)

        print(self.namestring(song.metadata))
        print("%.1f" % (len(song._data)/song.frame_width/song.frame_rate), "seconds")
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
                time.sleep(0.05)
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

    def namestring(self, metadata):
        title = metadata["title"]
        artist = metadata["artist"]
        if title is not None and artist is not None:
            return artist + " - " + title
        else:
            return "filename: " + os.path.splitext(os.path.basename(metadata["path"]))[0]
