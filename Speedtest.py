import tkinter as tk
from tkinter import ttk
import speedtest
import threading

class SpeedTestApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Speed Test App")
        self.geometry("1000x700")  
        self.configure(bg="#000000")

        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#000000")
        self.style.configure("TButton", font=("Helvetica", 18), background="#3498db", foreground="#ffffff", padding=12, relief="flat")
        self.style.map("TButton", background=[("active", "#2980b9")])
        self.style.configure("TLabel", background="#000000", foreground="#ffffff")
        self.style.configure("TProgressbar", thickness=25, background="#3498db") 

        self.main_frame = ttk.Frame(self, padding="30")
        self.main_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(self.main_frame, text="Internet Speed Test", font=("Helvetica", 36, "bold"))  
        title_label.pack(pady=(0, 40))

        self.speed_frame = ttk.Frame(self.main_frame)
        self.speed_frame.pack(fill="x", pady=30)

        self.download_label = ttk.Label(self.speed_frame, text="Download: -- Mbps", font=("Helvetica", 24)) 
        self.download_label.pack()

        self.upload_label = ttk.Label(self.speed_frame, text="Upload: -- Mbps", font=("Helvetica", 24))
        self.upload_label.pack()

        self.ping_label = ttk.Label(self.speed_frame, text="Ping: -- ms", font=("Helvetica", 24))
        self.ping_label.pack()

        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill="x", pady=50)

        self.progress_label = ttk.Label(self.progress_frame, text="", font=("Helvetica", 22))  
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=700, mode="determinate") 
        self.progress_bar.pack(pady=20)

        self.start_button = ttk.Button(self.main_frame, text="Start Test", command=self.start_test, style="TButton")
        self.start_button.pack(pady=30) 

    def start_test(self):
        self.start_button.config(state="disabled")
        self.update_labels("Testing...", "Testing...", "Testing...")
        self.progress_bar["value"] = 0
        thread = threading.Thread(target=self.run_speed_test)
        thread.start()

    def run_speed_test(self):
        speed_test = speedtest.Speedtest()

        self.animate_progress("Testing download speed", "#3498db")
        download = speed_test.download() / 1_000_000
        self.update_download(f"{download:.2f}")

        self.animate_progress("Testing upload speed", "#2ecc71")
        upload = speed_test.upload() / 1_000_000 
        self.update_upload(f"{upload:.2f}")

        self.animate_progress("Measuring ping", "#e74c3c")
        ping = speed_test.results.ping
        self.update_ping(f"{ping:.2f}")

        self.progress_label.config(text="Test completed!")
        self.start_button.config(state="normal")

    def animate_progress(self, message, color):
        self.progress_label.config(text=message)
        self.style.configure("TProgressbar", background=color)
        self.progress_bar["value"] = 0
        self.update_idletasks()

        for i in range(100):
            self.progress_bar["value"] = i + 1
            self.update_idletasks()
            self.after(10)

    def update_labels(self, download, upload, ping):
        self.download_label.config(text=f"Download: {download}")
        self.upload_label.config(text=f"Upload: {upload}")
        self.ping_label.config(text=f"Ping: {ping}")

    def update_download(self, value):
        self.download_label.config(text=f"Download: {value} Mbps")

    def update_upload(self, value):
        self.upload_label.config(text=f"Upload: {value} Mbps")

    def update_ping(self, value):
        self.ping_label.config(text=f"Ping: {value} ms")

if __name__ == "__main__":
    app = SpeedTestApp()
    app.mainloop()





