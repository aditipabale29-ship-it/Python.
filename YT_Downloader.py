import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_path = os.path.expanduser("~/Downloads")
        self.quality_var = tk.StringVar(value="720p")
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="YouTube Video Downloader", 
                              font=("Arial", 18, "bold"), fg="#FF0000")
        title_label.pack(pady=20)
        
        # URL Frame
        url_frame = tk.Frame(self.root)
        url_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(url_frame, text="Video URL:", font=("Arial", 10)).pack(anchor="w")
        url_entry = tk.Entry(url_frame, textvariable=self.url_var, font=("Arial", 10))
        url_entry.pack(fill="x", pady=5)
        
        # Quality Frame
        quality_frame = tk.Frame(self.root)
        quality_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(quality_frame, text="Select Quality:", font=("Arial", 10)).pack(anchor="w")
        quality_options = ["Audio Only (MP3)", "360p", "480p", "720p", "1080p", "Best Quality"]
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                    values=quality_options, state="readonly", font=("Arial", 10))
        quality_combo.pack(fill="x", pady=5)
        
        # Download Path Frame
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(path_frame, text="Save Location:", font=("Arial", 10)).pack(anchor="w")
        path_display_frame = tk.Frame(path_frame)
        path_display_frame.pack(fill="x", pady=5)
        
        self.path_label = tk.Label(path_display_frame, text=self.download_path, 
                                   font=("Arial", 9), fg="blue", anchor="w")
        self.path_label.pack(side="left", fill="x", expand=True)
        
        browse_btn = tk.Button(path_display_frame, text="Browse", 
                              command=self.browse_folder, font=("Arial", 9))
        browse_btn.pack(side="right", padx=5)
        
        # Progress Frame
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress_bar.pack(fill="x", pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Ready to download", 
                                     font=("Arial", 9), fg="green")
        self.status_label.pack()
        
        # Download Button
        download_btn = tk.Button(self.root, text="Download Video", 
                                command=self.start_download,
                                font=("Arial", 12, "bold"), 
                                bg="#FF0000", fg="white",
                                cursor="hand2", width=20, height=2)
        download_btn.pack(pady=20)
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.path_label.config(text=folder)
    
    def get_download_options(self):
        quality = self.quality_var.get()
        
        if quality == "Audio Only (MP3)":
            messagebox.showwarning("Not Available", "Audio only download requires FFmpeg.\nPlease select a video quality instead.")
            return None
        
        # Always download in 18 format (360p MP4) - most compatible, plays everywhere
        # This is a pre-merged format that doesn't need FFmpeg
        return {
            'format': '18/best[ext=mp4]/mp4',
            'outtmpl': os.path.join(self.download_path, '%(title)s.mp4'),
            'nocheckcertificate': True,
        }
    
    def download_video(self):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        try:
            self.status_label.config(text="Downloading...", fg="orange")
            self.progress_bar.start()
            
            ydl_opts = self.get_download_options()
            
            if ydl_opts is None:
                self.progress_bar.stop()
                self.status_label.config(text="Ready to download", fg="green")
                return
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.progress_bar.stop()
            self.status_label.config(text="Download Complete!", fg="green")
            messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {self.download_path}")
            
        except Exception as e:
            self.progress_bar.stop()
            self.status_label.config(text="Download Failed", fg="red")
            messagebox.showerror("Error", f"Failed to download video:\n{str(e)}")
    
    def start_download(self):
        # Run download in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()