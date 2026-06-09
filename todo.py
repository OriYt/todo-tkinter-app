"""Simple ToDo list desktop app built with Tkinter.

Features:
- Add tasks
- Mark tasks as done / not done (toggle)
- Delete tasks
- Tasks are saved to a JSON file next to this script, so they persist
  across restarts.

Run with:  python todo.py
"""

import json
import os
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

APP_TITLE = "ToDo List"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo_data.json")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("420x520")
        self.root.minsize(360, 420)

        self.tasks = []  # list of dicts: {"text": str, "done": bool}

        self._build_fonts()
        self._build_ui()
        self.load_tasks()
        self.refresh_list()

    # ----- fonts -----
    def _build_fonts(self):
        self.title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.item_font = tkfont.Font(family="Segoe UI", size=11)
        self.done_font = tkfont.Font(
            family="Segoe UI", size=11, overstrike=1, slant="italic"
        )

    # ----- UI -----
    def _build_ui(self):
        header = tk.Label(self.root, text=APP_TITLE, font=self.title_font)
        header.pack(pady=(14, 8))

        # Entry + Add button
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", padx=14)

        self.entry = tk.Entry(input_frame, font=self.item_font)
        self.entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.entry.bind("<Return>", lambda _e: self.add_task())
        self.entry.focus_set()

        add_btn = tk.Button(
            input_frame, text="Add", width=8, command=self.add_task
        )
        add_btn.pack(side="left", padx=(8, 0))

        # Listbox with scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=14, pady=12)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            font=self.item_font,
            activestyle="none",
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            highlightthickness=0,
            borderwidth=1,
            relief="solid",
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda _e: self.toggle_done())
        scrollbar.config(command=self.listbox.yview)

        # Action buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=14, pady=(0, 14))

        tk.Button(
            btn_frame, text="Toggle Done", command=self.toggle_done
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))
        tk.Button(
            btn_frame, text="Delete", command=self.delete_task
        ).pack(side="left", expand=True, fill="x", padx=(4, 4))
        tk.Button(
            btn_frame, text="Clear Done", command=self.clear_done
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

        self.status = tk.Label(self.root, text="", anchor="w", fg="#666")
        self.status.pack(fill="x", padx=14, pady=(0, 8))

    # ----- actions -----
    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.tasks.append({"text": text, "done": False})
        self.entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_list()

    def _selected_index(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return selection[0]

    def toggle_done(self):
        idx = self._selected_index()
        if idx is None:
            return
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self.save_tasks()
        self.refresh_list(keep=idx)

    def delete_task(self):
        idx = self._selected_index()
        if idx is None:
            return
        task = self.tasks[idx]
        if messagebox.askyesno("Delete", f"Delete this task?\n\n{task['text']}"):
            del self.tasks[idx]
            self.save_tasks()
            self.refresh_list()

    def clear_done(self):
        if not any(t["done"] for t in self.tasks):
            return
        if messagebox.askyesno("Clear Done", "Remove all completed tasks?"):
            self.tasks = [t for t in self.tasks if not t["done"]]
            self.save_tasks()
            self.refresh_list()

    # ----- rendering -----
    def refresh_list(self, keep=None):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            prefix = "\u2714 " if task["done"] else "\u2022 "
            self.listbox.insert(tk.END, prefix + task["text"])
            i = self.listbox.size() - 1
            if task["done"]:
                self.listbox.itemconfig(i, fg="#9aa0a6")
        if keep is not None and 0 <= keep < self.listbox.size():
            self.listbox.selection_set(keep)
        self._update_status()

    def _update_status(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        self.status.config(text=f"{done} / {total} done")

    # ----- persistence -----
    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.tasks = [
                    {"text": str(d.get("text", "")), "done": bool(d.get("done", False))}
                    for d in data
                    if isinstance(d, dict) and d.get("text")
                ]
        except (json.JSONDecodeError, OSError):
            self.tasks = []

    def save_tasks(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except OSError as e:
            messagebox.showerror("Save error", f"Could not save tasks:\n{e}")


def main():
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
