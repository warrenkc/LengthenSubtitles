# The purpose of this code is to lengthen the subtitles for a dual language video.

# File is: new-english.ind.srt
# I need to process the file and create a new file called: new-english-lengthened.ind.srt
# The first subtitle should be lengthened until the second subtitle starts, and so on for all subtitles in the file.
# Keep a space of of at .2 seconds between the end of one subtitle and the start of the next subtitle.

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta

def parse_time(time_str):
    """Parses SRT time format (HH:MM:SS,mmm) into a timedelta object."""
    return datetime.strptime(time_str.strip(), "%H:%M:%S,%f")

def format_time(dt):
    """Formats a datetime object back into SRT time format."""
    # datetime.strftime's %f gives microseconds, we need 3 digits for milliseconds
    s = dt.strftime("%H:%M:%S,%f")
    return s[:-3].replace(".", ",")

def process_srt(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find subtitle blocks: index, times, and text
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n\d+|\n*$)', re.DOTALL)
    matches = list(pattern.finditer(content))

    processed_blocks = []
    
    for i in range(len(matches)):
        index = matches[i].group(1)
        start_time_str = matches[i].group(2)
        end_time_str = matches[i].group(3)
        text = matches[i].group(4)

        start_time = parse_time(start_time_str)
        # By default, keep original end time for the last one
        new_end_time = parse_time(end_time_str)

        if i < len(matches) - 1:
            # Get start time of the next subtitle
            next_start_time = parse_time(matches[i+1].group(2))
            # Subtract 0.2 seconds
            calculated_end = next_start_time - timedelta(seconds=0.2)
            
            # Ensure we don't accidentally shorten it if the gap was already smaller than 0.2
            # or if the original end time was actually later (unlikely in valid SRT but safe)
            if calculated_end > start_time:
                new_end_time = calculated_end

        processed_blocks.append(f"{index}\n{start_time_str} --> {format_time(new_end_time)}\n{text}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(processed_blocks) + "\n")

def select_input_file():
    file_path = filedialog.askopenfilename(
        title="Select SRT File",
        filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save Processed SRT As",
        defaultextension=".srt",
        filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
    )
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def run_processing():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not input_file or not output_file:
        messagebox.showwarning("Warning", "Please select both input and output files.")
        return

    try:
        process_srt(input_file, output_file)
        messagebox.showinfo("Success", f"Processed subtitles saved to:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SRT Subtitle Lengthener")
    root.geometry("500x250")

    # Input File UI
    tk.Label(root, text="Input SRT File:").pack(pady=(20, 0))
    input_frame = tk.Frame(root)
    input_frame.pack(fill="x", padx=20)
    input_entry = tk.Entry(input_frame)
    input_entry.pack(side="left", fill="x", expand=True)
    tk.Button(input_frame, text="Browse...", command=select_input_file).pack(side="right")

    # Output File UI
    tk.Label(root, text="Output SRT File:").pack(pady=(10, 0))
    output_frame = tk.Frame(root)
    output_frame.pack(fill="x", padx=20)
    output_entry = tk.Entry(output_frame)
    output_entry.pack(side="left", fill="x", expand=True)
    tk.Button(output_frame, text="Browse...", command=select_output_file).pack(side="right")

    # Run Button
    tk.Button(root, text="Process SRT", command=run_processing, bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=30)

    root.mainloop()

