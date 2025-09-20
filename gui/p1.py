from tkinter import ttk
import tkinter as tk
import sys
sys.path.append('gui')
from video_preview_scale import create_video_preview


class P1Frame(ttk.Frame):
    def __init__(self, parent):
        self.和弦方式 = ["四角和弦"]
        super().__init__(parent)
        # 响应式布局设置
        for index in [0]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        # 加载界面
        self.GUI()

    def GUI(self):
        

        self.基础设置Frame = ttk.LabelFrame(self, text="设置", padding=(1, 1))
        self.基础设置Frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.label = ttk.Label(self.基础设置Frame, text="和弦方式：")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.选择和弦方式 = ttk.Combobox(self.基础设置Frame, state="readonly", values=self.和弦方式)
        self.选择和弦方式.current(0)
        self.选择和弦方式.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def 不可编辑下拉选择框_回调(self, event):
        选中的选项 = self.选择和弦方式.get()
        print("选中的选项:", 选中的选项)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("预览")

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    # 加载主题
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")
    # 显示界面
    app = P1Frame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()