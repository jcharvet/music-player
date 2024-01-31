import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class AudioPlayer:
    """
    A class representing an audio player application.

    Attributes:
        root (tk.Tk): The root window of the application.
        settings_file (str): The path to the settings file.
        folder_label (tk.Label): The label displaying the selected folder.
        audio_treeview (ttk.Treeview): The treeview displaying the audio files.
        prev_btn (tk.Button): The button for playing the previous audio.
        play_btn (tk.Button): The button for playing the audio.
        stop_btn (tk.Button): The button for stopping the audio.
        next_btn (tk.Button): The button for playing the next audio.
        volume_scale (tk.Scale): The scale for adjusting the volume.
        current_audio_index (int): The index of the currently selected audio.
        is_playing_sequence (bool): Indicates if the audio is playing in sequence.

    Methods:
        __init__(self, root): Initializes the AudioPlayer object.
        setup_labels(self): Sets up the labels in the GUI.
        setup_treeview(self): Sets up the treeview in the GUI.
        setup_controls(self): Sets up the controls in the GUI.
        select_folder(self): Opens a file dialog to select a folder.
        load_audio_files(self, folder_path): Loads the audio files from the selected folder.
        get_audio_metadata(self, file_path): Retrieves the metadata of an audio file.
        on_double_click_treeview(self, event): Handles the double-click event on the treeview.
        play_audio(self): Plays the selected audio.
        check_for_music_end(self): Checks if the current audio has ended.
        play_previous(self): Plays the previous audio.
        play_next(self): Plays the next audio.
        stop_audio(self): Stops the audio playback.
        adjust_volume(self, value): Adjusts the volume of the audio.
        save_folder(self, folder_path): Saves the selected folder to the settings file.
        load_saved_folders(self): Loads the previously saved folders from the settings file.
    """
    def __init__(self, root):
        self.root = root
        root.title("Audio Player")
        self.settings_file = "settings.txt"

        # Initialize pygame for audio playback
        pygame.init()
        pygame.mixer.init()

        # GUI Elements setup
        self.setup_labels()
        self.setup_treeview()
        self.setup_controls()
        self.load_saved_folders()
class AudioPlayer:
    def __init__(self, root):
        self.root = root
        root.title("Audio Player")
        self.settings_file = "settings.txt"

        # Initialize pygame for audio playback
        pygame.init()
        pygame.mixer.init()

        # GUI Elements setup
        self.setup_labels()
        self.setup_treeview()
        self.setup_controls()
        self.load_saved_folders()

    def setup_labels(self):
        self.folder_label = tk.Label(self.root, text="No folder selected")
        self.folder_label.pack()

    def setup_treeview(self):
        columns = ('Filename', 'Title', 'Artist', 'Album', 'Length', 'Sample Rate', 'Bit Depth', 'Bitrate', 'File Type')
        self.audio_treeview = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.audio_treeview.heading(col, text=col)
            self.audio_treeview.column(col, width=100)
        self.audio_treeview.pack(expand=True, fill='both')
        self.audio_treeview.bind('<Double-1>', self.on_double_click_treeview)

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        self.prev_btn = tk.Button(control_frame, text="Previous", command=self.play_previous)
        self.prev_btn.pack(side=tk.LEFT)

        self.play_btn = tk.Button(control_frame, text="Play", command=self.play_audio)
        self.play_btn.pack(side=tk.LEFT)

        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_audio)
        self.stop_btn.pack(side=tk.LEFT)

        self.next_btn = tk.Button(control_frame, text="Next", command=self.play_next)
        self.next_btn.pack(side=tk.LEFT)

        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.adjust_volume)
        self.volume_scale.set(20)
        self.volume_scale.pack()    

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir=os.path.expanduser("~/Desktop"))
        if folder_path:
            self.save_folder(folder_path)
            self.folder_label.config(text=folder_path)
            self.load_audio_files(folder_path)

    def load_audio_files(self, folder_path):
        self.audio_treeview.delete(*self.audio_treeview.get_children())
        for file in os.listdir(folder_path):
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(folder_path, file)
                audio_metadata = self.get_audio_metadata(file_path)
                self.audio_treeview.insert('', 'end', values=audio_metadata)

    def get_audio_metadata(self, file_path):
        try:
            audio = MP3(file_path, ID3=EasyID3)
            title = audio.get('title', [''])[0]
            artist = audio.get('artist', [''])[0]
            album = audio.get('album', [''])[0]
            length = str(int(audio.info.length))  # or format as needed
            sample_rate = audio.info.sample_rate
            bitrate = audio.info.bitrate // 1000  # in kbps
            file_type = 'MP3'
            bit_depth = 'N/A'  # MP3 files do not have bit depth
            return (os.path.basename(file_path), title, artist, album, length, sample_rate, bit_depth, bitrate, file_type)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read metadata from {file_path}.\nError: {str(e)}")
            return (os.path.basename(file_path), '', '', '', '', '', '', '', '')

    def on_double_click_treeview(self, event):
        # Get the item that was double-clicked
        selected_item = self.audio_treeview.selection()[0]
        # Set the current audio index to the index of the selected item
        self.current_audio_index = self.audio_treeview.index(selected_item)
        # Play the selected audio
        self.play_audio()

    def play_audio(self):
        if self.current_audio_index is not None:
            # Get the item to play based on the current index
            item_to_play = self.audio_treeview.get_children()[self.current_audio_index]
            # Extract the filename from the item values
            filename = self.audio_treeview.item(item_to_play, 'values')[0]
            folder = self.folder_label.cget("text")
            file_path = os.path.join(folder, filename)
            # Load and play the audio file
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            # Check if we should proceed to the next song after this one ends
            self.check_for_music_end()

    def check_for_music_end(self):
        if not pygame.mixer.music.get_busy():
            if self.is_playing_sequence:
                self.play_next()
        else:
            self.root.after(100, self.check_for_music_end)

    def play_previous(self):
        if self.audio_treeview.get_children():
            prev_index = (self.current_audio_index - 1) % len(self.audio_treeview.get_children())
            self.audio_treeview.selection_set(self.audio_treeview.get_children()[prev_index])
            self.current_audio_index = prev_index
            self.play_audio()

    def play_next(self):
        if self.audio_treeview.get_children():
            next_index = (self.current_audio_index + 1) % len(self.audio_treeview.get_children())
            self.audio_treeview.selection_set(self.audio_treeview.get_children()[next_index])
            self.current_audio_index = next_index
            self.play_audio()

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.is_playing_sequence = False

    def adjust_volume(self, value):
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)

    def save_folder(self, folder_path):
        with open(self.settings_file, "a") as file:
            file.write(folder_path + "\n")

    def load_saved_folders(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                folders = file.readlines()
                if folders:
                    last_folder = folders[-1].strip()
                    self.folder_label.config(text=last_folder)
                    self.load_audio_files(last_folder)

root = tk.Tk()
app = AudioPlayer(root)
root.mainloop()
