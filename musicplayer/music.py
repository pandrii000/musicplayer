from time import sleep
import os
import threading
import pyaudio
import datetime
from pydub import AudioSegment
from pydub.utils import make_chunks
import re


# Artist - Title .mp3/.wav 
SONG_PATTERN = r'([^\-]+)\-([^\-]+)\.(mp3|wav)'
# general music pattern
MUSIC_PATTERN = r'.+\.(mp3|wav)'


class PlaylistElement(dict):
    def __init__(self, filepath):
        super(PlaylistElement, self).__init__()
        self['filepath'] = filepath
        self['filename'] = filepath.split(os.path.sep)[-1]
        m = re.match(SONG_PATTERN, self['filename'])
        if m:
            self['artist'] = m.group(1).strip()
            self['title'] = m.group(2).strip()
            self['format'] = m.group(3).strip()


class Playlist:
    def __init__(self, name='Default'):
        self.name = name
        self.songs = []
        self.index = -1
        self.modified_date = datetime.datetime.now()

    def current(self):
        return self.songs[self.index]

    def next(self):
        self.index += 1
        return self.songs[self.index]

    def sync_with_directory(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if re.match(MUSIC_PATTERN, filename):
                    filepath = os.path.join(root, filename)
                    element = PlaylistElement(filepath)
                    self.songs.append(element)


class MusicPlayer:
    def __init__(self):
        self.playlist = Playlist()
        self.player = pyaudio.PyAudio()
        self.playing = False

        self.volume = 100
        self.playing_song = None
        self.time = 0
        self.song_duration = 0

    def play(self):
        if not self.playing:
            self.playing = True
            t = threading.Thread(target=self._play)
            t.start()

    def _play(self):
        while self.playing:
            try:
                self.playing_song = self.playlist.next()
            except IndexError:
                self.playing = False
                break

            sound = AudioSegment.from_file(self.playing_song['filepath'])
            stream = self.player.open(format=self.player.get_format_from_width(sound.sample_width),
                                channels=sound.channels,
                                rate=sound.frame_rate,
                                output=True)

            self.time = 0
            self.song_duration = sound.duration_seconds
            playchunk = sound[self.time*1000.0:(self.time+self.song_duration) * 1000.0] - (60 - (60 * (self.volume/100.0)))
            # playchunk = sound[self.time*1000.0:(self.time+self.song_duration) * 1000.0] - (60 - (60 * (self.volume/100.0)))
            millisecondchunk = 50 / 1000.0

            for chunks in make_chunks(playchunk, millisecondchunk*1000):
                self.time += millisecondchunk
                stream.write(chunks._data)
                if not self.playing:
                    break
                if self.time >= self.song_duration:
                    break

    def stop(self):
        """Stop playback."""
        self.playing = False

    def set_volume(self, value):
        """from 0 to 100."""
        self.volume = value


def stop_playlist(playlist, time):
    sleep(time)
    playlist.stop()


def test1():
    playlist = Playlist()
    playlist.sync_with_directory('./')
    playlist.songs.sort(key=lambda el: el['filename'])

    player = MusicPlayer()
    player.playlist = playlist
    player.play()
    
    sleep(1)
    player.set_volume(80)
    
    # while player.playing:
        # print(f"File: {player.playing_song['filename']} Time: {player.time} / {player.song_duration} Volume: {player.volume}")


if __name__ == '__main__':
    test1()    
    # sleep(2)
    # sleep(2)
    # sleep(2)
    # player.stop()


