from ExtendedAudioSegment import ExtendedAudioSegment as AudioSegment
# from pydub import AudioSegment
import pyaudio
import time
import os
import random
import threading as thr
from easytag import easytag


class musicplayer(object):

    def __init__(self):
        self.pause = False
        self.next = False
        self.pause_at_end = False
        self.stop = False
        self.reverse = False
        self.speed = 1
        self.directory = os.environ['HOME'] + "/Music"
        self.files = self.read_files(self.directory)
        self.queue_music = []
        self.init_play_queue()
        self._load_next()

    def scan_files(self):
        self.files = self.read_files(self.directory)
        return self.files

    def init_play_queue(self):
        self.queue_music = self.files
        random.shuffle(self.queue_music)

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
        thr_play = thr.Thread(target=self._play_next_song)
        thr_load = thr.Thread(target=self._load_next())
        thr_play.start()
        thr_load.start()
        thr_play.join()
        thr_load.join()
        if self.pause_at_end:
            self.pause = True
            self.pause_at_end = False

    def _load_next(self):
        while not self.queue_music:
            time.sleep(0.05)
        song_next = self.queue_music.pop()
        self.song_next = AudioSegment.from_file(song_next)
        self.song_next.name = song_next

    def _play_next_song(self):
        song = self.song_next

        if self.speed > 0:
            chunk_index = 0
            speed = self.speed
            data = song.readframes(chunk_index)
        else:
            chunk_index = int(len(song._data)/1024/song.frame_width)
            speed = -self.speed
            data = song.readframesreverse(chunk_index)

        print(self.return_name_string(song.name))
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

    def is_supported(self, file):
        e = os.path.splitext(file)[1]
        if e in [".mp3", ".mp4", ".wav", ".ogg", ".wma", ".aiff", ".flv", ".flac", "m4a"]:
            return True

    def read_files(self, dire):
        files = []
        for file in os.listdir(dire):
            if self.is_supported(file):
                if files is not None:
                    files.append(dire + "/" + file)
            else:
                try:
                    files += self.read_files(dire + '/' + file)
                except:
                    pass
        return files

    def search_music(self, search):
        songs_found = 0
        self.queue_music = []
        for file in self.files:
            if search.lower() in file.lower():
                print(file)
                self.queue_music.append(file)
                songs_found += 1
        print(songs_found, " songs found")

    def return_name_string(self, path):
        tag = easytag(path)
        title = tag.gettitle()
        artist = tag.getartist()
        if title is not None and artist is not None:
            return artist + " - " + title
        else:
            return "filename: " + os.path.splitext(os.path.basename(path))[0]
