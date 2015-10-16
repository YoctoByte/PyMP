from pydub import AudioSegment


class ExtendedAudioSegment(AudioSegment):

    def readframes(self, chunk_index, chunk):
        frame_start = chunk_index * chunk * self.frame_width
        frame_end = frame_start + self.frame_width * (chunk - 1)
        if frame_start < len(self._data):
            return self._data[frame_start:frame_end]
        else:
            return ''
