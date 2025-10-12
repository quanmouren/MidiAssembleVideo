from tkinter import ttk
import tkinter as tk
import sys
sys.path.append('gui')
sys.path.append('src')
from Tlog import TLog
log = TLog("界面p2")
class P2Frame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # 响应式布局设置
        for index in [0,1]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        # 加载界面
        self.GUI()

    def GUI(self):
        self.example_label = ttk.Label(self, text="这是预处理界面（p2）")
        self.example_label.grid(row=0, column=0, padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("预览")
    
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    # 加载主题
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")
    # 显示界面
    app = P2Frame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()