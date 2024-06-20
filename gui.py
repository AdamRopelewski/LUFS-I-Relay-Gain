# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from main import process_files
import threading
import os


def browse_input_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_dir_entry.delete(0, tk.END)
        input_dir_entry.insert(0, directory)


def browse_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, directory)


def update_status(message):
    status_text.config(state=tk.NORMAL)  # Allow modifications temporarily
    status_text.insert(tk.END, message)

    # Find and format LUFS value in bold
    start_idx = status_text.search("] ", tk.END, backwards=True, regexp=True)
    start_idx = status_text.index(f"{start_idx}+2c")  # Move 2 characters forward
    end_idx = status_text.search(" LUFS", start_idx, tk.END, regexp=True)

    if start_idx and end_idx:
        status_text.tag_add("bold", start_idx, end_idx)
        status_text.tag_configure("bold", font=("Arial", 8, "bold"))

    status_text.config(state=tk.DISABLED)  # Disable modifications again
    status_text.see(tk.END)  # Scroll to the end of the text


def start_processing_thread():
    input_dir = input_dir_entry.get()
    output_dir = output_dir_entry.get()
    target_lufs = target_lufs_entry.get()
    target_lufs = target_lufs.replace(",", ".")
    try:
        target_lufs = float(target_lufs)
    except ValueError:
        messagebox.showerror("Error", "Invalid target LUFS.")
        return
    if target_lufs >= 0:
        messagebox.showerror("Error", "Target LUFS must be negative.")
        return

    if os.path.isdir(input_dir) and os.path.isdir(output_dir):
        # Disable the process button
        process_button.config(state=tk.DISABLED)
        delete_button.config(state=tk.DISABLED)
        # Clear previous status messages
        status_text.delete(1.0, tk.END)

        def enable_process_buttons():
            process_button.config(state=tk.NORMAL)
            delete_button.config(state=tk.NORMAL)

        # Start processing in a separate thread
        global process_thread  # Make process_thread a global variable
        process_thread = threading.Thread(
            target=process_files,
            args=(input_dir, output_dir, target_lufs, update_status),
        )

        process_thread.start()

        # Check the thread status periodically
        def check_thread():
            if process_thread.is_alive():
                root.after(100, check_thread)  # Check again after 100ms
            else:
                # Enable the process button when processing is complete
                global flac_files  # Make flac_files a global variable
                flac_files = (
                    process_files()
                )  # Assuming process_thread returns flac_files

                enable_process_buttons()

        root.after(100, check_thread)  # Start checking thread status after 100ms
    else:
        messagebox.showerror("Error", "Invalid input directory.")


def delete_flac_files(output_dir, flac_files):
    for file in flac_files:
        file_path = os.path.join(output_dir, file)
        if os.path.exists(file_path):
            os.remove(file_path)


def delete_flac_files_gui():
    output_dir = output_dir_entry.get()
    if not os.path.isdir(output_dir):
        messagebox.showerror("Error", "Invalid output directory.")
        return
    try:
        if len(flac_files) == 0:
            raise NameError
    except NameError:
        messagebox.showerror("Error", "No .flac files to delete (from this session).")
        return
    if messagebox.askokcancel(
        "Delete FLAC Files", f"Do you want to delete all .flac files in {output_dir}?"
    ):
        delete_flac_files(output_dir, flac_files)
        messagebox.showinfo("Delete Complete", "Deleted all .flac files.")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Check if the processing thread is alive and terminate if necessary
        try:
            process_thread.daemon = True  # Terminate thread
        except:
            pass
        finally:
            root.destroy()


# Set up the main application window
root = tk.Tk()
root.title("FLAC ReplayGain Processor")

# Bind window close event to on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Input directory selection
tk.Label(root, text="Input Directory:").grid(row=0, column=0, padx=10, pady=5)
input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_input_directory)
browse_button.grid(row=0, column=2, padx=10, pady=5)
# Output directory selection

tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_output_directory)
browse_button.grid(row=1, column=2, padx=10, pady=5)


# Target LUFS input
tk.Label(root, text="Target LUFS:").grid(row=2, column=0, padx=10, pady=5)
target_lufs_entry = tk.Entry(root, width=10)
target_lufs_entry.grid(row=2, column=1, padx=10, pady=5)
target_lufs_entry.insert(0, "-14.0")

# Status text display
status_label = tk.Label(root, text="Status:")
status_label.grid(row=3, columnspan=3, padx=10, pady=5)

status_text = tk.Text(root, height=10, width=80, font=("Arial", 8), state=tk.DISABLED)
status_text.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

# Delete FLAC files button
# delete_button = tk.Button(root, text="Delete FLAC Files", command=delete_flac_files_gui)
# delete_button.grid(row=5, columnspan=3, pady=20)

# Process button
process_button = tk.Button(root, text="Process Files", command=start_processing_thread)
process_button.grid(row=6, columnspan=3, pady=20)

# Run the application
root.mainloop()
