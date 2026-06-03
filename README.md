# ToDo List (Tkinter desktop app)

A simple cross-platform ToDo list desktop app written in Python with Tkinter.
Works on Windows, macOS and Linux.

## Features

- Add tasks (type and press **Enter**, or click **Add**)
- Toggle a task as done / not done (select it and click **Toggle Done**, or
  double-click the task)
- Delete a selected task
- Clear all completed tasks at once
- Tasks are saved automatically to `todo_data.json` next to the app, so they
  persist across restarts

## Run on Windows

1. Install Python 3 from https://www.python.org/downloads/ (during install,
   check **"Add python.exe to PATH"**). Tkinter is included with the standard
   Windows Python installer.
2. Download `todo.py` (and keep it in its own folder).
3. Double-click `todo.py`, or open a terminal in that folder and run:

   ```
   python todo.py
   ```

## Build a standalone Windows .exe (no Python needed to run)

On a **Windows** machine with Python installed:

```
pip install pyinstaller
pyinstaller --onefile --windowed --name ToDoList todo.py
```

The executable will be created at `dist\ToDoList.exe`. You can double-click it
to run; no Python installation is required on the target machine.

> Note: a Windows `.exe` must be built on Windows (or via Wine). Building on
> Linux/macOS produces an executable for that platform, not a Windows `.exe`.

## Run on Linux / macOS

```
python3 todo.py
```

On some Linux distros you may need to install Tk first, e.g. on Debian/Ubuntu:

```
sudo apt-get install python3-tk
```
