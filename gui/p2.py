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
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.Alpha版本测试Label = ttk.Label(left_frame, text="该页为音频分析Alpha版本，功能暂未完善")
        self.Alpha版本测试Label.pack(fill="x", padx=(10, 10), pady=(10, 10))

        self.音频分析Frame = ttk.LabelFrame(left_frame, text="音频分析Alpha", padding=(1, 1))
        self.音频分析Frame.pack(fill="x", padx=(10, 10), pady=(10, 10))

        
        

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