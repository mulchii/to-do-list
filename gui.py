import tkinter as tk
from tkinter import messagebox

PRIORITY_COLORS = {"High":"red","Medium":"orange","Low":"green"}

class TodoGUI:
    def __init__(self, root, tasks, save_fn):
        self.tasks = tasks
        self.save_tasks = save_fn

        frm = tk.Frame(root); frm.pack(padx=10,pady=10)
        self.entry = tk.Entry(frm, width=25); self.entry.pack(side=tk.LEFT)
        self.priority_var = tk.StringVar(value="Medium")
        tk.OptionMenu(frm, self.priority_var, "High","Medium","Low").pack(side=tk.LEFT, padx=5)
        tk.Button(frm, text="추가", command=self.add_task).pack(side=tk.LEFT, padx=5)

        self.lb = tk.Listbox(root, width=50, height=10); self.lb.pack(padx=10,pady=5)
        self.lb.bind("<Double-1>", self.toggle_task)
        tk.Button(root, text="삭제", command=self.delete_task).pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.lb.delete(0, tk.END)
        for idx, t in enumerate(self.tasks):
            prio = t.get("priority", "Medium")
            mark = "[✔] " if t["done"] else "[ ] "
            self.lb.insert(tk.END, f"{mark}[{prio}] {t['text']}")
            self.lb.itemconfig(idx, fg=PRIORITY_COLORS.get(prio, "black"))

    def add_task(self):
        txt = self.entry.get().strip()
        if not txt:
            messagebox.showwarning("입력 오류","할 일을 입력하세요.")
            return
        self.tasks.append({"text":txt,"done":False,"priority":self.priority_var.get()})
        self.save_tasks(self.tasks)
        self.entry.delete(0,tk.END)
        self.refresh_list()

    def toggle_task(self,_):
        idxs = self.lb.curselection()
        if not idxs: return
        i = idxs[0]
        self.tasks[i]["done"] = not self.tasks[i]["done"]
        self.save_tasks(self.tasks)
        self.refresh_list()

    def delete_task(self):
        for i in reversed(self.lb.curselection()):
            del self.tasks[i]
        self.save_tasks(self.tasks)
        self.refresh_list()
