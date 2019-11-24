from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from music import Playlist, MusicPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.playlist = Playlist()
        self.player = MusicPlayer()

        self.setWindowTitle("Music Player")
        self.setMinimumSize(800, 500)

        # ======== DEFINE MENU ========

        # ======== DEFINE FILE MENU ========

        self.menu = self.menuBar().addMenu("File")

        self.open_file_action = QAction("Open File")
        self.open_file_action.triggered.connect(self.open_file)
        self.menu.addAction(self.open_file_action)

        self.open_directory_action = QAction("Open Directory")
        self.open_directory_action.triggered.connect(self.open_directory)
        self.menu.addAction(self.open_directory_action)

        self.close_action = QAction("Close")
        self.close_action.triggered.connect(self.close)
        self.menu.addAction(self.close_action)

        # ======== DEFINE PLAYLIST MENU ========

        self.menu = self.menuBar().addMenu("Playlist")

        self.import_playlist_action = QAction("Import playlist")
        self.import_playlist_action.triggered.connect(self.import_playlist)
        self.menu.addAction(self.import_playlist_action)

        self.export_playlist_action = QAction("Export playlist")
        self.export_playlist_action.triggered.connect(self.export_playlist)
        self.menu.addAction(self.export_playlist_action)

        # ======== DEFINE HELP MENU ========

        self.menu = self.menuBar().addMenu("Help")

        self.about_action = QAction("About")
        self.about_action.triggered.connect(self.about)
        self.menu.addAction(self.about_action)

        # ======== DEFINE WIDGETS ========

        # ======== DEFINE MAIN LAYOUT ========

        self.main_layout = QVBoxLayout()
        self.main_layout_widget = QWidget()
        self.main_layout_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_layout_widget)

        # ======== DEFINE HEADER LEVEL ========

        self.song_label = QLabel('No song playing...')
        self.song_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.song_label)

        # ======== DEFINE PLAYLIST LEVEL ========

        # dict of headers, where
        # key = header name
        # value = name of the same property in PlaylistElement
        self.columns = {"Filename": "filename",
                        "Artist": "artist",
                        "Title": "title",
                        "Format": "format",
                        "Filepath": "filepath"
                        }
        self.playlist_widget = QTableWidget()
        # adjust size of table to window size
        self.playlist_widget.horizontalHeader().setStretchLastSection(True)
        self.playlist_widget.setColumnCount(len(self.columns))
        self.playlist_widget.setRowCount(0)
        self.playlist_widget.setHorizontalHeaderLabels(self.columns.keys())
        self.playlist_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlist_widget.horizontalHeader().sectionClicked.connect(
            self.on_playlist_column_clicked)
        self.playlist_widget.doubleClicked.connect(self.on_cell_double_clicked)
        self.main_layout.addWidget(self.playlist_widget)

        # ======== DEFINE SLIDER LAYOUT ========

        self.slider_layout = QHBoxLayout()
        self.slider_layout_widget = QWidget()
        self.slider_layout_widget.setLayout(self.slider_layout)
        self.main_layout.addWidget(self.slider_layout_widget)

        # ======== DEFINE SLIDER LEVEL ========

        self.current_time_label = QLabel('--:--')
        self.slider_layout.addWidget(self.current_time_label)

        self.play_position_slider = QSlider(Qt.Horizontal)
        self.play_position_slider.setMinimum(0)
        self.play_position_slider.setTickInterval(0.01)
        self.play_position_slider.setValue(0)
        self.play_position_slider.valueChanged.connect(self.on_play_position_changed)
        self.slider_layout.addWidget(self.play_position_slider)

        self.finish_time_label = QLabel('--:--')
        self.slider_layout.addWidget(self.finish_time_label)

        # ======== DEFINE CONTROLS LAYOUT ========

        self.controls_layout = QHBoxLayout()
        self.controls_layout.setAlignment(Qt.AlignCenter)
        self.controls_layout_widget = QWidget()
        self.controls_layout_widget.setLayout(self.controls_layout)
        self.main_layout.addWidget(self.controls_layout_widget)

        # ======== DEFINE CONTROLS LEVEL ========

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon('play_button.png'))
        self.play_button.setIconSize(QSize(30, 30))
        self.play_button.setFixedSize(30, 30)
        self.play_button.clicked.connect(self.on_play_button_clicked)
        self.controls_layout.addWidget(self.play_button, Qt.AlignLeft)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon('pause_button.png'))
        self.pause_button.setIconSize(QSize(30, 30))
        self.pause_button.setFixedSize(30, 30)
        self.pause_button.clicked.connect(self.on_pause_button_clicked)
        self.controls_layout.addWidget(self.pause_button, Qt.AlignLeft)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon('stop_button.png'))
        self.stop_button.setIconSize(QSize(30, 30))
        self.stop_button.setFixedSize(30, 30)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)
        self.controls_layout.addWidget(self.stop_button, Qt.AlignLeft)

        self.repeat_button = QPushButton()
        self.repeat_button.setIcon(QIcon('repeat_button.png'))
        self.repeat_button.setIconSize(QSize(30, 30))
        self.repeat_button.setFixedSize(30, 30)
        self.repeat_button.clicked.connect(self.on_repeat_button_clicked)
        self.controls_layout.addWidget(self.repeat_button, Qt.AlignLeft)

        self.controls_layout.addStretch(4)

        self.controls_layout.addWidget(QWidget())

        self.volume_label = QLabel("Volume:")
        self.controls_layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.controls_layout.addWidget(self.volume_slider, Qt.AlignRight)

    def open_file(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            self, "Select File", "", "Music Files (*.mp3 *.wav)", options=QFileDialog.DontUseNativeDialog)
        if filenames:
            for filename in filenames:
                self.playlist.add_file(filename)

        self.update_playlist_widget(sorting_category='filename')

    def update_playlist_widget(self, sorting_category=None):
        if sorting_category is not None:
            self.playlist.sort_by(sorting_category)

        # clear widget info
        while self.playlist_widget.rowCount() > 0:
            self.playlist_widget.removeRow(0)

        # write info
        for i, playlist_element in enumerate(self.playlist):
            self.playlist_widget.insertRow(i)
            for j, column in enumerate(self.columns):
                self.playlist_widget.setItem(i, j, QTableWidgetItem(
                    playlist_element[self.columns[column]]))

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(
            None, 'Open Folder', '', options=QFileDialog.ShowDirsOnly)
        if directory:
            self.playlist.add_from_directory(directory)
            self.update_playlist_widget()

    def import_playlist(self):
        print("Importing playlist..")

    def export_playlist(self):
        print("Exporting playlist..")

    def about(self):
        print("About..")

    def on_cell_double_clicked(self, item):
        index_in_playlist = item.row()
        playlist_element = self.playlist[index_in_playlist]
        self.play_song(playlist_element)

    def on_play_button_clicked(self):
        index_in_playlist = self.playlist_widget.currentRow()
        if index_in_playlist >= 0:
            playlist_element = self.playlist[index_in_playlist]
            self.play_song(playlist_element)

    def on_pause_button_clicked(self):
        self.player.pause()

    def on_stop_button_clicked(self):
        self.player.stop()

    def on_repeat_button_clicked(self):
        self.player.repeat = True

    def on_playlist_column_clicked(self, column_id):
        column_name = list(self.columns.keys())[column_id]
        self.playlist.sort_by(self.columns[column_name])
        self.update_playlist_widget()

    def on_volume_changed(self):
        self.player.set_volume(self.volume_slider.value())

    def on_play_position_changed(self):
        self.player.time = self.play_position_slider.value()

    def play_song(self, playlist_element):
        self.song_label.setText(playlist_element['filename'])
        self.player.play(playlist_element['filepath'])


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.open_directory()
    window.show()
    app.exec_()
