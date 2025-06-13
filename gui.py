import tkinter as tk
from tkinter import messagebox, ttk

# 핵심 매핑: 키(High/Medium/Low) → 별 표현
PRIORITY_STARS = {
    "High": "★★★",
    "Medium": "★★",
    "Low": "★"
}

class TodoGUI:
    def __init__(self, root, tasks, save_fn):
        self.tasks = tasks
        self.save_tasks = save_fn

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=6)
        style.configure('Treeview', rowheight=24, font=('Helvetica', 10))
        style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'))

        top = ttk.Frame(root, padding=10)
        top.pack(fill='x')

        self.entry = ttk.Entry(top)
        self.entry.pack(side='left', expand=True, fill='x')
        self.entry.insert(0, '할 일을 입력하세요...')
        self.entry.bind('<FocusIn>', lambda e: self.entry.delete(0, 'end'))

        # 우선순위 키 저장: High/Medium/Low
        self.priority_var = tk.StringVar(value='Medium')
        ttk.OptionMenu(top, self.priority_var, 'High', 'Medium', 'Low')\
            .pack(side='left', padx=8)

        ttk.Button(top, text='추가', command=self.add_task).pack(side='left')

        cols = ('완료', '중요도', '할일')
        self.tree = ttk.Treeview(
            root, columns=cols, show='headings', selectmode='extended'
        )
        for col in cols:
            width = 60 if col != '할일' else 200
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        self.tree.pack(padx=10, pady=10, expand=True, fill='both')
        self.tree.bind('<Double-1>', self.toggle_task)

        bottom = ttk.Frame(root, padding=(10, 0, 10, 10))
        bottom.pack(fill='x')
        ttk.Button(bottom, text='삭제', command=self.delete_task).pack(side='left')
        ttk.Button(
            bottom, text='완료된 항목 모두 삭제',
            command=self.clear_completed
        ).pack(side='right')

        self.refresh_list()

    def refresh_list(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for t in self.tasks:
            done_mark = '✔' if t['done'] else ''
            key = t.get('priority', 'Medium')
            # 키를 별 문자열로 매핑, 없으면 그대로
            stars = PRIORITY_STARS.get(key, key)
            text = t['text']
            self.tree.insert(
                '', 'end',
                values=(done_mark, stars, text)
            )

    def add_task(self):
        txt = self.entry.get().strip()
        if not txt or txt == '할 일을 입력하세요...':
            messagebox.showwarning("입력 오류", "할 일을 입력하세요.")
            return
        self.tasks.append({
            'text': txt,
            'done': False,
            'priority': self.priority_var.get()  # "High"/"Medium"/"Low"
        })
        self.save_tasks(self.tasks)
        self.entry.delete(0, 'end')
        self.refresh_list()

    def toggle_task(self, _):
        sel = self.tree.selection()
        for iid in sel:
            idx = self.tree.index(iid)
            self.tasks[idx]['done'] = not self.tasks[idx]['done']
        self.save_tasks(self.tasks)
        self.refresh_list()

    def delete_task(self):
        sel = list(self.tree.selection())[::-1]
        for iid in sel:
            idx = self.tree.index(iid)
            del self.tasks[idx]
        self.save_tasks(self.tasks)
        self.refresh_list()

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t['done']]
        self.save_tasks(self.tasks)
        self.refresh_list()
