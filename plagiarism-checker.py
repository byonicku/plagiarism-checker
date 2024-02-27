import glob
import os
import csv
from pyunpack import Archive
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import shutil
import psutil
import patoolib as patool

import importlib
REQUIRED_DEPENDENCIES = ["npx"]
REQUIRED_LIBRARIES = ["tkinter", "glob", "csv", "shutil", "psutil", "importlib", "pyunpack", "patoolib"]
LANGUAGE_EXTENSION = {
    "Python": ".py",
    "Java": ".java",
    "C/C++": (".c", ".cpp"),
    "JavaScript": ".js",
    "PHP": ".php"
}
DOLOS_LANGUAGE = {
    "Python": "python",
    "Java": "java",
    "C/C++": "c",
    "JavaScript": "js",
    "PHP": "php"
}

def check_dependencies() -> bool:
    """Check if all required dependencies are installed."""
    for dependency in REQUIRED_DEPENDENCIES:
        if shutil.which(dependency) is None:
            return False
    return True

def check_libraries() -> bool:
    """Check if all required libraries are available."""
    for library in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(library)
        except ImportError:
            return False
    return True

def find_npx_executable() -> str:
    """Find the path to the npx executable."""
    npx_path = shutil.which("npx")
    if npx_path is None:
        raise FileNotFoundError("npx command not found.")
    return npx_path

def run_dolos_command(npx_path: str, folder_path: str, type: str, language: str):
    if type == "new":
        subprocess.Popen([npx_path, "dolos", "-f", "web", "-l", DOLOS_LANGUAGE[language], os.path.join(folder_path, "info.csv"), "-o", os.path.join(folder_path, "dolos-report")])
    else:
        subprocess.Popen([npx_path, "dolos", "serve", folder_path], shell=True)

def find_dolos_process() -> psutil.Process:
    for process in psutil.process_iter(['pid', 'cmdline']):
        if process.info['cmdline'] and 'dolos' in process.info['cmdline']:
            return process
    return None

