import tkinter as tk
from tkinter import filedialog, messagebox
import git
import os
import threading

# Function to clone all branches of a GitHub repo
def clone_branches(repo_url, output_dir):
    try:
        repo = git.Repo.clone_from(repo_url, output_dir)
        origin = repo.remotes.origin
        origin.fetch()

        # Get all branches from the remote
        remote_branches = [ref.name for ref in repo.remotes.origin.refs]
        for branch in remote_branches:
            if "HEAD" not in branch and "master" not in branch:
                branch_name = branch.split("/")[-1]
                branch_dir = os.path.join(output_dir, branch_name)
                git.Repo.clone_from(repo_url, branch_dir, branch=branch_name)
                print(f"Cloned branch: {branch_name}")
        
        messagebox.showinfo("Success", "All branches cloned successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clone branches: {str(e)}")

# Function to handle the "Clone" button click
def start_cloning():
    repo_url = url_entry.get()
    output_dir = directory_entry.get()

    if not repo_url or not output_dir:
        messagebox.showwarning("Input Error", "Please provide both the repo URL and the output directory.")
        return

    # Start cloning in a separate thread to prevent UI blocking
    threading.Thread(target=clone_branches, args=(repo_url, output_dir)).start()

# Function to open a directory picker dialog
def browse_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, selected_dir)

# Set up the tkinter GUI
root = tk.Tk()
root.title("GitHub Branch Cloner")

# GitHub repo URL label and text entry
tk.Label(root, text="GitHub Repo URL:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Output Directory label, text entry, and browse button
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Clone button
clone_button = tk.Button(root, text="Clone All Branches", command=start_cloning)
clone_button.grid(row=2, column=1, padx=10, pady=10)

# Run the GUI
root.mainloop()
