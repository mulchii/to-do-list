import tkinter as tk
from storage import load_tasks, save_tasks
from gui import TodoGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To-Do 리스트 앱")

    tasks = load_tasks()
    app = TodoGUI(root, tasks, save_tasks)

    root.mainloop()
