from music import *

if __name__ == "__main__":
    filepath1 = 'dir1/  Artist1 artist - Title2 title   .mp3'
    filepath2 = 'dir2/  Artist2 artist - Title1 title   .wav'
    playlist = Playlist([filepath1, filepath2])
    playlist.sort_by('title')
    playlist.show()