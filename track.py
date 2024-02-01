from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import os

class Track:
    def __init__(self, file_path):
        self.file_path = file_path
        self.title = ""
        self.artist = ""
        self.album = ""
        self.length = 0
        self.genre = ""
        self.year = ""
        self.bit_depth = 'N/A'  # MP3 files do not have a bit depth attribute
        self.load_metadata()

    def load_metadata(self):
        if not os.path.exists(self.file_path):
            print(f"File not found: {self.file_path}")
            return

        try:
            # Ensure EasyID3 is used for ID3 tag reading.
            audio = MP3(self.file_path, ID3=EasyID3)
            
            # Safely retrieve metadata, falling back to defaults if necessary.
            self.title = audio.get('title', ['Unknown Title'])[0]
            self.artist = audio.get('artist', ['Unknown Artist'])[0]
            self.album = audio.get('album', ['Unknown Album'])[0]
            self.genre = audio.get('genre', ['Unknown Genre'])[0]
            self.year = audio.get('date', ['Unknown Year'])[0]  # 'date' tag for year
            self.length = audio.info.length
            self.sample_rate = str(audio.info.sample_rate) + ' Hz'
            self.bitrate = str(int(audio.info.bitrate / 1000)) + ' kbps'
            self.file_type = 'MP3'  # or dynamically determine the file type
        except Exception as e:
            print(f"Error loading metadata for {self.file_path}: {e}")

    def __str__(self):
        return f"{self.title} by {self.artist} from {self.album}, Genre: {self.genre}, Year: {self.year}, Length: {self.length} seconds"

# Usage example:
# my_track = Track('path_to_my_mp3_file.mp3')
# print(my_track)
