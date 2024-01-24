import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
import os
from tkinter import messagebox

class MusicPlayer:

    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Initializing Pygame
        pygame.init()

        # Initializing Pygame Mixer
        pygame.mixer.init()

        # Playlist Frame
        self.playlist_frame = tk.Frame(self.root)
        self.playlist_frame.pack(pady=10)

        # Playlist Listbox
        self.playlist = tk.Listbox(self.playlist_frame, width=40, height=10)
        self.playlist.pack(fill=tk.BOTH, expand=True)
        self.playlist.bind("<<ListboxSelect>>", self.play_selected)

        # Control Frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # Play/Pause button
        self.play_var = tk.StringVar()
        self.play_var.set("Play")
        self.play_pause_button = ttk.Button(self.control_frame, textvariable=self.play_var, command=self.play_pause)
        self.play_pause_button.grid(row=1, column=0, padx=10)

        # Skip Backward button
        self.skip_backward_button = ttk.Button(self.control_frame, text="⏪", command=self.skip_backward)
        self.skip_backward_button.grid(row=1, column=1, padx=10)

        # Skip Forward button
        self.skip_forward_button = ttk.Button(self.control_frame, text="⏩", command=self.skip_forward)
        self.skip_forward_button.grid(row=1, column=2, padx=10)

        # Import Music button
        self.import_button = ttk.Button(self.control_frame, text="Import Music", command=self.import_music)
        self.import_button.grid(row=1, column=3, padx=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Current song label
        self.current_song = ""

        # Paused variable to check if the song is paused or not
        self.paused = False

    def play_selected(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        print("Selected Song:", selected_song)
        self.current_song = selected_song

        try:
            pygame.mixer.music.load(self.current_song)
            print("Music Loaded:", self.current_song)
            self.progress_bar["maximum"] = pygame.mixer.Sound(self.current_song).get_length()
            self.update_progressbar()
            pygame.mixer.music.play()
            self.play_var.set("Pause")
        except pygame.error as e:
            print("Error loading music:", e)
            messagebox.showerror("Error", "Error loading the selected song.")

    def play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_var.set("Pause")
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_var.set("Play")

    def skip_backward(self):
        selection = self.playlist.curselection()
        if selection:
            prev_song_index = int(selection[0]) - 1
            if prev_song_index >= 0:
                prev_song = self.playlist.get(prev_song_index)
                self.current_song = prev_song
                pygame.mixer.music.load(self.current_song)
                pygame.mixer.music.play()
                self.play_var.set("Pause")
            else:
                messagebox.showwarning("Warning", "This is the first song.")
        else:
            messagebox.showerror("Error", "No song is selected.")

    def skip_forward(self):
        selection = self.playlist.curselection()
        if selection:
            next_song_index = int(selection[0]) + 1
            if next_song_index < self.playlist.size():
                next_song = self.playlist.get(next_song_index)
                self.current_song = next_song
                pygame.mixer.music.load(self.current_song)
                pygame.mixer.music.play()
                self.play_var.set("Pause")
            else:
                messagebox.showwarning("Warning", "This is the last song.")

    def import_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3;*.wav")])
        for file_path in file_paths:
            if file_path not in self.playlist.get(0, tk.END):
                self.playlist.insert(tk.END, file_path)

    def update_progressbar(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        print("Current Time:", current_time)
        self.progress_bar["value"] = current_time
        self.root.after(1000, self.update_progressbar)

# Main program starts here using the class MusicPlayer and the root window
root = tk.Tk()
MusicPlayer(root)
root.mainloop()
