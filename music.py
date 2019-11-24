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
                    print(root, dirs, files)
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
        return self.elements[index ]


# class MusicPlayer:
#     def __init__(self, volume=100):
#         self.playlist = Playlist()
#         self.player = pyaudio.PyAudio()

#         self.is_playing = Event()
#         self.is_playing.clear()

#         self.time_played = 0
#         self.time_length = 0
#         self.volume = volume

#         self._plating_thread = Thread(target=self._play)
#         self._plating_thread.start()

#     def stop(self):
#         self.time_played = 0
#         self.is_playing.clear()

#     def pause(self):
#         self.is_playing.clear()
    
#     def play(self):
#         self.is_playing.set()

#     def _play(self):
#         # wait for is_playing state
#         self.is_playing.wait()

#         while self.playlist.has_next():
#             # wait for is_playing state
#             self.is_playing.wait()

#             # get next song in playlist
#             playing_song = self.playlist.get_next()

#             # read sound data
#             sound = AudioSegment.from_file(playing_song['filepath'])

#             # open stream
#             stream = self.player.open(
#                 format=self.player.get_format_from_width(sound.sample_width),
#                 channels=sound.channels, 
#                 rate=sound.frame_rate,
#                 output=True
#                 )

#             # length of song in seconds for one writing to stream
#             chunk_length = 50 / 1000

#             # playing song
#             # self.time_length = self.sound.duration_seconds
#             # while self.time_played < self.time_length:
#             #     self.playing.wait()
#             #     # _data = sound[]
#             #     self.stream.write(chunk._data)
#             #     self.time += chunk_length / 1000

#             stream.stop_stream()
#             stream.close()
#             # player.terminate()

#     def set_volume(self, value):
#         """from 0 to 100."""
#         self.volume = value


# def stop_playlist(playlist, time):
#     sleep(time)
#     playlist.stop()


# def test1():
#     player = MusicPlayer()

#     playlist = Playlist()
#     playlist.sync_with_directory('./')

#     player.playlist = playlist
#     player.play()

#     # while player.playing:
#     # sleep(1)
#     # player.set_volume(80)
#     # print(f"File: {player.playing_song['filename']} Time: {player.time} / {player.song_duration} Volume: {player.volume}")


# if __name__ == '__main__':
#     test1()
#     # sleep(2)
#     # sleep(2)
#     # sleep(2)
#     # player.stop()

class MusicPlayer:
    def __init__(self, volume=100):
        self.player = pyaudio.PyAudio()

        self.is_playing = Event()
        self.is_playing.set()  

        self.repeat = False
    
    def play(self, filepath):
        self.is_playing.set()

        thread = Thread(target=self._play, args=(filepath,))
        thread.start()

    def _play(self, filepath):        
        sound = AudioSegment.from_file(filepath)
        player = pyaudio.PyAudio()
    
        stream = player.open(format = player.get_format_from_width(sound.sample_width),
            channels = sound.channels,
            rate = sound.frame_rate,
            output = True)

        start = 0
        length = sound.duration_seconds
        volume = 100.0
        playchunk = sound[start*1000.0:(start+length)*1000.0] - (60 - (60 * (volume/100.0)))
        millisecondchunk = 50 / 1000.0
        
        time = start
        for chunks in make_chunks(playchunk, millisecondchunk*1000):
            self.is_playing.wait()

            time += millisecondchunk
            stream.write(chunks._data)
            if time >= start+length:
                break

        stream.close()
        player.terminate()

    def pause(self):
        self.is_playing.clear()

    def stop(self):
        self.is_playing.clear()

    def set_volume(self, value):
        """from 0 to 100."""
        self.volume = value
