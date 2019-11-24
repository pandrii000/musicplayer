from time import sleep
import os
from threading import Thread, Event
import pyaudio
import datetime
from pydub import AudioSegment
from pydub.utils import make_chunks
import re


# general music pattern
MUSIC_PATTERN = r'[^.]*\.(mp3|wav)'

# Artist - Title .mp3/.wav
SONG_PATTERN = r'([^\-]+)\-([^.]+)\.(mp3|wav)'


class PlaylistElement:
    def __init__(self, filepath):
        self._properties = {
            'filepath': '',
            'filename': '',
            'artist': '',
            'title': '',
            'format': ''
        }

        self._properties['filepath'] = filepath
        self._properties['filename'] = filepath.split(os.path.sep)[-1]

        m = re.match(SONG_PATTERN, self._properties['filename'])
        if m:
            self._properties['artist'] = m.group(1).strip()
            self._properties['title'] = m.group(2).strip()
            self._properties['format'] = m.group(3).strip()

    def get_properties(self):
        return self._properties

    def __getitem__(self, key):
        return self._properties[key]


class Playlist:
    def __init__(self, name='Default'):
        self.name = name
        self.elements = []
        self.index = -1
        self.modified_date = datetime.datetime.now()

    def add_file(self, filepath):
        element = PlaylistElement(filepath)
        self.elements.append(element)

    def add_from_directory(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if re.match(MUSIC_PATTERN, filename):
                    filepath = os.path.join(root, filename)
                    self.add_file(filepath)

    def current(self):
        return self.songs[self.index]

    def has_next(self):
        return self.index + 1 < len(self.elements)

    def get_next(self):
        self.index += 1
        return self.elements[self.index]

    def sort_by(self, category):
        self.elements.sort(key=lambda el: el[category].lower())

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, index):
        return self.elements[index]


# class MusicPlayer:
#     def __init__(self, volume=100):
#         self.player = None
#         self.stream = None
#         self.volume = volume
#         self.time = 0
#         self.length = 0

#         self.is_playing = Event()
#         self.is_playing.set()  

#         self.repeat = False

#     def play(self, filepath):
#         self.is_playing.set()

#         thread = Thread(target=self._play, args=(filepath,))
#         thread.start()

#     def _play(self, filepath):        
#         sound = AudioSegment.from_file(filepath)
#         self.player = pyaudio.PyAudio()
    
#         self.stream = self.player.open(format = self.player.get_format_from_width(sound.sample_width),
#             channels = sound.channels,
#             rate = sound.frame_rate,
#             output = True)

#         self.length = sound.duration_seconds
#         playchunk = sound[self.time*1000.0:(self.length)*1000.0]
#         millisecondchunk = 10 / 1000.0
        
#         for chunks in make_chunks(playchunk, millisecondchunk*1000):
#             self.is_playing.wait()

#             self.time += millisecondchunk
#             self.stream.write((chunks - (60 - (60 * (self.volume/100.0))))._data)
#             if self.time >= self.length:
#                 break

#         self.stream.close()
#         self.player.terminate()

#     def pause(self):
#         self.is_playing.clear()

#     def stop(self):
#         self.pause()
#         self.stream.close()
#         self.player.terminate()

#     def set_volume(self, value):
#         """from 0 to 100."""
#         self.volume = value

import pygame 

class MusicPlayer:
    def __init__(self, volume=100):
        pygame.mixer.init()
        self.volume = volume

    def play(self, filepath):
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

if __name__ == '__main__':
    filepath = 'In The End (Official Video) - Linkin Park.mp3'
    m = MusicPlayer()
    m.play(filepath)
    sleep(200)