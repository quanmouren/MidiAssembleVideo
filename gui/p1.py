from tkinter import ttk
import tkinter as tk
import sys
from tkinter import filedialog 
sys.path.append('gui')
sys.path.append('src')


from Tlog import TLog
log = TLog("界面p1")

class P1Frame(ttk.Frame):
    def __init__(self, parent):
        self.和弦方式 = ["四角和弦"]
        super().__init__(parent)
        self.选择文件 = ""
        # 响应式布局设置
        for index in [0]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        # 加载界面
        self.GUI()

    def GUI(self):
        def 模块test():
            选中的选项 = self.选择和弦方式.get()
            print("选中的选项:", 选中的选项)
        def 选择midi文件():
            file_path = filedialog.askopenfilename(
                title="选择MIDI文件",
                filetypes=[("MIDI文件", "*.mid *.midi"), ("所有文件", "*.*")]
            )
            if file_path:
                self.选择文件 = file_path
                self.midi文件位置_输入框.delete(0, tk.END)
                self.midi文件位置_输入框.insert(0, file_path)
            log.INFO(f"midi{file_path}")
        def 选择音符片段文件夹():
            folder_path = filedialog.askdirectory(title="选择音符片段文件夹")
            if folder_path:
                self.音符片段文件夹 = folder_path
                self.音符片段_输入框.delete(0, tk.END)
                self.音符片段_输入框.insert(0, folder_path)
            log.INFO(f"音符{folder_path}")

        self.基础设置Frame = ttk.LabelFrame(self, text="设置", padding=(1, 1))
        self.基础设置Frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.label = ttk.Label(self.基础设置Frame, text="和弦方式：")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.选择和弦方式 = ttk.Combobox(self.基础设置Frame, state="readonly", values=self.和弦方式)
        self.选择和弦方式.current(0)
        self.选择和弦方式.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.label1 = ttk.Label(self.基础设置Frame, text="MIDI文件：")
        self.label1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.midi文件位置_输入框 = ttk.Entry(self.基础设置Frame)
        self.midi文件位置_输入框.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.选择midi文件按钮 = ttk.Button(self.基础设置Frame, text="选择文件", command=选择midi文件)
        self.选择midi文件按钮.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.label2 = ttk.Label(self.基础设置Frame, text="音符片段：")
        self.label2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.音符片段_输入框 = ttk.Entry(self.基础设置Frame)
        self.音符片段_输入框.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.选择音符片段文件夹按钮 = ttk.Button(self.基础设置Frame, text="选择文件夹", command=选择音符片段文件夹)
        self.选择音符片段文件夹按钮.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.生成设置Frame = ttk.LabelFrame(self, text="生成", padding=(1, 1))
        self.生成设置Frame.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        #两个tab
        self.生成设置TabControl = ttk.Notebook(self.生成设置Frame)
        self.生成设置TabControl.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.生成设置Tab1 = ttk.Frame(self.生成设置TabControl)
        self.生成设置TabControl.add(self.生成设置Tab1, text="基本")
        #添加一个文本”延音时长“，数字输入框输入时间，在添加一个文本”和弦占比“，数字输入框（取值范围0-1）
        self.延音时长_标签 = ttk.Label(self.生成设置Tab1, text="延音时长：")
        self.延音时长_标签.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.延音时长_输入框 = ttk.Entry(self.生成设置Tab1)
        self.延音时长_输入框.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.和弦占比_标签 = ttk.Label(self.生成设置Tab1, text="和弦占比(0-1)：")
        self.和弦占比_标签.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.和弦占比_输入框 = ttk.Entry(self.生成设置Tab1)
        self.和弦占比_输入框.grid(row=1, column=1, padx=5, pady=5, sticky="w")



        self.生成设置Tab2 = ttk.Frame(self.生成设置TabControl)
        self.生成设置TabControl.add(self.生成设置Tab2, text="高级")
        #添加开始渲染时间和输入框和结束渲染时间和输入框
        self.开始渲染时间_标签 = ttk.Label(self.生成设置Tab2, text="开始渲染时间：")
        self.开始渲染时间_标签.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.开始渲染时间_输入框 = ttk.Entry(self.生成设置Tab2)
        self.开始渲染时间_输入框.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.结束渲染时间_标签 = ttk.Label(self.生成设置Tab2, text="结束渲染时间：")
        self.结束渲染时间_标签.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.结束渲染时间_输入框 = ttk.Entry(self.生成设置Tab2)
        self.结束渲染时间_输入框.grid(row=1, column=1, padx=5, pady=5, sticky="w")


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