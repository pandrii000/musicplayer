from time import sleep
import os
from threading import Thread, Event
import pyaudio
import datetime
from pydub import AudioSegment
from pydub.utils import make_chunks
import re
import json


# general music pattern
MUSIC_PATTERN = r'[^.]*\.(mp3|wav)'

# Artist - Title .mp3/.wav
SONG_PATTERN = r'([^\-]+)\-([^.]+)\.(mp3|wav)'


class PlaylistElement:
    def __init__(self, filepath=None):
        self._properties = {
            'filepath': '',
            'filename': '',
            'artist': '',
            'title': '',
            'format': ''
        }

        if filepath is not None:
            self._properties['filepath'] = filepath
            self._properties['filename'] = filepath.split(os.path.sep)[-1]
            self._properties['format'] = filepath.split('.')[-1]

            m = re.match(SONG_PATTERN, self._properties['filename'])
            if m:
                self._properties['artist'] = m.group(1).strip()
                self._properties['title'] = m.group(2).strip()

    def get_properties(self):
        return self._properties

    def set_properies(self, d):
        self._properties = d

    def __getitem__(self, key):
        return self._properties[key]


class Playlist:
    def __init__(self, name='Default'):
        self.name = name
        self.elements = []
        self.index = 0
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

    def remove(self, i):
        del self.elements[i]

    def current(self):
        return self.elements[self.index]

    def set_current(self, i):
        self.index = i

    def next(self):
        self.index += 1

    def previous(self):
        self.index -= 1

    def has_next(self):
        return self.index + 1 < len(self.elements)

    def has_previous(self):
        return self.index - 1 >= 0

    def finished(self):
        return self.index < 0 or self.index >= len(self.elements) 

    def sort_by(self, category):
        self.elements.sort(key=lambda el: el[category].lower())

    def to_json(self, filepath):
        dict_repr = {}
        dict_repr['name'] = self.name
        dict_repr['modified_date'] = self.modified_date.timestamp()
        dict_repr['elements'] = [element.get_properties() for element in self.elements]
        with open(filepath, 'w') as f:
            json.dump(dict_repr, f, indent=4)

    def from_json(self, filepath):
        with open(filepath, 'r') as f:
            dict_repr = json.load(f)
        self.name = dict_repr['name']
        self.modified_date = datetime.datetime.fromtimestamp(dict_repr['modified_date'])
        self.elements = []
        for element_properties in dict_repr['elements']:
            element = PlaylistElement()
            element.set_properies(element_properties)
            self.elements.append(element)


class MusicPlayer:
    def __init__(self, app):
        self.app = app

        self.is_playing = Event()
        self.is_playing.clear()

        self.play_thread = None

    def play(self):
        if self.play_thread is not None:
            self.stop()
        
        self.is_playing.set()
        self.play_thread = Thread(target=self._play, daemon=True)
        self.play_thread.start()

    def _play(self):
        while not self.app.playlist.finished():
            cur_song = self.app.playlist.current()
            self._playsong(cur_song['filepath'])
            if not self.is_playing.is_set():
                break
            else:
                self.app.playlist.next()

                if self.app.get_repeat():
                    self.app.playlist.previous()

    def _playsong(self, filepath, cur_time=0):
        sound = AudioSegment.from_file(filepath)
        player = pyaudio.PyAudio()
    
        stream = player.open(format = player.get_format_from_width(sound.sample_width),
                            channels = sound.channels,
                            rate = sound.frame_rate,
                            output = True)

        self.app.set_cur_time(cur_time)
        self.app.set_max_time(sound.duration_seconds)

        playchunk = sound[1000 * self.app.get_cur_time() : 1000 * self.app.get_max_time()]
        millisecondchunk = 10 / 1000.0

        self.app.update_gui_info()

        while self.app.get_cur_time() < self.app.get_max_time():
            self.app.set_cur_time(self.app.get_cur_time() + millisecondchunk)
            stream.write((playchunk[1000*self.app.get_cur_time():1000*(self.app.get_cur_time()+millisecondchunk)]-(60-60*self.app.get_volume()/100))._data)
            self.app.update_gui_info()
            if self.app.get_cur_time() >= self.app.get_max_time():
                break
            self.is_playing.wait()

        stream.close()
        player.terminate()

    def resume(self):
        self.is_playing.set()

    def pause(self):
        self.is_playing.clear()

    def stop(self):
        if self.play_thread is not None:
            self.app.set_cur_time(self.app.get_max_time())
            self.is_playing.clear()
            while self.play_thread.is_alive():
                pass

            self.play_thread = None
            self.app.set_cur_time(0)
            self.app.set_max_time(0)

    def next(self):
        if self.app.playlist.has_next():
            self.app.playlist.next()
            self.play()

    def previous(self):
        if self.app.playlist.has_previous():
            self.app.playlist.previous()
            self.play()
