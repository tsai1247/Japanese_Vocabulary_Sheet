import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox  # 添加 messagebox 模块

# 列名的字符串常量
COLUMN_1 = "中文"
COLUMN_2 = "漢字"
COLUMN_3 = "日文"

# 讀取或初始化數據
try:
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    data = []

# 創建主視窗
root = tk.Tk()
root.title("3*n 列表")

# 设置全局字体大小
font_style = ttk.Style()
font_style.configure("Treeview", font=("Arial", 14))  # 设置字体大小

# 创建表格样式
tree_style = ttk.Style()
tree_style.configure("Treeview", background="white", foreground="black")  # 设置表格背景和前景颜色
tree_style.configure("Treeview.Heading", font=("Arial", 14, "bold"))  # 设置表头的字体和样式
tree_style.map("Treeview", background=[("selected", "#A3A3A3")])  # 设置选中行的背景颜色

# 设置表头颜色
tree = ttk.Treeview(root, columns=(COLUMN_1, COLUMN_2, COLUMN_3), show="headings")
tree.heading(COLUMN_1, text=COLUMN_1, anchor="center")
tree.heading(COLUMN_2, text=COLUMN_2, anchor="center")
tree.heading(COLUMN_3, text=COLUMN_3, anchor="center")
tree.pack()

# 创建一个框架来容纳输入框和添加按钮
input_frame = tk.Frame(root)
input_frame.pack(pady=10)  # 增加垂直间距

# 创建输入框样式
entry_style = ttk.Style()
entry_style.configure("Entry.TEntry", font=("Arial", 14))  # 设置输入框的字体大小

# 创建输入框
label1 = tk.Label(input_frame, text=f"{COLUMN_1}:", font=("Arial", 14))
label1.grid(row=0, column=0, padx=5)  # 增加水平间距
entry1 = ttk.Entry(input_frame, font=("Arial", 14), style="Entry.TEntry")
entry1.grid(row=0, column=1, padx=5)  # 增加水平间距

label2 = tk.Label(input_frame, text=f"{COLUMN_2}:", font=("Arial", 14))
label2.grid(row=0, column=2, padx=5)  # 增加水平间距
entry2 = ttk.Entry(input_frame, font=("Arial", 14), style="Entry.TEntry")
entry2.grid(row=0, column=3, padx=5)  # 增加水平间距

label3 = tk.Label(input_frame, text=f"{COLUMN_3}:", font=("Arial", 14))
label3.grid(row=0, column=4, padx=5)  # 增加水平间距
entry3 = ttk.Entry(input_frame, font=("Arial", 14), style="Entry.TEntry")
entry3.grid(row=0, column=5, padx=5)  # 增加水平间距

# 添加行的函数
def add_row():
    value1 = entry1.get().strip()
    value2 = entry2.get().strip()
    value3 = entry3.get().strip()
    
    if value1 and value2 and value3:  # 检查是否都有输入值
        values = [value1, value2, value3]
        tree.insert('', 'end', values=values)
        save_to_json()
        # 清除输入框的文字
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')

# 删除行的函数
def delete_row(event=None):
    selected_items = tree.selection()
    if event is None or messagebox.askyesno("确认删除", "您确定要删除此行吗？"):
        if selected_items:
            for item in selected_items:
                tree.delete(item)
            save_to_json()

# 将新增的内容保存到 JSON 文件中
def save_to_json():
    data = []
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if values:
            data.append(values)
    
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 添加行的按钮
add_button = tk.Button(input_frame, text="添加行", command=add_row, font=("Arial", 14))
add_button.grid(row=0, column=6, padx=5)  # 增加水平间距

# 删除行的按钮
delete_button = tk.Button(input_frame, text="删除选定行", command=delete_row, font=("Arial", 14))
delete_button.grid(row=0, column=7, padx=5)  # 增加水平间距

# 绑定 Enter 键的事件处理程序以保存数据
entry1.bind("<Return>", lambda event=None: add_row())
entry2.bind("<Return>", lambda event=None: add_row())
entry3.bind("<Return>", lambda event=None: add_row())

# 绑定双击行来删除行
tree.bind("<Double-1>", delete_row)

# 初始化表格中的数据
for i, row_data in enumerate(data, start=1):
    tree.insert('', 'end', values=row_data)

# 启动应用程序的主循环
root.mainloop()
