import tkinter as tk
from tkinter import messagebox

class TodoGUI:
    def __init__(self, root, tasks, save_fn):
        self.tasks = tasks
        self.save_tasks = save_fn

        frm = tk.Frame(root)
        frm.pack(padx=10, pady=10)
        self.entry = tk.Entry(frm, width=30)
        self.entry.pack(side=tk.LEFT)
        tk.Button(frm, text="추가", command=self.add_task).pack(side=tk.LEFT, padx=5)

        self.lb = tk.Listbox(root, width=40, height=10)
        self.lb.pack(padx=10, pady=5)
        self.lb.bind("<Double-1>", self.toggle_task)

        tk.Button(root, text="삭제", command=self.delete_task).pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.lb.delete(0, tk.END)
        for t in self.tasks:
            mark = "[✔] " if t.get("done") else "[ ] "
            self.lb.insert(tk.END, mark + t.get("text", ""))

    def add_task(self):
        txt = self.entry.get().strip()
        if not txt:
            messagebox.showwarning("입력 오류", "할 일을 입력하세요.")
            return
        self.tasks.append({"text": txt, "done": False})
        self.save_tasks(self.tasks)
        self.entry.delete(0, tk.END)
        self.refresh_list()

    def toggle_task(self, _event):
        pass

    def delete_task(self):
        idxs = self.lb.curselection()
        for i in reversed(idxs):
            del self.tasks[i]
        self.save_tasks(self.tasks)
        self.refresh_list()
