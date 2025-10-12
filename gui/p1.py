from tkinter import ttk
import tkinter as tk
import sys
import os
import random
from tkinter import filedialog 
sys.path.append('gui')
sys.path.append('src')
from parse_midi import parse_midi_notes
from VideoRendering import VideoRendering
from sounds_Inspection import runwebserver



from Tlog import TLog
import cv2
import threading
log = TLog("界面p1")

# 支持的视频文件扩展名
VIDEO_EXTENSIONS = ('.mp4')

class VideoPreviewGenerator:
    def __init__(self, parent, canvas_width=400, canvas_height=300, output_size=(1280, 720), chord_size_ratio=0.4):
        """
        自适应视频预览生成器(四角和弦)
        """
        self.parent = parent
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.output_size = output_size
        self.chord_size_ratio = chord_size_ratio
        self.canvas = tk.Canvas(
            parent, 
            width=self.canvas_width, 
            height=self.canvas_height, 
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.calculate_layout()
        self.draw_preview()
    
    def calculate_layout(self):
        """计算布局尺寸和位置"""
        output_width, output_height = self.output_size
        self.chord_width = int(output_width * self.chord_size_ratio)
        self.chord_height = int(output_height * self.chord_size_ratio)

        self.corner_positions = [
            (0, 0),  # 左上角
            (output_width - self.chord_width, 0),  # 右上角
            (0, output_height - self.chord_height),  # 左下角
            (output_width - self.chord_width, output_height - self.chord_height)  # 右下角
        ]
        self.scale_x = self.canvas_width / self.output_size[0]
        self.scale_y = self.canvas_height / self.output_size[1]
        self.scale = min(self.scale_x, self.scale_y) 
        self.display_width = int(self.output_size[0] * self.scale)
        self.display_height = int(self.output_size[1] * self.scale)
        self.offset_x = (self.canvas_width - self.display_width) // 2
        self.offset_y = (self.canvas_height - self.display_height) // 2
    
    def scale_coordinates(self, x, y, width, height):
        """将实际坐标转换为画布上的缩放坐标"""
        scaled_x = self.offset_x + int(x * self.scale)
        scaled_y = self.offset_y + int(y * self.scale)
        scaled_width = int(width * self.scale)
        scaled_height = int(height * self.scale)
        return scaled_x, scaled_y, scaled_width, scaled_height
    
    def draw_preview(self):
        """绘制预览布局"""
        self.canvas.delete("all")
        
        bg_x1, bg_y1, bg_width, bg_height = self.scale_coordinates(0, 0, self.output_size[0], self.output_size[1])
        self.canvas.create_rectangle(
            bg_x1, bg_y1, bg_x1 + bg_width, bg_y1 + bg_height,
            outline="gray", width=1, fill="", dash=(2, 2), tags="bg_rect"
        )
        main_x1, main_y1, main_width, main_height = self.scale_coordinates(0, 0, self.output_size[0], self.output_size[1])
        self.canvas.create_rectangle(
            main_x1, main_y1, main_x1 + main_width, main_y1 + main_height,
            outline="blue", width=2, fill="", tags="main_video"
        )
        res_text = f"{self.output_size[0]}x{self.output_size[1]}"
        self.canvas.create_text(
            main_x1 + main_width // 2, main_y1 + 20,
            text=f"主视频 (全屏, {res_text})", fill="white", font=("Arial", 10), tags="main_label"
        )
        colors = ["red", "green", "yellow", "cyan"]
        labels = ["和弦视频 1", "和弦视频 2", "和弦视频 3", "和弦视频 4"]
        
        for i, (x, y) in enumerate(self.corner_positions):
            chord_x1, chord_y1, chord_width, chord_height = self.scale_coordinates(
                x, y, self.chord_width, self.chord_height
            )
            
            self.canvas.create_rectangle(
                chord_x1, chord_y1, chord_x1 + chord_width, chord_y1 + chord_height,
                outline=colors[i], width=2, fill="", tags=f"chord_{i}"
            )
            
            if chord_width > 60 and chord_height > 20:
                self.canvas.create_text(
                    chord_x1 + chord_width // 2, chord_y1 + 12,
                    text=labels[i], fill=colors[i], font=("Arial", 8), tags=f"chord_label_{i}"
                )
    
    def update_parameters(self, output_size=None, chord_size_ratio=None):
        """更新参数并重新绘制预览"""
        if output_size:
            self.output_size = output_size
        
        if chord_size_ratio is not None:
            self.chord_size_ratio = chord_size_ratio
        
        self.calculate_layout()

        self.draw_preview()
        
    def get_parameters(self):
        """获取当前参数"""
        return {
            "output_size": self.output_size,
            "chord_size_ratio": self.chord_size_ratio
        }

class P1Frame(ttk.Frame):
    def __init__(self, parent):
        self.和弦方式 = ["","四角和弦"]
        super().__init__(parent)
        self.选择文件 = ""
        self.音符片段文件夹 = ""
        self.preview = None  # 视频预览实例
        self.default_resolution = (1280, 720)  # 默认分辨率
        self.scale_factor = 0.7  # 分辨率缩小比例
        
        # 响应式布局设置
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)  # 预览区域列
        self.rowconfigure(index=0, weight=1)
        
        # 加载界面
        self.GUI()

    def GUI(self):
        def 模块test():
            选中的选项 = self.选择和弦方式.get()
            print("选中的选项:", 选中的选项)
            # 根据和弦方式显示或隐藏预览
            self.update_preview_visibility()
        
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
                
                video_files = self.get_video_files(folder_path)
                if video_files:
                    selected_video = random.choice(video_files)
                    resolution = self.get_video_resolution(selected_video)
                    if resolution:
                        scaled_resolution = (
                            int(resolution[0] * self.scale_factor),
                            int(resolution[1] * self.scale_factor)
                        )
                        log.INFO(f"随机选择视频: {selected_video}, 原始分辨率: {resolution}, 调整后: {scaled_resolution}")
                        
                        if self.preview:
                            self.preview.update_parameters(output_size=scaled_resolution)
                        else:
                            # 如果预览还未创建，先创建再更新
                            self.create_preview(scaled_resolution)
                    else:
                        log.ERROR(f"无法获取视频 {selected_video} 的分辨率，使用默认值")
                else:
                    log.ERROR(f"所选文件夹 {folder_path} 中未找到视频文件，使用默认分辨率")
            
            log.INFO(f"音符片段文件夹: {folder_path}")
        def 生成视频_1():
            log.INFO(f"生成视频_1")
            sustained = float(self.延音时长_输入框.get()) if self.延音时长_输入框.get().strip() else 0.3
            log.DEBUG(f"延音时长: {sustained}")
            chord_size_ratio = float(self.和弦占比_输入框.get()) if self.和弦占比_输入框.get().strip() else 0.4
            log.DEBUG(f"和弦占比: {chord_size_ratio}")
            start_render_time_input = self.开始渲染时间_输入框.get().strip()
            start_render_time = float(start_render_time_input) if start_render_time_input else None
            log.DEBUG(f"开始时间: {start_render_time}")
            end_render_time_input = self.结束渲染时间_输入框.get().strip()
            end_render_time = float(end_render_time_input) if end_render_time_input else None
            log.DEBUG(f"结束时间: {end_render_time}")
            midi_file_path = self.midi文件位置_输入框.get()
            log.DEBUG(f"midi文件位置: {midi_file_path}")
            sounds_file_path = self.音符片段_输入框.get()
            log.DEBUG(f"音符片段文件夹: {sounds_file_path}")
            notes = parse_midi_notes(midi_file_path)
            if self.选择和弦方式.get() == "四角和弦":
                def run_video_rendering():
                    try:
                        VideoRendering(notes, 
                        video_dir=sounds_file_path, 
                        sustained=0.4, 
                        output_video_path="output_video.mp4",
                        chord_size_ratio=0.44, 
                        start_render_time=None,
                        end_render_time=10)
                    except Exception as e:
                        print("运行错误:", e)
                        runwebserver(midi_file_path, sounds_file_path)

                thread = threading.Thread(target=run_video_rendering)
                thread.start()
            
        def create_preview(self, resolution=None):
            if resolution is None:
                resolution = self.default_resolution
            
            self.preview = VideoPreview(self, resolution)
            self.preview.grid(row=0, column=1, rowspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        def on_chord_ratio_change(event=None):
            """和弦占比变化时更新预览"""
            if self.preview and self.选择和弦方式.get() == "四角和弦":
                try:
                    ratio = float(self.和弦占比_输入框.get())
                    # 限制在0-1范围内
                    if 0 <= ratio <= 1:
                        self.preview.update_parameters(chord_size_ratio=ratio)
                except ValueError:
                    pass  # 输入非数字时忽略
        
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        self.基础设置Frame = ttk.LabelFrame(left_frame, text="设置", padding=(1, 1))
        self.基础设置Frame.pack(fill="x", padx=(10, 10), pady=(10, 10))
        
        self.label = ttk.Label(self.基础设置Frame, text="和弦方式：")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.选择和弦方式 = ttk.Combobox(self.基础设置Frame, state="readonly", values=self.和弦方式)
        self.选择和弦方式.current(0)
        self.选择和弦方式.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.选择和弦方式.bind("<<ComboboxSelected>>", lambda e: 模块test())
        
        self.label1 = ttk.Label(self.基础设置Frame, text="MIDI文件：")
        self.label1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.midi文件位置_输入框 = ttk.Entry(self.基础设置Frame)
        self.midi文件位置_输入框.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.选择midi文件按钮 = ttk.Button(self.基础设置Frame, text="选择文件", command=选择midi文件)
        self.选择midi文件按钮.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        self.label2 = ttk.Label(self.基础设置Frame, text="音符片段：")
        self.label2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.音符片段_输入框 = ttk.Entry(self.基础设置Frame)
        self.音符片段_输入框.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.选择音符片段文件夹按钮 = ttk.Button(self.基础设置Frame, text="选择文件夹", command=选择音符片段文件夹)
        self.选择音符片段文件夹按钮.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        self.生成设置Frame = ttk.LabelFrame(left_frame, text="生成", padding=(1, 1))
        self.生成设置Frame.pack(fill="x", padx=(10, 10), pady=(10, 10))
        
        self.生成设置TabControl = ttk.Notebook(self.生成设置Frame)
        self.生成设置TabControl.pack(fill="x", padx=(10, 10), pady=(10, 10))
        
        self.生成设置Tab1 = ttk.Frame(self.生成设置TabControl)
        self.生成设置TabControl.add(self.生成设置Tab1, text="基本")
        
        self.延音时长_标签 = ttk.Label(self.生成设置Tab1, text="延音时长：")
        self.延音时长_标签.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.延音时长_输入框 = ttk.Entry(self.生成设置Tab1)
        self.延音时长_输入框.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.和弦占比_标签 = ttk.Label(self.生成设置Tab1, text="和弦占比(0-1)：")
        self.和弦占比_标签.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.和弦占比_输入框 = ttk.Entry(self.生成设置Tab1)
        self.和弦占比_输入框.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.和弦占比_输入框.insert(0, "0.4")  # 设置默认值

        self.和弦占比_输入框.bind("<FocusOut>", on_chord_ratio_change)
        self.和弦占比_输入框.bind("<Return>", on_chord_ratio_change)
        
        self.生成设置Tab2 = ttk.Frame(self.生成设置TabControl)
        self.生成设置TabControl.add(self.生成设置Tab2, text="高级")
        
        self.开始渲染时间_标签 = ttk.Label(self.生成设置Tab2, text="开始渲染时间：")
        self.开始渲染时间_标签.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.开始渲染时间_输入框 = ttk.Entry(self.生成设置Tab2)
        self.开始渲染时间_输入框.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.结束渲染时间_标签 = ttk.Label(self.生成设置Tab2, text="结束渲染时间：")
        self.结束渲染时间_标签.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.结束渲染时间_输入框 = ttk.Entry(self.生成设置Tab2)
        self.结束渲染时间_输入框.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.preview_frame = ttk.LabelFrame(self, text="视频布局预览", padding=(10, 10))
        self.preview_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)

        self.生成视频按钮 = ttk.Button(self.生成设置Frame, text="生成视频", command=生成视频_1)
        self.生成视频按钮.pack(fill="x", padx=(10, 10), pady=(10, 10))

        # 创建预览组件（使用默认分辨率）
        self.create_preview(self.default_resolution)
        
        # 初始更新预览可见性
        self.update_preview_visibility()
    
    def create_preview(self, resolution):
        """创建预览组件"""
        if self.preview:
            # 移除现有预览
            self.preview.canvas.pack_forget()
            self.preview.info_label.pack_forget()
        
        # 创建新预览
        self.preview = VideoPreviewGenerator(
            self.preview_frame, 
            canvas_width=500, 
            canvas_height=400,
            output_size=resolution
        )
        self.preview.canvas.pack(fill="both", expand=True, pady=(0, 10))
    
    def update_preview_visibility(self):
        """根据和弦方式更新预览的可见性"""
        if self.选择和弦方式.get() == "四角和弦":
            self.preview_frame.grid()  # 显示预览
            # 更新预览比例
            try:
                ratio = float(self.和弦占比_输入框.get())
                if 0 <= ratio <= 1:
                    self.preview.update_parameters(chord_size_ratio=ratio)
            except ValueError:
                pass
        else:
            self.preview_frame.grid_remove()  # 隐藏预览
    
    def get_video_files(self, folder_path):
        """获取文件夹中所有视频文件"""
        video_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(VIDEO_EXTENSIONS):
                    video_files.append(os.path.join(root, file))
        return video_files
    
    def get_video_resolution(self, video_path):
        """
        获取视频文件的分辨率
        使用opencv库获取真实分辨率
        """
        try:
            cap = cv2.VideoCapture(video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            return (width, height)
        except Exception as e:
            # 如果获取分辨率失败，返回None
            print(f"获取视频 {video_path} 分辨率失败: {e}")
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("预览")

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    # 加载主题
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except tk.TclError:
        print("警告: 未找到azure主题，使用默认主题")
        log.ERROR("未找到azure主题，使用默认主题")
    
    # 显示界面
    app = P1Frame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()