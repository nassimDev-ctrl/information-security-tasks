import os
import json
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ---------------------------
# مساعدة: تنسيق الأحجام
# ---------------------------
def human_size(num_bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

# ---------------------------
# فتح ملف/مجلد في مستعرض النظام
# ---------------------------
def open_in_explorer(path):
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open:\n{e}")

# ---------------------------
# DFS: بناء لائحة أسطر مع المسارات والأحجام
# كل عنصر في lines سيكون tuple: (text_line, full_path_or_None)
# ---------------------------
def dfs_build_lines(path, indent=0):
    """
    Returns: (total_size_bytes, lines_list)
    where lines_list = [(text_line, path_for_line), ...]
    For directory line, path_for_line = full_dir_path
    For file line, path_for_line = full_file_path
    For error lines, path_for_line = None
    """
    name = os.path.basename(path) or path
    lines = []

    # Attempt to list items; if permission denied, show message and return size 0
    try:
        items = os.listdir(path)
    except PermissionError:
        lines.append(("  " * indent + f"{name}/ [ACCESS DENIED]", None))
        return 0, lines
    except OSError as e:
        # Other OS errors, treat similarly
        lines.append(("  " * indent + f"{name}/ [ERROR: {e}]", None))
        return 0, lines

    # Sort: directories first, then files (alphabetical)
    items_sorted = sorted(items, key=lambda s: (not os.path.isdir(os.path.join(path, s)), s.lower()))

    total_size = 0
    child_lines = []

    # First, process directories and files to collect child lines and compute total_size
    for item in items_sorted:
        full = os.path.join(path, item)
        if os.path.isdir(full):
            # Recurse into subdirectory
            sub_size, sub_lines = dfs_build_lines(full, indent + 1)
            total_size += sub_size
            # Prepend the subdirectory header (we want header with size) — sub_lines already includes its header
            child_lines.extend(sub_lines)
        else:
            # File: get size (catch possible OSError)
            try:
                fsize = os.path.getsize(full)
            except OSError:
                fsize = 0
            total_size += fsize
            # Append file line with its path
            child_lines.append(("  " * (indent + 1) + f"{item} ({human_size(fsize)})", full))

    # Now create header for current directory with cumulative size
    header = "  " * indent + f"{name}/ ({human_size(total_size)})"
    # The header line should map to the directory path
    lines.append((header, path))
    # Then add all child lines
    lines.extend(child_lines)

    return total_size, lines

# ---------------------------
# DFS -> JSON builder (with sizes)
# ---------------------------
def dfs_to_json(path):
    node = {"name": os.path.basename(path) or path, "type": "directory", "children": []}
    try:
        items = os.listdir(path)
    except PermissionError:
        node["error"] = "ACCESS DENIED"
        return node
    except OSError as e:
        node["error"] = f"ERROR: {e}"
        return node

    items_sorted = sorted(items, key=lambda s: (not os.path.isdir(os.path.join(path, s)), s.lower()))
    for item in items_sorted:
        full = os.path.join(path, item)
        if os.path.isdir(full):
            node["children"].append(dfs_to_json(full))
        else:
            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0
            node["children"].append({"name": item, "type": "file", "size_bytes": size, "size": human_size(size)})
    # Optionally: compute cumulative size of directory (sum of children) and add to node
    total = 0
    for c in node["children"]:
        if c["type"] == "file":
            total += c["size_bytes"]
        else:
            # if directory, we can sum "size" if present; but dfs_to_json for subdirs doesn't include cumulative size currently
            # to keep it simple, don't compute recursively here (could be expensive)
            pass
    return node

# ---------------------------
# GUI class
# ---------------------------
class SimpleDFSExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple DFS File Explorer (with sizes & open-on-doubleclick)")
        self.root.geometry("860x640")
        self.root.minsize(700, 500)

        self.current_path = None
        self.theme = "light"

        # mapping: line_number (1-based) -> full_path
        self.line_to_path = {}

        # themes
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "btn_bg": "#f0f0f0",
                "txt_bg": "#ffffff",
                "txt_fg": "#000000"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#e6e6e6",
                "btn_bg": "#3b3b3b",
                "txt_bg": "#1e1e1e",
                "txt_fg": "#e6e6e6"
            }
        }

        # UI
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=8)

        btn_choose = tk.Button(top_frame, text="Choose Folder", command=self.choose_folder, width=15)
        btn_choose.pack(side=tk.LEFT, padx=4)

        self.open_btn = tk.Button(top_frame, text="Open Folder", command=self.open_folder, width=12, state=tk.DISABLED)
        self.open_btn.pack(side=tk.LEFT, padx=4)

        tk.Label(top_frame, text="  ").pack(side=tk.LEFT)  # spacer

        self.theme_btn = tk.Button(top_frame, text="Dark Theme", command=self.toggle_theme, width=12)
        self.theme_btn.pack(side=tk.LEFT, padx=4)

        tk.Label(top_frame, text="  ").pack(side=tk.LEFT)

        self.export_txt_btn = tk.Button(top_frame, text="Export TXT", command=self.export_txt, width=12, state=tk.DISABLED)
        self.export_txt_btn.pack(side=tk.LEFT, padx=4)

        self.export_json_btn = tk.Button(top_frame, text="Export JSON", command=self.export_json, width=12, state=tk.DISABLED)
        self.export_json_btn.pack(side=tk.LEFT, padx=4)

        # path label
        self.path_label = tk.Label(root, text="Selected: None", anchor="w")
        self.path_label.pack(fill=tk.X, padx=12)

        # output text box (scrolled)
        self.output = scrolledtext.ScrolledText(root, wrap=tk.NONE, width=120, height=35)
        self.output.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # bind double-click on output to open file/folder
        self.output.bind("<Double-Button-1>", self.on_double_click)

        # bottom status
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=6)
        self.status_label = tk.Label(bottom_frame, text="Ready", anchor="w")
        self.status_label.pack(side=tk.LEFT)

        # apply theme
        self.apply_theme()

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_path = folder
            self.path_label.config(text=f"Selected: {self.current_path}")
            self.open_btn.config(state=tk.NORMAL)
            self.export_txt_btn.config(state=tk.NORMAL)
            self.export_json_btn.config(state=tk.NORMAL)
            self.show_tree()
        else:
            self.status_label.config(text="No folder selected")

    def open_folder(self):
        if self.current_path:
            open_in_explorer(self.current_path)

    def show_tree(self):
        if not self.current_path:
            messagebox.showwarning("Warning", "Choose a folder first")
            return
        self.status_label.config(text="Exploring... (may take time for large folders)")
        self.root.update_idletasks()

        try:
            # build lines via DFS (each line paired with path info)
            _, lines = dfs_build_lines(self.current_path, indent=0)

            # clear previous mapping and output
            self.line_to_path.clear()
            self.output.configure(state=tk.NORMAL)
            self.output.delete(1.0, tk.END)

            # insert lines one by one and map line numbers to paths
            for i, (text_line, path_for_line) in enumerate(lines, start=1):
                # insert the line
                self.output.insert(tk.END, text_line + "\n")
                # map the line number to path (if present)
                if path_for_line:
                    self.line_to_path[i] = path_for_line

            self.status_label.config(text=f"Done. Lines: {len(lines)}")
            # move view to top
            self.output.yview_moveto(0.0)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Error during exploration")

    def export_txt(self):
        if not self.current_path:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="dfs_tree.txt",
                                            initialdir=self.current_path, filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            _, lines = dfs_build_lines(self.current_path, indent=0)
            txt = "\n".join([ln for ln, p in lines])
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            messagebox.showinfo("Exported", f"TXT exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export TXT:\n{e}")

    def export_json(self):
        if not self.current_path:
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="dfs_tree.json",
                                            initialdir=self.current_path, filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            tree = dfs_to_json(self.current_path)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(tree, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Exported", f"JSON exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export JSON:\n{e}")

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
        # update button text
        self.theme_btn_text_update()

    def apply_theme(self):
        t = self.themes[self.theme]
        self.root.configure(bg=t["bg"])
        # Apply to top-level widgets
        for w in self.root.winfo_children():
            try:
                w.configure(bg=t["bg"], fg=t["fg"])
            except Exception:
                pass
        # path label & status
        self.path_label.configure(bg=t["bg"], fg=t["fg"])
        self.status_label.configure(bg=t["bg"], fg=t["fg"])
        # text box
        self.output.configure(bg=t["txt_bg"], fg=t["txt_fg"], insertbackground=t["txt_fg"])
        # buttons: set color for top frame children if possible
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, tk.Button):
                        try:
                            btn.configure(bg=self.themes[self.theme]["btn_bg"], fg=self.themes[self.theme]["fg"])
                        except Exception:
                            pass

    def theme_btn_text_update(self):
        # find the theme button and update its text accordingly
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, tk.Button) and btn.cget("command") == self.toggle_theme:
                        # not reliable to compare command; instead we update the button we created earlier by text matching
                        pass
        # simpler: change label of the stored theme button by searching text
        # (we don't keep a direct reference to theme button here; but its text was "Dark Theme" initially)
        # We'll iterate and change any button that currently shows "Dark Theme" or "Light Theme"
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, tk.Button):
                        txt = btn.cget("text")
                        if txt in ("Dark Theme", "Light Theme"):
                            btn.config(text="Dark Theme" if self.theme == "light" else "Light Theme")

    def on_double_click(self, event):
        # get index under mouse click
        try:
            index = self.output.index(f"@{event.x},{event.y}")
            line_str = index.split(".")[0]
            line_no = int(line_str)
        except Exception:
            return
        # get path mapped to this line
        path = self.line_to_path.get(line_no)
        if not path:
            # nothing mapped to this line
            return
        # If it's a file, ask to open it; if it's a dir, open folder
        if os.path.isfile(path):
            # confirm opening file
            if messagebox.askyesno("Open File", f"Open file?\n{path}"):
                open_in_explorer(path)
        elif os.path.isdir(path):
            if messagebox.askyesno("Open Folder", f"Open folder in explorer?\n{path}"):
                open_in_explorer(path)

# ---------------------------
# تشغيل التطبيق
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDFSExplorer(root)
    root.mainloop()
