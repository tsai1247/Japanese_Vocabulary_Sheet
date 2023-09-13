import tkinter as tk
from tkinter import ttk
import json

# 讀取或初始化數據
try:
    with open("data.json", "r") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    data = []

# 創建主視窗
root = tk.Tk()
root.title("3*n 列表")

# 創建表格
tree = ttk.Treeview(root, columns=("Column 1", "Column 2", "Column 3", "操作"), show="headings")
tree.heading("Column 1", text="Column 1")
tree.heading("Column 2", text="Column 2")
tree.heading("Column 3", text="Column 3")
tree.heading("操作", text="操作")
tree.pack()

# 創建輸入框
label1 = tk.Label(root, text="Column 1:")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Column 2:")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

label3 = tk.Label(root, text="Column 3:")
label3.pack()
entry3 = tk.Entry(root)
entry3.pack()

# 初始化表格中的數據
for row_data in data:
    tree.insert('', 'end', values=row_data + ("刪除",))

# 添加行的函數
def add_row():
    values = (entry1.get(), entry2.get(), entry3.get(), "刪除")
    tree.insert('', 'end', values=values)
    save_to_json()

# 刪除行的函數
def delete_row():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        save_to_json()

# 將新增的內容保存到 JSON 文件中
def save_to_json():
    data = []
    for item in tree.get_children():
        values = tree.item(item, 'values')[:-1]  # 去掉最後一個 "刪除"
        if values:
            data.append(values)
    
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

# 添加行的按鈕
add_button = tk.Button(root, text="添加行", command=add_row)
add_button.pack()

# 刪除行的按鈕
delete_button = tk.Button(root, text="刪除選定行", command=delete_row)
delete_button.pack()

# 啟動應用程序的主迴圈
root.mainloop()
