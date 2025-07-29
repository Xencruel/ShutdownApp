import os, json, time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import subprocess

ACTIVE_TASK_FILE = "active_task.json"
LOG_FILE = "log.json"

class ShutdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Shutdown Manager")
        self.root.geometry("600x400")
        self.seconds = 0
        self.timer_running = False
        self.task_type = "shutdown"
        self.log_data = self.load_log()

        self.restore_active_task()
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Select Action:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.task_combobox = ttk.Combobox(self.root, values=["Shutdown", "Restart", "Sleep"], state="readonly")
        self.task_combobox.current(0)
        self.task_combobox.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(self.root, text="Enter time (seconds):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry = ttk.Entry(self.root)
        self.entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        self.time_label = ttk.Label(self.root, text="00:00:00", font=("Consolas", 20))
        self.time_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.start_btn = ttk.Button(self.root, text="Start", command=self.start_task)
        self.start_btn.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.cancel_btn = ttk.Button(self.root, text="Cancel", command=self.cancel_task)
        self.cancel_btn.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Log panel
        self.log_box = tk.Listbox(self.root, height=10)
        self.log_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.update_log_panel()

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def start_task(self):
        try:
            self.seconds = int(self.entry.get())
            if self.seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number.")
            return

        self.task_type = self.task_combobox.get().lower()
        self.save_active_task()
        self.add_log("Started")

        cmd = {"shutdown": "shutdown /s /t",
               "restart": "shutdown /r /t",
               #"sleep": subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True, shell=True)}
        }

        if self.task_type == "sleep":
            threading.Timer(self.seconds, self.sleep_computer).start()
        else:
            os.system(f"{cmd[self.task_type]} {self.seconds}")

        if not self.timer_running:
            self.timer_running = True
            self.countdown()

    def countdown(self):
        if self.seconds >= 0:
            h, m, s = self.seconds // 3600, (self.seconds % 3600) // 60, self.seconds % 60
            self.time_label.config(text=f"{h:02}:{m:02}:{s:02}")
            self.seconds -= 1
            self.save_active_task()
            self.root.after(1000, self.countdown)
        else:
            self.timer_running = False
            self.clear_active_task()
            self.add_log("Completed")

    def cancel_task(self):
        os.system("shutdown /a")
        self.seconds = 0
        self.time_label.config(text="00:00:00")
        self.timer_running = False
        self.clear_active_task()
        self.add_log("Cancelled")
        messagebox.showinfo("Cancelled", "Scheduled task was cancelled.")

    def sleep_computer(self):
        try:
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to put computer to sleep:\n{e}")


    def save_active_task(self):
        with open(ACTIVE_TASK_FILE, "w") as f:
            json.dump({
                "seconds_left": self.seconds,
                "task_type": self.task_type,
                "timestamp": time.time()
            }, f)

    def restore_active_task(self):
        try:
            with open(ACTIVE_TASK_FILE, "r") as f:
                data = json.load(f)
                passed = int(time.time() - data["timestamp"])
                self.seconds = max(0, data["seconds_left"] - passed)
                self.task_type = data["task_type"]
                if self.seconds > 0:
                    self.timer_running = True
                    self.countdown()
        except:
            pass

    def clear_active_task(self):
        if os.path.exists(ACTIVE_TASK_FILE):
            os.remove(ACTIVE_TASK_FILE)

    def add_log(self, status):
        entry = {
            "task": self.task_type,
            "status": status,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.log_data.insert(0, entry)
        self.log_data = self.log_data[:10]  # Son 10
        with open(LOG_FILE, "w") as f:
            json.dump(self.log_data, f)
        self.update_log_panel()

    def load_log(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []

    def update_log_panel(self):
        self.log_box.delete(0, tk.END)
        for log in self.log_data:
            self.log_box.insert(tk.END, f"[{log['time']}] {log['task'].capitalize()} - {log['status']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownApp(root)
    root.mainloop()
