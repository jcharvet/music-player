import os
import tkinter as tk
from tkinter import filedialog
import pygame

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        root.title("Green Audio Player")
        self.settings_file = "settings.txt"

        # Initialize pygame for audio playback
        pygame.init()
        pygame.mixer.init()

        # GUI Elements
        self.folder_label = tk.Label(root, text="No folder selected")
        self.folder_label.pack()

        self.select_folder_btn = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack()

        self.audio_listbox = tk.Listbox(root, width=50, height=20)  # Increased size
        self.audio_listbox.pack()

        self.play_btn = tk.Button(root, text="Play", command=self.play_audio)
        self.play_btn.pack()

        self.stop_btn = tk.Button(root, text="Stop", command=self.stop_audio)
        self.stop_btn.pack()

        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.adjust_volume)
        self.volume_scale.set(100)  # Default volume
        self.volume_scale.pack()

        # Current playing audio
        self.current_audio = None

        # Load saved folders
        self.load_saved_folders()

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

    def play_audio(self):
        if self.audio_listbox.curselection():
            selected_index = self.audio_listbox.curselection()[0]
            selected_file = self.audio_listbox.get(selected_index)
            folder = self.folder_label.cget("text")
            file_path = os.path.join(folder, selected_file)

            if self.current_audio != file_path:
                self.current_audio = file_path
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

    def stop_audio(self):
        pygame.mixer.music.stop()

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
                    last_folder = folders[-1].strip()  # Load the last saved folder
                    self.folder_label.config(text=last_folder)
                    self.load_audio_files(last_folder)

root = tk.Tk()
app = AudioPlayer(root)
root.mainloop()