def close_dolos(window: tk.Tk, status : str):
    dolos_process = find_dolos_process()
    if dolos_process:
        try:
            parent = psutil.Process(dolos_process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
            print("Dolos process terminated successfully.")
        except psutil.NoSuchProcess:
            print("Dolos process not found.")
    else:
        print("Dolos process not found.")

    run_button.configure(state=tk.NORMAL)
    close_button.configure(state=tk.DISABLED)

    if status == "Force":
        window.destroy()

def check_zipped(folder_path: str) -> bool:
    return any(filepath.endswith(".unzipped") for filepath in glob.glob(os.path.join(folder_path, ".unzipped")))

def check_scanned(folder_path: str) -> bool:
    return any(os.path.relpath(filepath,folder_path).startswith("dolos-report") for filepath in glob.glob(os.path.join(folder_path, "*")))
    

def find_compress(folder_path: str) -> bool:
    return any(filepath.endswith(".zip") or filepath.endswith(".rar") for filepath in glob.glob(os.path.join(folder_path, "**", "*"), recursive=True))

def find_report(folder_path: str) -> str:
    for filepath in glob.glob(os.path.join(folder_path, "*")):
        if os.path.relpath(filepath, folder_path).split(os.sep)[0].startswith("dolos-report"):
            return filepath
    return None

def find_extension(folder_path: str, language: str) -> bool:
    return any(filepath.endswith(LANGUAGE_EXTENSION[language]) for filepath in glob.glob(os.path.join(folder_path, "**", "*"), recursive=True))

def extract_compress_main(folder_path: str):
    print("Processing main archive ...")
    for filepath in glob.glob(os.path.join(folder_path, "*.zip")):
        Archive(filepath).extractall(folder_path)
        os.remove(filepath)

def extract_compress_sub(folder_path: str):
    if find_compress(folder_path):
        print("Processing sub archives ...")
        for filepath in glob.glob(os.path.join(folder_path, "**", "*"), recursive=True):
            destination_dir = os.path.relpath(filepath, folder_path).split(os.sep)[0]
            if filepath.endswith(".zip"):
                Archive(filepath).extractall(os.path.join(folder_path, destination_dir))
                os.remove(filepath)
            else:
                for inner in glob.glob(os.path.join(filepath, "*")):
                    if inner.endswith(".rar"):
                        patool.extract_archive(inner, outdir=os.path.join(filepath, destination_dir), verbosity=-1)
                        os.remove(inner)

def to_csv(folder_path: str, language: str):
    with open(os.path.join(folder_path, "info.csv"), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=("full_name", "filename"))
        writer.writeheader()
        for filepath in glob.glob(os.path.join(folder_path, "**", "*"), recursive=True):
            relative_path = os.path.relpath(filepath, folder_path)
            destination_dir = relative_path.split(os.sep)[0]
            if filepath.endswith(LANGUAGE_EXTENSION[language]):
                full_name = destination_dir.split("_")[0]
                writer.writerow({"full_name": full_name, "filename": relative_path.replace('\\', '/')})
                

def run(folder_var : str, language : str):
    folder_path = folder_var
    
    # Check if user haven't selected a language
    if language == "Select Language":
        messagebox.showinfo("Error", "Please Select Your Language!")
        return
    
    # Check if all dependencies are installed
    if not check_dependencies():
        messagebox.showinfo("Error", "Required dependencies are missing.")
        return
    
    # Check if a folder is selected
    if not folder_path:
        messagebox.showinfo("Error", "No folder selected.")
        return
    
    # Check the files in the folder
    if not check_zipped(folder_path):
        open(os.path.join(folder_path, ".unzipped"), "x")
        extract_compress_main(folder_path)
        while(find_compress(folder_path)):
            extract_compress_sub(folder_path)

    # Check to find selected language after unzipping
    if not find_extension(folder_path, language):
        messagebox.showinfo("Error", "Language not found in this folder")
        return
    
    print("Running!")

    if not check_scanned(folder_path):
        print("Processing to csv ...")
        to_csv(folder_path, language)
        try:
            npx_path = find_npx_executable()
            run_dolos_command(npx_path, folder_path, "new", language)
            run_button.configure(state=tk.DISABLED)
            close_button.configure(state=tk.NORMAL)
        except FileNotFoundError as e:
            print(str(e))

        return
    
    report_path = find_report(folder_path)
    if report_path:
        print("Report found:", report_path)
        try:
            npx_path = find_npx_executable()
            run_dolos_command(npx_path, report_path, "else", language)
            run_button.configure(state=tk.DISABLED)
            close_button.configure(state=tk.NORMAL)
        except FileNotFoundError as e:
            print(str(e))
    else:
        print("No report found.")

    print("Dolos process started.")

# Create the GUI window
window = tk.Tk()

# Set window title
window.title("Dolos Report Checker")

# Create a frame for the folder selection
frame = tk.Frame(window)
frame.pack(pady=20)

# Function to handle folder selection
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)

# Label for folder selection
label = tk.Label(frame, text="Select a folder to check:")
label.pack(side=tk.LEFT)

# Entry field to display selected folder
folder_var = tk.StringVar()
folder_entry = tk.Entry(frame, textvariable=folder_var, width=40, state="disabled")
folder_entry.pack(side=tk.LEFT)

# Button to browse for a folder
browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

# Create a frame for the action buttons
action_frame = tk.Frame(window)
action_frame.pack(pady=10)

# Dropdown for language selection
language_var = tk.StringVar()
language_options = ["Python", "Java", "C/C++", "JavaScript", "PHP"]  # Add more options as needed
language_dropdown = tk.OptionMenu(action_frame, language_var, *language_options)
language_var.set("Select Language")
language_dropdown.pack(side=tk.LEFT)

# Button to run the check
run_button = tk.Button(action_frame, text="Run Check", command=lambda: run(folder_var.get(), language_var.get()))
run_button.pack(side=tk.LEFT)

# Button to close Dolos
close_button = tk.Button(action_frame, text="Close Dolos", command=lambda: close_dolos(window, "Normal"), state=tk.DISABLED)
close_button.pack(side=tk.LEFT)

def main():
    if not check_libraries():
        messagebox.showinfo("Error", "Required Python libraries are missing.")
        return
    
    window.protocol("WM_DELETE_WINDOW", lambda: close_dolos(window, "Force"))
    window.mainloop()

if __name__ == "__main__":
    main()