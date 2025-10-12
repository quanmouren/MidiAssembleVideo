import tkinter as tk
from tkinter import ttk
from gui.p0 import P0Frame
from gui.p1 import P1Frame
from gui.p2 import P2Frame
from gui.p3 import P3Frame

class MainApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # 添加第一个界面（从p1导入）
        self.p1_frame = P1Frame(self.notebook)
        self.notebook.add(self.p1_frame, text="midi合成")
        # 添加第二个界面（从p2导入）
        self.p2_frame = P2Frame(self.notebook)
        self.notebook.add(self.p2_frame, text="预处理")
        # 添加第三个界面（从p3导入）
        self.p3_frame = P3Frame(self.notebook)
        self.notebook.add(self.p3_frame, text="测试用")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("主应用程序")
    root.update()
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