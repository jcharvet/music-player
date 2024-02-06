# main.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Menu
import pygame
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import threading
import time

from visualization import Visualization
from video_player import VideoPlayer
from track import Track
from search import SearchAndSort

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        root.title("Audio Player")
        self.settings_file = "settings.txt"
        self.current_audio_index = None  # Initialize the current audio index to None

        # Initialize pygame for audio playback
        pygame.init()
        pygame.mixer.init()

        # GUI Elements setup
        self.setup_menus()  # Setup the menu bar
        self.setup_labels()
        self.setup_treeview()
        self.setup_controls()
        self.load_saved_folders()
        self.setup_search()  # Set up the search bar
        self.setup_sorting() # Set up the sorting options
        self.setup_search_and_sorting()  # Set up the search and sorting options

        # Initialize Visualization with a callback function
        self.visualization = Visualization(self, stop_callback=self.on_visualization_stop)
        self.video_player = VideoPlayer(self)

        # Initialize the flag to track visualization state
        self.visualization_active = False

    def setup_menus(self):
        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Create a File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add items to the File menu
        self.file_menu.add_command(label="Add Folder", command=self.select_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def setup_labels(self):
        self.folder_label = tk.Label(self.root, text="No folder selected")
        self.folder_label.pack()

    def setup_treeview(self):
        columns = ('Filename', 'Title', 'Artist', 'Album', 'Length', 'Sample Rate', 'Bit Depth', 'Bitrate', 'File Type', 'Genre', 'Year')
        self.audio_treeview = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.audio_treeview.heading(col, text=col, anchor=tk.W)
            self.audio_treeview.column(col, width=100)
        self.audio_treeview.pack(expand=True, fill='both')
        self.audio_treeview.bind('<Double-1>', self.on_double_click_treeview)
        self.audio_treeview.bind('<<TreeviewSelect>>', self.on_track_select)

    def on_track_select(self, event):
        selected_items = self.audio_treeview.selection()
        if selected_items:  # If there's at least one selected item
            self.current_audio_index = selected_items[0]  # Assuming the index or ID is what you need
        else:
            self.current_audio_index = None

    def setup_controls(self):
        # Initialize control_frame attribute
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        # Current track label
        self.current_track_label = tk.Label(self.control_frame, text='Not Playing', anchor='w')
        self.current_track_label.pack(fill='x')

        # Initialize the track progress bar
        self.track_progress = ttk.Progressbar(self.control_frame, orient="horizontal", length=100, mode="determinate")
        self.track_progress.pack(fill='x')

        self.prev_btn = tk.Button(self.control_frame, text="Previous", command=self.play_previous)
        self.prev_btn.pack(side=tk.LEFT)

        self.play_btn = tk.Button(self.control_frame, text="Play", command=self.play_audio)
        self.play_btn.pack(side=tk.LEFT)

        self.stop_btn = tk.Button(self.control_frame, text="Stop", command=self.stop_audio)
        self.stop_btn.pack(side=tk.LEFT)

        self.next_btn = tk.Button(self.control_frame, text="Next", command=self.play_next)
        self.next_btn.pack(side=tk.LEFT)

        self.volume_scale = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.adjust_volume)
        self.volume_scale.set(20)
        self.volume_scale.pack(side=tk.LEFT)

        # Button to toggle visualization
        self.visualization_btn = tk.Button(self.control_frame, text="Show Visualization", command=self.toggle_visualization)
        self.visualization_btn.pack(side=tk.LEFT)

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
                track = Track(file_path)
                self.audio_treeview.insert('', 'end', values=(
                    os.path.basename(file_path),
                    track.title,
                    track.artist,
                    track.album,
                    str(int(track.length)),  # Convert to int for a cleaner look, if desired
                    track.sample_rate,  # Assuming you have this attribute
                    'N/A',    # Assuming you have this attribute
                    track.bitrate,      # Assuming you have this attribute
                    track.file_type,    # Assuming you have this attribute
                    track.genre,
                    track.year
                ))

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
        if not self.current_audio_index:
            messagebox.showerror("Error", "No track selected!")
            return

        print(self.current_audio_index)
        # Get the item to play based on the current index
        item_to_play = self.audio_treeview.get_children()[self.current_audio_index]
        print(item_to_play)
        # Extract the filename from the item values
        filename = self.audio_treeview.item(item_to_play, 'values')[0]
        folder = self.folder_label.cget("text")
        file_path = os.path.join(folder, filename)
        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        # Check if we should proceed to the next song after this one ends
        self.check_for_music_end()

        # Use mutagen to get the track length
        audio = MP3(file_path)
        track_length = audio.info.length

        # Update track label with the new track name
        self.current_track_label.config(text='Now Playing: ' + filename)

        # Configure the track progress bar for the new track
        self.track_progress.config(maximum=track_length, value=0)

        # Start updating the progress bar
        self.update_progress()

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            self.track_progress['value'] = current_pos
            self.root.after(1000, self.update_progress)  # Schedule next update
        else:
            self.track_progress['value'] = 0

    def on_scale_move(self, val):
        if pygame.mixer.music.get_busy():
            # Seek to the new position if the user moves the progress bar
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(float(val))

    def check_for_music_end(self):
        if not pygame.mixer.music.get_busy():
            self.play_next()  # Automatically play the next track
        else:
            self.root.after(100, self.check_for_music_end)

    def play_previous(self):
        if self.audio_treeview.get_children():
            prev_index = (self.current_audio_index - 1) % len(self.audio_treeview.get_children())
            self.audio_treeview.selection_set(self.audio_treeview.get_children()[prev_index])
            self.current_audio_index = prev_index
            self.play_audio()

    def play_next(self):
        if self.current_audio_index is not None and self.audio_treeview.get_children():
            next_index = (self.current_audio_index + 1) % len(self.audio_treeview.get_children())
            self.audio_treeview.selection_set(self.audio_treeview.get_children()[next_index])
            self.current_audio_index = next_index
            self.play_audio()
        else:
            # If there's no current track, do nothing or reset to the first track
            pass  # or you can reset self.current_audio_index to 0 or another default value

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.is_playing_sequence = False
        self.current_audio_index = None  # Reset the current track index

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

    def toggle_visualization(self):
        if self.visualization_active:
            self.visualization.stop_visualization()
        else:
            self.visualization.start_visualization()
        # No need to toggle the button text here, it's handled in the callback
            
    def on_visualization_stop(self):
        # This method will be called when visualization stops
        self.visualization_active = False
        self.visualization_btn.config(text="Show Visualization")

    def show_video_player(self):
        # Implementation when VideoPlayer is available
        print("Video player shown")  # Replace with actual GUI code

    def hide_video_player(self):
        # Implementation when VideoPlayer is available
        print("Video player hidden")  # Replace with actual GUI code

    def setup_search_and_sorting(self):
        # Search Bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.root, textvariable=self.search_var)
        search_entry.pack(side=tk.TOP, fill=tk.X)
        
        # Assuming you have a button or entry for search
        search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        search_button.pack(side=tk.TOP)

        # Sort OptionMenu
        self.sort_var = tk.StringVar(value="Sort By")
        sort_options = ttk.OptionMenu(self.root, self.sort_var, "Sort By", "Artist", "Album", "Genre", "Year", "Title", command=self.perform_sort)
        sort_options.pack(side=tk.TOP)

        self.search_and_sort = SearchAndSort(self.audio_treeview)

    def setup_search(self):
        # Create a search bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.control_frame, textvariable=self.search_var)
        self.search_entry.pack()
        self.search_button = tk.Button(self.control_frame, text="Search", command=self.perform_search)
        self.search_button.pack()

    def perform_search(self):
        query = self.search_var.get().lower()
        for item in self.audio_treeview.get_children():
            track = self.audio_treeview.item(item, 'values')
            # Check if query is in any of the track's fields
            if query in track[1].lower() or query in track[2].lower() or query in track[3].lower():
                self.audio_treeview.item(item, tags='match')
            else:
                self.audio_treeview.item(item, tags='')

        # Highlight or show only matching items
        self.audio_treeview.tag_configure('match', background='yellow')

    def setup_sorting(self):
        # Create a dropdown or buttons for sorting options
        self.sort_var = tk.StringVar()
        self.sort_options = tk.OptionMenu(self.control_frame, self.sort_var, "Artist", "Album", "Title", command=self.perform_sort)
        self.sort_options.pack()

    def perform_sort(self, sort_by):
        all_tracks = [(self.audio_treeview.item(item, 'values'), item) for item in self.audio_treeview.get_children()]

        # Define sorted_tracks with a default value, such as the original order
        sorted_tracks = all_tracks

        if sort_by == "Artist":
            sorted_tracks = sorted(all_tracks, key=lambda x: x[0][2])
        elif sort_by == "Album":
            sorted_tracks = sorted(all_tracks, key=lambda x: x[0][3])
        elif sort_by == "Genre":
            sorted_tracks = sorted(all_tracks, key=lambda x: x[0][4])
        elif sort_by == "Year":
            sorted_tracks = sorted(all_tracks, key=lambda x: x[0][5])
        elif sort_by == "Title":
            sorted_tracks = sorted(all_tracks, key=lambda x: x[0][1])
        # Continue with other sorting criteria if needed

        # Now, iterate over the sorted_tracks and reinsert them into the Treeview
        for track in sorted_tracks:
            self.audio_treeview.move(track[1], '', 'end')


root = tk.Tk()
app = AudioPlayer(root)
root.mainloop()
