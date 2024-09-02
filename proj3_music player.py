import os
import threading
import tkinter as tk
from tkinter import messagebox
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x500")
        self.root.config(bg="#2B2B2B")
        self.root.resizable(False, False)

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Music directory
        self.music_folder = os.path.expanduser("~/Music")
        self.song_list = self.get_song_list()

        # Playback control variables
        self.playing = False
        self.paused = False
        self.current_song = None
        self.play_thread = None

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title = tk.Label(self.root, text="Music Player", font=("Helvetica", 20, "bold"), bg="#2B2B2B", fg="#FFFFFF")
        title.pack(pady=20)

        # Listbox to display songs
        self.listbox = tk.Listbox(self.root, bg="#1E1E1E", fg="#FFFFFF", selectbackground="#00BFFF", selectforeground="#1E1E1E", width=60, height=15, font=("Helvetica", 12))
        self.listbox.pack(pady=20)

        # Populate the listbox with songs
        for song in self.song_list:
            self.listbox.insert(tk.END, song)

        # Control Buttons Frame
        controls_frame = tk.Frame(self.root, bg="#2B2B2B")
        controls_frame.pack(pady=20)

        # Button styles
        button_style = {"font": ("Helvetica", 12, "bold"), "width": 12, "fg": "#FFFFFF", "activebackground": "#555555", "activeforeground": "#FFFFFF"}

        #  Buttons code
        play_button = tk.Button(controls_frame, text="Play", command=self.play_music, bg="#00CC00", **button_style)
        play_button.grid(row=0, column=0, padx=10)
        pause_button = tk.Button(controls_frame, text="Pause", command=self.pause_music, bg="#333333", **button_style)
        pause_button.grid(row=0, column=1, padx=10)
        stop_button = tk.Button(controls_frame, text="Stop", command=self.stop_music, bg="#CC0000", **button_style)
        stop_button.grid(row=0, column=2, padx=10)

        # Currently Playing Label
        self.current_song_label = tk.Label(self.root, text="No song playing", font=("Helvetica", 14), bg="#2B2B2B", fg="#00BFFF")
        self.current_song_label.pack(pady=10)

    def get_song_list(self):
        supported_formats = ('.mp3', '.wav', '.ogg', '.flac')
        try:
            return [f for f in os.listdir(self.music_folder) if f.lower().endswith(supported_formats)]
        except FileNotFoundError:
            messagebox.showerror("Error", f"Music folder not found at {self.music_folder}")
            return []
        
        # code for playing selcted song

    def play_music(self):
        if not self.playing:
            try:
                selected_index = self.listbox.curselection()
                if not selected_index:
                    messagebox.showwarning("No selection", "Please select a song to play.")
                    return
                selected_song = self.listbox.get(selected_index)
                song_path = os.path.join(self.music_folder, selected_song)
                self.current_song = selected_song
                self.current_song_label.config(text=f"Playing: {self.current_song}")

                # Load and play the song
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()

                self.playing = True
                self.paused = False

                # Start a thread to monitor when the song ends
                self.play_thread = threading.Thread(target=self.monitor_playback)
                self.play_thread.start()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while playing the song:\n{e}")

    def monitor_playback(self):
        while self.playing and pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        self.playing = False
        self.current_song_label.config(text="No song playing")

    def pause_music(self):
        if self.playing:
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
                self.current_song_label.config(text=f"Paused: {self.current_song}")
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                self.current_song_label.config(text=f"Playing: {self.current_song}")

    def stop_music(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            self.current_song_label.config(text="No song playing")

    def on_closing(self):
        self.stop_music()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
