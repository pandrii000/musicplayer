from tkinter import Tk, Label, Button, Entry

from music import MusicPlayer


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.player = MusicPlayer()

    def _make_widgets(self):
        '''Створити елементи інтерфейсу.'''
        self.master.title("MusicPlayer")
        
        self.entry = Entry(master)
        self.entry.insert(0, "/home/andrii_polukhin/university/labs/lab31/PracticeProgramming/musicplayer/resources/In The End (Official Video) - Linkin Park.mp3")
        self.entry.pack()

        self.buttonplay = Button(
            master, text="Play", command=lambda: play_audio_background(self.entry.get()))
        self.buttonplay.pack()

    def _make_entries(self):
        '''Створити надписи та поля введення.'''
        pass

    def _layout_entries(self):
        '''Озмістити надписи та поля введення.'''
        pass

    def play_handler(self, ev=None):
        '''Обробити натиснення кнопки "Ok".'''
        print('playing..')


if __name__ == "__main__":
    root = Tk()
    my_gui = MainWindow(root)
    root.mainloop()
