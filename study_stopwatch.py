import tkinter as tk
from datetime import datetime
import json
import os

# File to store study logs
LOG_FILE = "study_log.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_log():
    global start_time, total_time
    if start_time:
        elapsed = (datetime.now() - start_time).seconds
        total_time += elapsed
    
    today = datetime.now().strftime("%Y-%m-%d")
    logs = load_logs()
    logs[today] = logs.get(today, 0) + total_time
    
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)
    
    reset_timer()

def reset_timer():
    global start_time, total_time
    start_time = None
    total_time = 0
    timer_label.config(text="00:00:00")

def start_timer():
    global start_time
    if start_time is None:
        start_time = datetime.now()
    update_timer()

def stop_timer():
    global start_time, total_time
    if start_time:
        elapsed = (datetime.now() - start_time).seconds
        total_time += elapsed
    start_time = None

def update_timer():
    if start_time:
        elapsed = (datetime.now() - start_time).seconds + total_time
        timer_label.config(text=format_time(elapsed))
        root.after(1000, update_timer)

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def show_history():
    logs = load_logs()
    history_window = tk.Toplevel(root)
    history_window.title("Study History")
    text = tk.Text(history_window, width=40, height=15)
    text.pack()
    text.insert(tk.END, "Date\tTotal Time (hh:mm:ss)\n")
    text.insert(tk.END, "-" * 30 + "\n")
    
    for date, seconds in logs.items():
        text.insert(tk.END, f"{date}\t{format_time(seconds)}\n")
    text.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Study Stopwatch")
root.geometry("300x250")

timer_label = tk.Label(root, text="00:00:00", font=("Arial", 24))
timer_label.pack(pady=20)

start_button = tk.Button(root, text="Start", command=start_timer)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_timer)
stop_button.pack()

save_button = tk.Button(root, text="Save & Reset", command=save_log)
save_button.pack()

history_button = tk.Button(root, text="Show History", command=show_history)
history_button.pack()

start_time = None
total_time = 0

root.mainloop()
