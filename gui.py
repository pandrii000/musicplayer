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

        self.playlist_widget = QTableWidget()
        # adjust size of table to window size
        self.playlist_widget.horizontalHeader().setStretchLastSection(True)
        self.playlist_widget.setColumnCount(5)
        self.playlist_widget.setRowCount(1)
        self.playlist_widget.setHorizontalHeaderLabels(["Filename", "Artist", "Title", "Format", "Filepath"])
        self.playlist_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlist_widget.horizontalHeaderItem(0).setToolTip("Filename")
        self.playlist_widget.horizontalHeaderItem(0).setToolTip("Artist")
        self.playlist_widget.horizontalHeaderItem(1).setToolTip("Title")
        self.playlist_widget.horizontalHeaderItem(2).setToolTip("Format")
        self.playlist_widget.horizontalHeaderItem(3).setToolTip("Filepath")
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

        self.play_slider = QSlider(Qt.Horizontal)
        self.slider_layout.addWidget(self.play_slider)
        
        self.finish_time_label = QLabel('--:--')
        self.slider_layout.addWidget(self.finish_time_label) 

        # ======== DEFINE CONTROLS LAYOUT ========  

        self.controls_layout = QHBoxLayout()
        self.controls_layout.setAlignment(Qt.AlignHCenter)
        self.controls_layout_widget = QWidget()
        self.controls_layout_widget.setLayout(self.controls_layout)
        self.main_layout.addWidget(self.controls_layout_widget)

        # ======== DEFINE CONTROLS LEVEL ========
        
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon('play_button.png'))
        self.play_button.setIconSize(QSize(30,30))
        self.play_button.setFixedSize(30, 30)
        self.play_button.clicked.connect(self.on_play_button_clicked)
        self.controls_layout.addWidget(self.play_button) 

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon('pause_button.png'))
        self.pause_button.setIconSize(QSize(30,30))
        self.pause_button.setFixedSize(30, 30)
        self.pause_button.clicked.connect(self.on_pause_button_clicked)
        self.controls_layout.addWidget(self.pause_button) 

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon('stop_button.png'))
        self.stop_button.setIconSize(QSize(30,30))
        self.stop_button.setFixedSize(30, 30)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)
        self.controls_layout.addWidget(self.stop_button) 

        self.repeat_button = QPushButton()
        self.repeat_button.setIcon(QIcon('repeat_button.png'))
        self.repeat_button.setIconSize(QSize(30,30))
        self.repeat_button.setFixedSize(30, 30)
        self.repeat_button.clicked.connect(self.on_repeat_button_clicked)
        self.controls_layout.addWidget(self.repeat_button) 

    def open_file(self):
        filenames, _ = QFileDialog.getOpenFileNames(self,"Select File", "","Music Files (*.mp3 *.wav)", options=QFileDialog.DontUseNativeDialog)
        if filenames:
            for filename in filenames:
                self.playlist.add_file(filename)

        self.reload_playlist_widget(sorting_category='filename')

    def reload_playlist_widget(self, sorting_category=None):
        if sorting_category is not None:
            self.playlist.sort_by(sorting_category)

        # clear widget info
        while self.playlist_widget.rowCount() > 0:
            self.playlist_widget.removeRow(0)

        # write info 
        for i, playlist_element in enumerate(self.playlist):
            self.playlist_widget.insertRow(i)
            self.playlist_widget.setItem(i, 0, QTableWidgetItem(playlist_element['filename'])) 
            self.playlist_widget.setItem(i, 1, QTableWidgetItem(playlist_element['artist'])) 
            self.playlist_widget.setItem(i, 2, QTableWidgetItem(playlist_element['title'])) 
            self.playlist_widget.setItem(i, 3, QTableWidgetItem(playlist_element['format'])) 
            self.playlist_widget.setItem(i, 4, QTableWidgetItem(playlist_element['filepath'])) 
            print(playlist_element.get_properties())

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(None, 'Open Folder', '', options=QFileDialog.ShowDirsOnly)
        if directory:
            self.playlist.add_from_directory(directory)

    def import_playlist(self):
        print("Importing playlist..")

    def export_playlist(self):
        print("Exporting playlist..")

    def about(self):
        print("About..")

    def on_cell_double_clicked(self, item):
        index_in_playlist = item.row()
        playlist_element = self.playlist[index_in_playlist]
        filepath = playlist_element['filepath']
        self.player.play(filepath)

    def on_play_button_clicked(self):
        index_in_playlist = self.playlist_widget.currentRow()
        playlist_element = self.playlist[index_in_playlist]
        filepath = playlist_element['filepath']
        self.player.play(filepath)

    def on_pause_button_clicked(self):
        self.player.pause()

    def on_stop_button_clicked(self):
        self.player.stop()

    def on_repeat_button_clicked(self):
        self.player.repeat = True


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()