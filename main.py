import tkinter as tk
from tkinter import ttk

def add_row():
    values = [entry1.get(), entry2.get(), entry3.get()]
    tree.insert('', 'end', values=values)

# 建立主視窗
root = tk.Tk()
root.title("3*n 列表")

# 創建表格
tree = ttk.Treeview(root, columns=("Column 1", "Column 2", "Column 3"), show="headings")
tree.heading("Column 1", text="Column 1")
tree.heading("Column 2", text="Column 2")
tree.heading("Column 3", text="Column 3")
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

# 添加行的按鈕
add_button = tk.Button(root, text="添加行", command=add_row)
add_button.pack()

# 啟動應用程序的主迴圈
root.mainloop()
