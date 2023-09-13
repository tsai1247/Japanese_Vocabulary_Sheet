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
root.title("日文單字假名紀錄表")

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
tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # 使用grid排版

# 创建一个框架来容纳输入框和添加按钮
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")  # 使用grid排版

# 创建输入框样式
entry_style = ttk.Style()
entry_style.configure("Entry.TEntry", font=("Arial", 14))  # 设置输入框的字体大小

# 创建输入框
label1 = tk.Label(input_frame, text=f"{COLUMN_1}:", font=("Arial", 14))
label1.grid(row=0, column=0, padx=5, pady=5, sticky="e")  # 使用grid排版
entry1 = ttk.Entry(input_frame, font=("Arial", 14), style="Entry.TEntry")
entry1.grid(row=0, column=1, padx=5, pady=5, sticky="w")  # 使用grid排版

label2 = tk.Label(input_frame, text=f"{COLUMN_2}:", font=("Arial", 14))
label2.grid(row=1, column=0, padx=5, pady=5, sticky="e")  # 使用grid排版
entry2 = ttk.Entry(input_frame, font=("Arial", 14), style="Entry.TEntry")
entry2.grid(row=1, column=1, padx=5, pady=5, sticky="w")  # 使用grid排版

label3 = tk.Label(input_frame, text=f"{COLUMN_3}:", font=("Arial", 14))
label3.grid(row=2, column=0, padx=5, pady=5, sticky="e")  # 使用grid排版
entry3 = ttk.Entry(input_frame, font=("Arial", 14), style="Entry.TEntry")
entry3.grid(row=2, column=1, padx=5, pady=5, sticky="w")  # 使用grid排版

# 添加行的函数
def add_row(just_tab=False):
    value1 = entry1.get().strip()
    value2 = entry2.get().strip()
    value3 = entry3.get().strip()
    
    if value1 and value2 and value3 and not just_tab:  # 检查是否都有输入值
        values = [value1, value2, value3]
        tree.insert('', 'end', values=values)
        save_to_json()
        # 清除输入框的文字
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        entry1.focus_set()
    else:
        filter_row()
        focus_next = root.focus_get().tk_focusNext()
        if focus_next:
            if type(focus_next) is not tk.Entry:
                entry3.focus_set()
            else:
                focus_next.focus_set()

# 删除行的函数
def delete_row(event):
    selected_items = tree.selection()
    # 弹出确认警告对话框
    response = messagebox.askyesno("确认删除", "您确定要删除此行吗？")
    if selected_items:
        for item in selected_items:
            tree.delete(item)
        save_to_json()

# 篩選
def filter_row():
    values = [
        entry1.get().strip(),
        entry2.get().strip(),
        entry3.get().strip()
    ]
    allempty = not(values[0] or values[1] or values[2])
    tree.delete(*tree.get_children())
    for i, row_data in enumerate(data, start=1):
        if allempty:
            tree.insert('', 'end', values=row_data)
            continue
        for j in range(len(values)):
            if values[j] and values[j] in row_data[j]:
                tree.insert('', 'end', values=row_data)
                break

    treeview_values = tree.get_children()
    if len(treeview_values):
        tree.selection_set(treeview_values[0])

# 将新增的内容保存到 JSON 文件中
def save_to_json():
    data = []
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if values:
            data.append(values)
    
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 绑定 Enter 键的事件处理程序以保存数据
entry1.bind("<Return>", lambda event=None: add_row())
entry2.bind("<Return>", lambda event=None: add_row())
entry3.bind("<Return>", lambda event=None: add_row())

entry1.bind("<Tab>", lambda event=None: add_row(True))
entry2.bind("<Tab>", lambda event=None: add_row(True))
entry3.bind("<Tab>", lambda event=None: add_row(True))

# 複製內容到輸入框
def copy_to_entry(event):
    item = tree.selection()[0]
    values = tree.item(item, 'values')

    entry1.delete(0, 'end')
    entry1.insert(0, values[0])

    entry2.delete(0, 'end')
    entry2.insert(0, values[1])

    entry3.delete(0, 'end')
    entry3.insert(0, values[2])

# 绑定双击事件以删除行
tree.bind("<Delete>", delete_row)
tree.bind("<Double-1>", copy_to_entry)

# 初始化表格中的数据
for i, row_data in enumerate(data, start=1):
    tree.insert('', 'end', values=row_data)


# 创建一个框架来容纳输入框和添加按钮
display_frame = tk.Frame(root)
display_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")  # 使用grid排版

# 添加用于显示汉字的 Label 和小字标注的 Label
japanese_label = tk.Label(display_frame, text="", font=("Arial", 24))
japanese_label.pack()
# japanese_label.grid(row=0, column=0, padx=10, sticky="s")  # 使用grid排版
hanzi_label = tk.Label(display_frame, text="", font=("Arial", 60))
hanzi_label.pack()
# hanzi_label.grid(row=1, column=0, padx=10, sticky="n")  # 使用grid排版

# 当选择项发生变化时更新汉字和日文标签
def update_labels(event):
    selected_item = tree.selection()[0] if tree.selection() else ""
    values = tree.item(selected_item, "values") if selected_item else []
    
    hanzi = values[1] if values else ""
    japanese = values[2] if values else ""
    
    hanzi_label.config(text=hanzi)
    japanese_label.config(text=f"{japanese}")

tree.bind("<<TreeviewSelect>>", update_labels)

# 启动应用程序的主循环
root.mainloop()
