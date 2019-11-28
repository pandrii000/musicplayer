from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from music import Playlist, MusicPlayer


class MainWindow(QMainWindow):
    def __init__(self, application):
        QMainWindow.__init__(self)

        self.app = application

        self.setWindowTitle("Music Player")
        self.setMinimumSize(800, 500)
        
        # move to the center of the screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

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
        self.song_label_style = QFont("Courier", 18) 
        self.song_label.setFont(self.song_label_style)
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
                        "Filepath": "filepath"}

        self.playlist_widget = QTableWidget()
        # adjust size of table to window size
        self.playlist_widget.horizontalHeader().setStretchLastSection(True)
        self.playlist_widget.setColumnCount(len(self.columns))
        self.playlist_widget.setRowCount(0)
        self.playlist_widget.setHorizontalHeaderLabels(self.columns.keys())
        self.playlist_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlist_widget.horizontalHeader().sectionClicked.connect(self.on_playlist_column_clicked)
        self.playlist_widget.doubleClicked.connect(self.on_cell_double_clicked)
        self.main_layout.addWidget(self.playlist_widget)

        # ======== DEFINE SLIDER LAYOUT ========

        self.slider_layout = QHBoxLayout()
        self.slider_layout_widget = QWidget()
        self.slider_layout_widget.setLayout(self.slider_layout)
        self.main_layout.addWidget(self.slider_layout_widget)

        # ======== DEFINE SLIDER LEVEL ========

        self.cur_time_label = QLabel('--:--')
        self.slider_layout.addWidget(self.cur_time_label)

        self.play_position_slider = QSlider(Qt.Horizontal)
        self.play_position_slider.setMinimum(0)
        self.play_position_slider.setTickInterval(0.01)
        self.play_position_slider.setValue(0)
        self.play_position_slider.sliderPressed.connect(self.on_play_play_slider_pressed)
        self.play_position_slider.sliderReleased.connect(self.on_play_play_slider_released)
        self.slider_layout.addWidget(self.play_position_slider)

        self.max_time_label = QLabel('--:--')
        self.slider_layout.addWidget(self.max_time_label)

        # ======== DEFINE CONTROLS LAYOUT ========

        self.controls_layout = QHBoxLayout()
        self.controls_layout.setAlignment(Qt.AlignCenter)
        self.controls_layout_widget = QWidget()
        self.controls_layout_widget.setLayout(self.controls_layout)
        self.main_layout.addWidget(self.controls_layout_widget)

        # ======== DEFINE CONTROLS LEVEL ========

        # ======== DEFINE CONTROL BUTTONS ========

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon('resources/play.png'))
        self.play_button.setIconSize(QSize(30, 30))
        self.play_button.setFixedSize(30, 30)
        self.play_button.clicked.connect(self.on_play_button_clicked)
        self.controls_layout.addWidget(self.play_button, Qt.AlignLeft)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon('resources/pause.png'))
        self.pause_button.setIconSize(QSize(30, 30))
        self.pause_button.setFixedSize(30, 30)
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.on_pause_button_clicked)
        self.controls_layout.addWidget(self.pause_button, Qt.AlignLeft)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon('resources/stop.png'))
        self.stop_button.setIconSize(QSize(30, 30))
        self.stop_button.setFixedSize(30, 30)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)
        self.controls_layout.addWidget(self.stop_button, Qt.AlignLeft)

        self.repeat_button = QPushButton()
        self.repeat_button.setIcon(QIcon('resources/repeat.png'))
        self.repeat_button.setIconSize(QSize(30, 30))
        self.repeat_button.setFixedSize(30, 30)
        self.repeat_button.setCheckable(True)
        self.repeat_button.clicked.connect(self.on_repeat_button_clicked)
        self.controls_layout.addWidget(self.repeat_button, Qt.AlignLeft)

        self.previous_button = QPushButton()
        self.previous_button.setIcon(QIcon('resources/previous.png'))
        self.previous_button.setIconSize(QSize(30, 30))
        self.previous_button.setFixedSize(30, 30)
        self.previous_button.clicked.connect(self.on_previous_button_clicked)
        self.controls_layout.addWidget(self.previous_button, Qt.AlignLeft)

        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon('resources/next.png'))
        self.next_button.setIconSize(QSize(30, 30))
        self.next_button.setFixedSize(30, 30)
        self.next_button.clicked.connect(self.on_next_button_clicked)
        self.controls_layout.addWidget(self.next_button, Qt.AlignLeft)

        self.controls_layout.addStretch(4)

        self.controls_layout.addWidget(QWidget())

        # ======== DEFINE VOLUME CONTROLS ========

        self.volume_label = QLabel("Volume:")
        self.controls_layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.controls_layout.addWidget(self.volume_slider, Qt.AlignRight)

    def play_current_song(self):
        self.app.play()

    def update_playlist_widget(self, sorting_category=None):
        # sorting
        if sorting_category is not None:
            self.app.playlist.sort_by(sorting_category)

        # clear widget info
        while self.playlist_widget.rowCount() > 0:
            self.playlist_widget.removeRow(0)

        # write info
        for i, playlist_element in enumerate(self.app.playlist.elements):
            self.playlist_widget.insertRow(i)
            for j, column in enumerate(self.columns):
                self.playlist_widget.setItem(i, j, QTableWidgetItem(
                    playlist_element[self.columns[column]]))

    def setColorRow(self, rowIndex, color):
        for j in range(self.playlist_widget.columnCount()):
            self.playlist_widget.item(rowIndex, j).setBackground(color)

    def update_playing_info(self):
        self.song_label.setText(self.app.playlist.current()['filename'])
        self.cur_time_label.setText("{:0>2}:{:0>2}".format(int(self.app.get_cur_time()) // 60, int(self.app.get_cur_time()) % 60))
        self.max_time_label.setText("{:0>2}:{:0>2}".format(int(self.app.get_max_time()) // 60, int(self.app.get_max_time()) % 60))
        self.play_position_slider.setMaximum(self.app.get_max_time())
        self.play_position_slider.setValue(self.app.get_cur_time())

    def open_file(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, "Select File", "", "Music Files (*.mp3 *.wav)")
        if filenames:
            for filename in filenames:
                self.app.playlist.add_file(filename)

        self.update_playlist_widget(sorting_category='filename')

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Folder", "", options=QFileDialog.ShowDirsOnly)
        if directory:
            self.app.playlist.add_from_directory(directory)
            self.update_playlist_widget()

    def import_playlist(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select File", "", "JSON (*.json)")
        if filepath:
            self.app.playlist.from_json(filepath)
            self.update_playlist_widget()

    def export_playlist(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Select File", "", "*.json")
        if filepath:
            self.app.playlist.to_json(filepath)

    def about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About")
        msg.setText("Music Player made by Andrii Polukhin")
        msg.setInformativeText(
            '''
            Features:
             - supports default music player options
             - can play .mp3 and .wav files
             - search for a music in a directory recursively
             - import and export playlists
             - show this window 
            ''')
        msg.exec_()

    def on_cell_double_clicked(self, item):
        index_in_playlist = item.row()
        self.app.playlist.set_current(index_in_playlist)
        self.play_current_song()

    def on_play_button_clicked(self):
        index_in_playlist = self.playlist_widget.currentRow()
        if index_in_playlist >= 0:
            self.app.playlist.set_current(index_in_playlist)
            self.play_current_song()

    def on_pause_button_clicked(self):
        if self.pause_button.isChecked():
            self.app.pause()
        else:
            self.app.resume()

    def on_stop_button_clicked(self):
        self.app.stop()
        self.song_label.setText('No song playing...')

    def on_repeat_button_clicked(self):
        self.app.set_repeat(self.repeat_button.isChecked())

    def on_previous_button_clicked(self):
        self.app.previous()

    def on_next_button_clicked(self):
        self.app.next()

    def on_volume_changed(self):
        self.app.set_volume(self.volume_slider.value())

    def on_playlist_column_clicked(self, column_id):
        column_name = list(self.columns.keys())[column_id]
        self.app.playlist.sort_by(self.columns[column_name])
        self.update_playlist_widget()

    def on_play_play_slider_pressed(self):
        self.app.pause()

    def on_play_play_slider_released(self):
        self.app.set_cur_time(self.play_position_slider.value())
        self.app.resume()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.app.playlist.remove(self.playlist_widget.currentRow())
            self.update_playlist_widget()
        elif e.key() == Qt.Key_Space:
            if not self.pause_button.isChecked():
                self.pause_button.toggle()
                self.app.pause()
            else:
                self.pause_button.toggle()
                self.app.resume()