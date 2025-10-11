import tkinter as tk
from tkinter import ttk
from gui.p0 import P0Frame  # 导入p1中的界面框架
from gui.p1 import P1Frame



class MainApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # 配置主窗口布局
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # 创建标签页控件，用于管理多个界面
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # 添加第一个界面（从p1导入）
        self.p0_frame = P0Frame(self.notebook)
        self.notebook.add(self.p0_frame, text="测试界面")

        # 添加第一个界面（从p1导入）
        self.p1_frame = P1Frame(self.notebook)
        self.notebook.add(self.p1_frame, text="测试界面")
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("主应用程序")
    #root.geometry("800x600")  # 主窗口初始大小
    # 设置窗口的最小尺寸，并将其放置在屏幕中央
    root.update()
    # 设置窗口的最小宽度和高度为当前窗口的宽度和高度，防止用户将窗口缩放到太小而无法正常显示
    root.minsize(root.winfo_width(), root.winfo_height())
    
    # 加载主题
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except tk.TclError:
        print("未找到azure主题，使用默认主题")
    
    app = MainApp(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()