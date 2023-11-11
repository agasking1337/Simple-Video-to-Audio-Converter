import os
import moviepy.editor as mp
from tkinter import Tk, filedialog, Label, Button, Text, ttk
from ttkthemes import ThemedTk
import threading

class VideoToAudioConverter:
    def __init__(self, root):
        self.root = ThemedTk(theme="equilux")
        self.root.title("Video to Audio Converter")
        self.root.geometry("800x500")

        self.video_paths = []
        self.audio_path = ""
        self.conversion_thread = None

        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Arial', 12), background='#E50914', foreground='#FFFFFF', relief="flat")

        self.root.configure(bg='#111111')

        self.label = Label(self.root, text="Select video files:", font=('Arial', 16, 'bold'), pady=10, bg='#111111', fg='#FFFFFF')
        self.label.pack()

        self.file_list = Text(self.root, height=5, width=60, font=('Arial', 10), bg='#111111', fg='#FFFFFF', wrap="none")
        self.file_list.pack(pady=10)

        self.select_button = ttk.Button(self.root, text="Browse", command=self.browse_videos, style="TButton")
        self.select_button.pack(pady=5)

        self.clear_button = ttk.Button(self.root, text="Clear Selection", command=self.clear_selection, style="TButton")
        self.clear_button.pack(pady=5)

        self.convert_button = ttk.Button(self.root, text="Convert", command=self.convert_videos_to_audio, style="TButton")
        self.convert_button.pack(pady=5)

        self.progress_label = Label(self.root, text="", font=('Arial', 14), pady=10, bg='#111111', fg='#FFFFFF')
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.root.after(100, self.check_conversion_status)

    def browse_videos(self):
        self.video_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        self.update_file_list()

    def clear_selection(self):
        self.video_paths = []
        self.update_file_list()

    def update_file_list(self):
        self.file_list.delete(1.0, "end")
        for path in self.video_paths:
            self.file_list.insert("end", f"{os.path.basename(path)}\n")
        self.file_list.see("end")

    def convert_videos_to_audio(self):
        if not self.video_paths:
            self.label.config(text="Please select video files.")
            return

        folder_path = filedialog.askdirectory()
        if not folder_path:
            self.label.config(text="Please select a destination folder.")
            return

        self.progress_label.config(text="Converting...")
        self.progress_bar["value"] = 0

        def update_progress_callback(progress_percentage):
            self.progress_label.config(text=f"Converting: {progress_percentage}%", fg='#E50914')
            self.progress_bar["value"] = progress_percentage

        def convert_single_video(video_path):
            video_title = os.path.splitext(os.path.basename(video_path))[0]
            audio_path = os.path.join(folder_path, f"{video_title}_audio.mp3")

            video_clip = mp.VideoFileClip(video_path)
            audio_clip = video_clip.audio

            total_frames = int(video_clip.fps * video_clip.duration)
            frame_count = 0

            while frame_count < total_frames:
                progress_percentage = int((frame_count / total_frames) * 100)
                update_progress_callback(progress_percentage)
                frame_count += 1

            audio_clip.write_audiofile(audio_path, codec='mp3')

        def convert_all_videos():
            for video_path in self.video_paths:
                convert_single_video(video_path)

            update_progress_callback(100)
            self.progress_label.config(text="Conversion complete!", fg='#FFFFFF')
            self.progress_bar.stop()

        self.conversion_thread = threading.Thread(target=convert_all_videos)
        self.conversion_thread.start()

    def check_conversion_status(self):
        if self.conversion_thread and not self.conversion_thread.is_alive():
            self.progress_label.config(text="Conversion complete!", fg='#FFFFFF')
            self.progress_bar.stop()
        else:
            self.root.after(100, self.check_conversion_status)

if __name__ == "__main__":
    app = VideoToAudioConverter(None)
    app.root.mainloop()
