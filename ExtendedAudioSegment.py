from pydub import AudioSegment


class ExtendedAudioSegment(AudioSegment):

    def readframes(self, chunk_index, chunk=1024):
        frame_start = chunk_index * chunk * self.frame_width
        frame_end = frame_start + self.frame_width * (chunk - 1)
        if frame_start < len(self._data):
            return self._data[frame_start:frame_end]
        else:
            return ''

    def readframesreverse(self, chunk_index, chunk=1024):
        chunk_width = chunk * self.frame_width
        frame_start = chunk_index * chunk * self.frame_width
        frame_end = frame_start + self.frame_width * (chunk - 1)
        if frame_start < len(self._data) and frame_start >= 0:
            data = self._data[frame_start: frame_end]
            revereddata = data[chunk_width - self.frame_width: chunk_width]
            for frame in range(chunk - 1):
                revereddata += data[(chunk - frame - 1) * self.frame_width: (chunk - frame) * self.frame_width]
            return revereddata
        else:
            return ''
