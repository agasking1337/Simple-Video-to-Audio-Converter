import os
import moviepy.editor as mp
from tkinter import Tk, filedialog, Label, Button, ttk
from ttkthemes import ThemedTk
import threading

class VideoToAudioConverter:
    def __init__(self, root):
        self.root = ThemedTk(theme="clam") 
        self.root.title("Video to Audio Converter")
        self.root.geometry("800x400")
        self.root.configure(bg='#CCCCCC')

        self.video_path = ""
        self.audio_path = ""
        self.conversion_thread = None

      
        style = ttk.Style()

        self.label = Label(self.root, text="Select a video file:", font=('roboto', 14), bg='#CCCCCC', fg='#000000')
        self.label.pack(pady=20)

        self.select_button = ttk.Button(self.root, text="Browse", command=self.browse_video, style="TButton")
        self.select_button.pack(pady=10)

        self.convert_button = ttk.Button(self.root, text="Convert", command=self.convert_video_to_audio, style="TButton")
        self.convert_button.pack(pady=10)

        self.progress_label = Label(self.root, text="", font=('Arial', 12), bg='#CCCCBC', fg='#001200')
        self.progress_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.root.after(100, self.check_conversion_status)

    def browse_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        self.label.config(text=f"Selected video: {self.video_path}")

    def convert_video_to_audio(self):
        if not self.video_path:
            self.label.config(text="Please select a video file.")
            return

        video_title = os.path.splitext(os.path.basename(self.video_path))[0]
        self.audio_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("Audio files", "*.mp3")],
            initialfile=f"{video_title}_audio"
        )

        video_clip = mp.VideoFileClip(self.video_path)
        audio_clip = video_clip.audio

        total_frames = int(video_clip.fps * video_clip.duration)
        frame_count = 0

        def update_progress_callback():
            nonlocal frame_count
            while frame_count < total_frames:
                progress_percentage = int((frame_count / total_frames) * 100)
                self.progress_label.config(text=f"Converting: {progress_percentage}%")
                self.progress_bar["value"] = progress_percentage
                frame_count += 1

        def convert():
            nonlocal frame_count
            frame_count = 0
            update_progress_thread = threading.Thread(target=update_progress_callback)
            update_progress_thread.start()

            audio_clip.write_audiofile(self.audio_path, codec='mp3')
            frame_count = total_frames
            update_progress_thread.join()
            self.progress_label.config(text="Conversion complete!")
            self.progress_bar.stop()


        self.conversion_thread = threading.Thread(target=convert)
        self.conversion_thread.start()

    def check_conversion_status(self):
        if self.conversion_thread and not self.conversion_thread.is_alive():
            self.progress_label.config(text="Conversion complete!")
            self.progress_bar.stop()
        else:
            self.root.after(100, self.check_conversion_status)

if __name__ == "__main__":
    app = VideoToAudioConverter(None)
    app.root.mainloop()
