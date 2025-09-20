import tkinter as tk
from tkinter import ttk

class VideoPreviewGenerator:
    def __init__(self, parent, canvas_width=400, canvas_height=300, output_size=(1280, 720), chord_size_ratio=0.4):
        """
        自适应视频预览生成器
        
        参数:
            parent: Tkinter父组件
            canvas_width: 画布固定宽度
            canvas_height: 画布固定高度
            output_size: 输出视频实际尺寸 (宽, 高)
            chord_size_ratio: 和弦视频尺寸占主视频的比例
        """
        self.parent = parent
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.output_size = output_size
        self.chord_size_ratio = chord_size_ratio
        
        # 创建预览画布
        self.canvas = tk.Canvas(
            parent, 
            width=self.canvas_width, 
            height=self.canvas_height, 
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack(pady=10)
        
        # 添加说明标签
        info_text = f"预览布局: 主视频全屏显示，和弦视频显示在四个角落 (尺寸比例: {chord_size_ratio})"
        self.info_label = ttk.Label(parent, text=info_text)
        self.info_label.pack(pady=5)
        
        # 计算布局
        self.calculate_layout()
        
        # 绘制预览布局
        self.draw_preview()
    
    def calculate_layout(self):
        """计算布局尺寸和位置"""
        output_width, output_height = self.output_size
        
        # 计算和弦视频尺寸
        self.chord_width = int(output_width * self.chord_size_ratio)
        self.chord_height = int(output_height * self.chord_size_ratio)
        
        # 计算和弦视频位置
        self.corner_positions = [
            (0, 0),  # 左上角
            (output_width - self.chord_width, 0),  # 右上角
            (0, output_height - self.chord_height),  # 左下角
            (output_width - self.chord_width, output_height - self.chord_height)  # 右下角
        ]
        
        # 计算缩放比例
        self.scale_x = self.canvas_width / self.output_size[0]
        self.scale_y = self.canvas_height / self.output_size[1]
        self.scale = min(self.scale_x, self.scale_y)  # 使用较小的比例保持宽高比
        
        # 计算在画布上的实际显示尺寸
        self.display_width = int(self.output_size[0] * self.scale)
        self.display_height = int(self.output_size[1] * self.scale)
        
        # 计算偏移量以居中显示
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
        # 清除画布
        self.canvas.delete("all")
        
        # 绘制背景区域（表示实际视频尺寸）
        bg_x1, bg_y1, bg_width, bg_height = self.scale_coordinates(0, 0, self.output_size[0], self.output_size[1])
        self.canvas.create_rectangle(
            bg_x1, bg_y1, bg_x1 + bg_width, bg_y1 + bg_height,
            outline="gray", width=1, fill="", dash=(2, 2), tags="bg_rect"
        )
        
        # 绘制主视频区域（全屏）
        main_x1, main_y1, main_width, main_height = self.scale_coordinates(0, 0, self.output_size[0], self.output_size[1])
        self.canvas.create_rectangle(
            main_x1, main_y1, main_x1 + main_width, main_y1 + main_height,
            outline="blue", width=2, fill="", tags="main_video"
        )
        
        # 添加主视频标签
        self.canvas.create_text(
            main_x1 + main_width // 2, main_y1 + 20,
            text="主视频 (全屏)", fill="white", font=("Arial", 10), tags="main_label"
        )
        
        # 绘制四个角落的和弦视频区域
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
            
            # 添加和弦视频标签
            if chord_width > 60 and chord_height > 20:  # 只在足够大的区域显示标签
                self.canvas.create_text(
                    chord_x1 + chord_width // 2, chord_y1 + 12,
                    text=labels[i], fill=colors[i], font=("Arial", 8), tags=f"chord_label_{i}"
                )
    
    def update_parameters(self, output_size=None, chord_size_ratio=None):
        """更新参数并重新绘制预览"""
        if output_size:
            self.output_size = output_size
        
        if chord_size_ratio:
            self.chord_size_ratio = chord_size_ratio
        
        # 重新计算布局
        self.calculate_layout()
        
        # 更新信息标签
        info_text = f"预览布局: 主视频全屏显示，和弦视频显示在四个角落 (尺寸比例: {self.chord_size_ratio})"
        self.info_label.config(text=info_text)
        
        # 重新绘制预览
        self.draw_preview()
        
    def get_parameters(self):
        """获取当前参数"""
        return {
            "output_size": self.output_size,
            "chord_size_ratio": self.chord_size_ratio
        }


# 使用示例函数
def create_video_preview(parent, canvas_width=400, canvas_height=300, output_size=(1280, 720), chord_size_ratio=0.4):
    """
    创建自适应视频预览组件
    
    参数:
        parent: Tkinter父组件
        canvas_width: 画布固定宽度
        canvas_height: 画布固定高度
        output_size: 输出视频实际尺寸 (宽, 高)
        chord_size_ratio: 和弦视频尺寸占主视频的比例
    
    返回:
        VideoPreviewGenerator实例
    """
    return VideoPreviewGenerator(parent, canvas_width, canvas_height, output_size, chord_size_ratio)


# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.title("自适应视频布局预览器")
    
    # 创建控制面板
    control_frame = ttk.Frame(root)
    control_frame.pack(pady=10, fill=tk.X)
    
    # 添加尺寸选择
    ttk.Label(control_frame, text="输出尺寸:").grid(row=0, column=0, padx=5, sticky=tk.W)
    size_var = tk.StringVar(value="1280x720")
    size_combo = ttk.Combobox(control_frame, textvariable=size_var, 
                             values=["640x480", "1280x720", "1920x1080", "3840x2160"])
    size_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
    
    # 添加比例滑块
    ttk.Label(control_frame, text="和弦尺寸比例:").grid(row=0, column=2, padx=5, sticky=tk.W)
    ratio_var = tk.DoubleVar(value=0.4)
    ratio_scale = ttk.Scale(control_frame, from_=0.2, to=0.6, variable=ratio_var, 
                           orient=tk.HORIZONTAL, length=150)
    ratio_scale.grid(row=0, column=3, padx=5, sticky=tk.W)
    ratio_label = ttk.Label(control_frame, text="0.40")
    ratio_label.grid(row=0, column=4, padx=5, sticky=tk.W)
    
    # 创建预览组件 - 固定画布大小
    preview = create_video_preview(root, canvas_width=500, canvas_height=300)
    
    # 更新函数
    def update_preview():
        size_str = size_var.get()
        width, height = map(int, size_str.split('x'))
        ratio = ratio_var.get()
        ratio_label.config(text=f"{ratio:.2f}")
        preview.update_parameters(output_size=(width, height), chord_size_ratio=ratio)
    
    # 添加更新按钮
    update_btn = ttk.Button(control_frame, text="更新预览", command=update_preview)
    update_btn.grid(row=0, column=5, padx=10, sticky=tk.W)
    
    # 比例滑块绑定事件
    def on_ratio_change(event):
        ratio_label.config(text=f"{ratio_var.get():.2f}")
    
    ratio_scale.configure(command=on_ratio_change)
    
    # 尺寸选择绑定事件
    size_combo.bind("<<ComboboxSelected>>", lambda e: update_preview())
    
    # 初始更新
    update_preview()
    
    root.mainloop()