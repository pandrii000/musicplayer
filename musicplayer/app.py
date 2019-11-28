from music import Playlist, MusicPlayer
from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication


class PlayerApplication:
    def __init__(self):
        # APPLICATION VARIABLES
        self._volume = 100
        self._cur_time = 0
        self._max_time = 0
        self._repeat = False

        # PLAYLIST
        self.playlist = Playlist()

        # GUI
        self.qapp = QApplication([])
        self.mainwindow = MainWindow(self)

        # MUSIC PLAYER
        self.player = MusicPlayer(self)

    def start(self):
        self.mainwindow.show()
        self.qapp.exec_()

    def update_gui_info(self):
        self.mainwindow.update_playing_info()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()
    
    def resume(self):
        self.player.resume()

    def stop(self):
        self.player.stop()

    def next(self):
        self.player.next()

    def previous(self):
        self.player.previous()

    def get_volume(self):
        return self._volume

    def set_volume(self, v):
        self._volume = v

    def get_cur_time(self):
        return self._cur_time

    def set_cur_time(self, t):
        self._cur_time = t

    def get_max_time(self):
        return self._max_time

    def set_max_time(self, t):
        self._max_time = t

    def get_repeat(self):
        return self._repeat

    def set_repeat(self, b):
        self._repeat = b


if __name__ == '__main__':
    app = PlayerApplication()
    playlist = Playlist()
    playlist.add_from_directory('./')
    app.playlist = playlist
    app.mainwindow.update_playlist_widget()
    app.start()