import tkinter as tk
from tkinter import filedialog, messagebox
from main import *


def process_files(input_dir, target_lufs):
    flac_files = find_flac_files(input_dir)
    for file in flac_files:
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join("output", file)
        integrated_lufs = calculate_lufs_integrated(input_file)
        gain_to_target_lufs = calculate_gain_to_target_lufs(
            integrated_lufs, target_lufs
        )
        copy_file_to_output(input_file, output_file)
        write_replay_gain_flac(input_file, gain_to_target_lufs, output_file)
    messagebox.showinfo("Success", "Processing completed.")


def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_dir_entry.delete(0, tk.END)
        input_dir_entry.insert(0, directory)


def start_processing():
    input_dir = input_dir_entry.get()
    target_lufs = float(target_lufs_entry.get())
    if os.path.isdir(input_dir):
        process_files(input_dir, target_lufs)
    else:
        messagebox.showerror("Error", "Invalid input directory.")


# Set up the main application window
root = tk.Tk()
root.title("FLAC ReplayGain Processor")

# Input directory selection
tk.Label(root, text="Input Directory:").grid(row=0, column=0, padx=10, pady=5)
input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2, padx=10, pady=5)

# Target LUFS input
tk.Label(root, text="Target LUFS:").grid(row=1, column=0, padx=10, pady=5)
target_lufs_entry = tk.Entry(root, width=10)
target_lufs_entry.grid(row=1, column=1, padx=10, pady=5)
target_lufs_entry.insert(0, "-14.0")

# Process button
process_button = tk.Button(root, text="Process Files", command=start_processing)
process_button.grid(row=2, columnspan=3, pady=20)

# Run the application
root.mainloop()
