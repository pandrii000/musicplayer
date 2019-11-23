from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("Music Player")

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
        self.main_layout.addWidget(self.song_label)

        # ======== DEFINE PLAYLIST LEVEL ========  

        self.playlist_widget = QListWidget()
        self.main_layout.addWidget(self.playlist_widget)

        # ======== DEFINE BOTTOM LEVEL ========  


    def open_file(self):
        print("Opening file..")

    def open_directory(self):
        print("Opening directory..")

    def import_playlist(self):
        print("Importing playlist..")

    def export_playlist(self):
        print("Exporting playlist..")

    def about(self):
        print("About..")



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()