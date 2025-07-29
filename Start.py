import os
import tkinter as tk
from tkinter import messagebox
import time

def main ():
    print("Shutdown Timer System")
    

def shutdown():
    try:
        seconds =int(entry.get())
        if seconds <= 0:
            raise ValueError
        os.system(f"shutdown /s /t {seconds}")
        messagebox.showinfo("Shutdown Timer Started...",f"The device shutdown in {seconds}")
        except ValueError:
            messagebox.showerror("ValueError","Please enter value for seconds")
        
        def timer():
            nonlocal seconds
            if seconds >= 0:
                hours = seconds //3600
                minutes =(seconds % 3600) //60
                second = second %60

                time_str = f"{hours:02d}:{minutes:02d}:{second:02d}"
                label.config(text=time_str)
                total_seconds -=1
                root.after (1000,timer)
            else:
                messagebox.showinfo("The computer is preparing to shutdown")
        
        timer()

def Cancel():
    os.system("shutdown /a")
    messagebox.showinfo("Canceled shutdown")


    