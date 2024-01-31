import os
import tkinter as tk
from tkinter import filedialog
import pygame

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        root.title("Audio Player")
        self.settings_file = "settings.txt"

        # Initialize pygame for audio playback
        pygame.init()
        pygame.mixer.init()

        # GUI Elements
        self.folder_label = tk.Label(root, text="No folder selected")
        self.folder_label.pack()

        self.select_folder_btn = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack()

        self.audio_listbox = tk.Listbox(root, width=50, height=20)
        self.audio_listbox.pack()
        self.audio_listbox.bind('<Double-1>', self.on_double_click)

        # Playback control frame
        control_frame = tk.Frame(root)
        control_frame.pack()

        self.play_btn = tk.Button(control_frame, text="Play", command=self.play_audio)
        self.play_btn.pack(side=tk.LEFT)

        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_audio)
        self.stop_btn.pack(side=tk.LEFT)

        self.next_btn = tk.Button(control_frame, text="Next", command=self.play_next)
        self.next_btn.pack(side=tk.LEFT)

        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.adjust_volume)
        self.volume_scale.set(20)  # Set default volume to 20%
        self.volume_scale.pack()

        self.current_audio = None
        self.is_playing_sequence = False

        self.load_saved_folders()
        self.check_for_music_end()

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir=os.path.expanduser("~/Desktop"))
        if folder_path:
            self.save_folder(folder_path)
            self.folder_label.config(text=folder_path)
            self.load_audio_files(folder_path)

    def load_audio_files(self, folder_path):
        self.audio_listbox.delete(0, tk.END)
        for file in os.listdir(folder_path):
            if file.endswith('.mp3') or file.endswith('.wav'):
                self.audio_listbox.insert(tk.END, file)

    def on_double_click(self, event):
        self.is_playing_sequence = True
        self.play_audio()

    def play_audio(self):
        if self.audio_listbox.curselection():
            selected_index = self.audio_listbox.curselection()[0]
            self.play_selected_audio(selected_index)

    def play_selected_audio(self, index):
        selected_file = self.audio_listbox.get(index)
        folder = self.folder_label.cget("text")
        file_path = os.path.join(folder, selected_file)

        if self.current_audio != file_path:
            self.current_audio = file_path
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

    def check_for_music_end(self):
        if self.is_playing_sequence and not pygame.mixer.music.get_busy():
            current_index = self.audio_listbox.curselection()[0]
            next_index = (current_index + 1) % self.audio_listbox.size()
            self.audio_listbox.selection_clear(0, tk.END)
            self.audio_listbox.selection_set(next_index)
            self.play_selected_audio(next_index)
        self.root.after(1000, self.check_for_music_end)

    def play_next(self):
        if self.audio_listbox.size() > 0:
            current_index = self.audio_listbox.curselection()[0] if self.audio_listbox.curselection() else -1
            next_index = (current_index + 1) % self.audio_listbox.size()
            self.audio_listbox.selection_clear(0, tk.END)
            self.audio_listbox.selection_set(next_index)
            self.play_selected_audio(next_index)

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
