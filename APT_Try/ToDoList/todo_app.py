import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from threading import Thread
import time

# ファイル名定義
DATA_FILE = "tasks.json"

# データの読み込み
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"pending": [], "completed": []}

# データの保存
def save_tasks():
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# 通知機能（期限が近づくとポップアップ通知）
def check_deadlines():
    while True:
        current_time = datetime.now()
        for task in tasks["pending"]:
            if "deadline" in task and task["deadline"]:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
                if deadline <= current_time + timedelta(minutes=5):
                    messagebox.showinfo("通知", f"期限が近づいているタスク: {task['text']}")
        time.sleep(60)

# タスクを追加
def add_task():
    task_text = task_entry.get()
    deadline = deadline_entry.get()
    if task_text:
        tasks["pending"].append({"text": task_text, "deadline": deadline})
        task_listbox.insert(tk.END, f"{task_text} (期限: {deadline})")
        task_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("警告", "タスクを入力してください！")

# タスクを削除
def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        del tasks["pending"][selected_index]
        task_listbox.delete(selected_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("警告", "削除するタスクを選んでください！")

# タスクを完了に移動
def complete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        completed_task = tasks["pending"].pop(selected_index)
        tasks["completed"].append(completed_task)
        task_listbox.delete(selected_index)
        completed_listbox.insert(tk.END, completed_task["text"])
        save_tasks()
    except IndexError:
        messagebox.showwarning("警告", "完了するタスクを選んでください！")

# タスクをリロード
def reload_tasks():
    task_listbox.delete(0, tk.END)
    completed_listbox.delete(0, tk.END)
    for task in tasks["pending"]:
        task_listbox.insert(tk.END, f"{task['text']} (期限: {task['deadline']})")
    for task in tasks["completed"]:
        completed_listbox.insert(tk.END, task["text"])

# メインウィンドウの作成
tasks = load_tasks()
root = tk.Tk()
root.title("TODOリスト")
root.geometry("500x500")
root.resizable(True, True)

# ttk.Styleでテーマを設定
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12))

# タブ構成
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ペンディングタブ
pending_frame = ttk.Frame(notebook)
notebook.add(pending_frame, text="タスク一覧")

# 完了済みタブ
completed_frame = ttk.Frame(notebook)
notebook.add(completed_frame, text="完了済みタスク")

# ペンディングタスク
task_label = ttk.Label(pending_frame, text="新しいタスク:")
task_label.pack(pady=5)

task_entry = ttk.Entry(pending_frame, width=40)
task_entry.pack(pady=5)

deadline_label = ttk.Label(pending_frame, text="期限 (例: 2025-01-29 14:30):")
deadline_label.pack(pady=5)

deadline_entry = ttk.Entry(pending_frame, width=40)
deadline_entry.pack(pady=5)

add_button = ttk.Button(pending_frame, text="追加", command=add_task)
add_button.pack(pady=5)

task_listbox = tk.Listbox(pending_frame, width=50, height=15)
task_listbox.pack(pady=10)

delete_button = ttk.Button(pending_frame, text="削除", command=delete_task)
delete_button.pack(side="left", padx=5, pady=5)

complete_button = ttk.Button(pending_frame, text="完了", command=complete_task)
complete_button.pack(side="right", padx=5, pady=5)

# 完了済みタスク
completed_listbox = tk.Listbox(completed_frame, width=50, height=20)
completed_listbox.pack(pady=10)

# タスクのリロード
reload_tasks()

# デッドラインチェック用スレッド
deadline_thread = Thread(target=check_deadlines, daemon=True)
deadline_thread.start()

# メインループの実行
root.mainloop()
