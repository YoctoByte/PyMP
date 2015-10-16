from pydub import AudioSegment


class ExtendedAudioSegment(AudioSegment):

    def get_chunk(self, chunk_index, chunk):
        frame_start = chunk_index * chunk * self.frame_width
        frame_end = frame_start + self.frame_width * (chunk - 1)
        return self._data[frame_start:frame_end]