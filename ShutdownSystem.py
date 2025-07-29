import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Logo eklemek için pillow gerekiyor

class ShutdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shutdown Timer")
        self.root.geometry("500x300")
        self.root.minsize(400, 250)
        self.root.configure(bg="#1e1e1e")  # Dark theme
        self.root.iconbitmap("logo.ico")  # Uygulama simgesi

        self.seconds = 0
        self.timer_running = False

        self.create_style()
        self.create_widgets()

    def create_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 12))
        self.style.configure("Timer.TLabel", font=("Segoe UI", 28, "bold"), foreground="#00FFAA", background="#1e1e1e")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6, background="#333", foreground="white")
        self.style.map("TButton", background=[("active", "#444")])

    def create_widgets(self):
        # Giriş etiketi
        ttk.Label(self.root, text="Enter shutdown time (seconds):").grid(row=0, column=0, columnspan=2, pady=(20, 5), padx=20, sticky="w")

        # Giriş alanı
        self.entry = ttk.Entry(self.root, font=("Segoe UI", 12))
        self.entry.grid(row=1, column=0, columnspan=2, padx=20, sticky="ew")

        # Geri sayım etiketi
        self.time_label = ttk.Label(self.root, text="00:00:00", style="Timer.TLabel", anchor="center")
        self.time_label.grid(row=2, column=0, columnspan=2, pady=20)

        # Başlat butonu
        self.start_button = ttk.Button(self.root, text="Start Shutdown", command=self.start_timer)
        self.start_button.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="ew")

        # İptal butonu
        self.cancel_button = ttk.Button(self.root, text="Cancel Shutdown", command=self.cancel_shutdown)
        self.cancel_button.grid(row=3, column=1, padx=(10, 20), pady=10, sticky="ew")

        # Footer
        footer = ttk.Frame(self.root, style="TLabel")
        footer.grid(row=10, column=0, columnspan=2, sticky="se", padx=10, pady=5)

        self.signature_label = ttk.Label(footer, text="Prepared by Xencruel", font=("Segoe UI", 9, "italic"), foreground="#888")
        self.signature_label.pack(anchor="e")

        self.root.grid_rowconfigure(10, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        

        # Grid yapı ölçeklenebilirliği
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def start_timer(self):
        try:
            self.seconds = int(self.entry.get())
            if self.seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number greater than 0.")
            return

        os.system(f"shutdown /s /t {self.seconds}")
        messagebox.showinfo("Timer Started", f"Shutdown scheduled in {self.seconds} seconds.")

        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.seconds >= 0:
            hours = self.seconds // 3600
            minutes = (self.seconds % 3600) // 60
            secs = self.seconds % 60
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{secs:02d}")
            self.seconds -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.time_label.config(text="00:00:00")
            messagebox.showinfo("Shutdown", "The computer is preparing to shutdown...")

    def cancel_shutdown(self):
        os.system("shutdown /a")
        self.timer_running = False
        self.seconds = 0
        self.time_label.config(text="00:00:00")
        messagebox.showinfo("Cancelled", "Shutdown has been cancelled.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTimerApp(root)
    root.mainloop()
