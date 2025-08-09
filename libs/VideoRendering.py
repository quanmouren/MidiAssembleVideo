from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
import os
from collections import defaultdict

# 全局视频缓存，key为视频路径，value为加载的视频对象
VIDEO_CACHE = {}

class VideoComposer:
    def __init__(self, output_size=None, background_color=(0, 0, 0)):
        self.clips = []
        self.output_size = output_size
        self.background_color = background_color
        self.max_end_time = 0

    def _get_cached_clip(self, video_path):
        """从缓存获取视频，不存在则加载并缓存"""
        if video_path not in VIDEO_CACHE:
            # 首次加载时存入缓存
            VIDEO_CACHE[video_path] = VideoFileClip(video_path)
        return VIDEO_CACHE[video_path].copy()  # 返回副本避免冲突

    def add_clip(self, video_path, start_time, duration=None, position=(0, 0), custom_size=None):
        """添加视频片段（使用缓存）"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        # 从缓存获取视频
        clip = self._get_cached_clip(video_path)
        
        # 设置持续时间
        if duration is not None:
            clip = clip.set_duration(min(duration, clip.duration))
        
        # 设置时间和位置
        clip = clip.set_start(start_time).set_position(position)
        
        # 初始化输出尺寸（使用第一个视频的尺寸）
        if self.output_size is None:
            self.output_size = clip.size
            
        # 调整尺寸
        target_size = custom_size or self.output_size
        if clip.size != target_size:
            clip = clip.resize(target_size)
            
        # 更新最大结束时间
        end_time = start_time + clip.duration
        if end_time > self.max_end_time:
            self.max_end_time = end_time
            
        self.clips.append(clip)
        return self

    def save(self, output_path, fps=15, codec="libx264", audio_codec="aac", threads=4):
        """保存视频并清理缓存"""
        if not self.clips:
            raise ValueError("没有添加任何视频片段")
            
        # 创建背景
        background = ColorClip(
            size=self.output_size,
            color=self.background_color,
            duration=self.max_end_time
        )
        
        # 合成视频（按添加顺序叠加，底层先加）
        final_clip = CompositeVideoClip([background] + self.clips)
        
        # 保存视频（启用多线程加速）
        final_clip.write_videofile(
            output_path,
            fps=fps or self.clips[0].fps,
            codec=codec,
            audio_codec=audio_codec,
            threads=threads,
            preset="fast"  # 快速编码预设
        )
        
        # 释放资源
        final_clip.close()
        background.close()
        for clip in self.clips:
            clip.close()
        
        # 清空缓存释放内存
        global VIDEO_CACHE
        for clip in VIDEO_CACHE.values():
            clip.close()
        VIDEO_CACHE.clear()


def preload_video_cache(note_names, video_dir="sounds"):
    """预加载所有可能用到的视频到缓存"""
    print(f"预加载 {len(note_names)} 个视频到缓存...")
    global VIDEO_CACHE
    for note_name in note_names:
        video_path = os.path.join(video_dir, f"{note_name}.mp4")
        if video_path not in VIDEO_CACHE and os.path.exists(video_path):
            VIDEO_CACHE[video_path] = VideoFileClip(video_path)
    print(f"缓存完成，当前缓存大小: {len(VIDEO_CACHE)}")


def VideoRendering(notes, video_dir="sounds", sustained=0.3, output_video_path="output_video.mp4", 
                   chord_size_ratio=0.4, start_render_time=None, end_render_time=None):
    """
    渲染MIDI文件为视频
    notes: 音符列表
    video_dir: 视频目录
    sustained: 音符保持时间（延音）
    chord_size_ratio: 和弦视频尺寸占主视频的比例
    start_render_time: 开始渲染的时间点（None表示从开头开始）
    end_render_time: 结束渲染的时间点（None表示渲染到结尾）
    """
    
    # 处理时间范围过滤和偏移
    filtered_notes = []
    time_offset = 0  # 时间偏移量，将指定的开始时间调整为0
    
    if start_render_time is not None:
        time_offset = -start_render_time  # 计算偏移量
        
        for note in notes:
            # 检查音符是否在指定的时间范围内
            note_end = note['end_time']
            note_start = note['start_time']
            
            # 如果音符完全在时间范围外，则跳过
            if (end_render_time is not None and note_start >= end_render_time) or note_end <= start_render_time:
                continue
                
            # 复制音符并调整时间
            adjusted_note = note.copy()
            
            # 调整开始时间（不早于0）
            adjusted_start = max(note_start, start_render_time) + time_offset
            adjusted_note['start_time'] = adjusted_start
            
            # 调整结束时间（不晚于指定的结束时间）
            if end_render_time is not None:
                adjusted_end = min(note_end, end_render_time)
            else:
                adjusted_end = note_end
                
            adjusted_note['end_time'] = adjusted_end + time_offset
            adjusted_note['duration'] = adjusted_note['end_time'] - adjusted_note['start_time']
            
            filtered_notes.append(adjusted_note)
    else:
        # 如果没有指定开始时间，使用所有音符
        filtered_notes = notes.copy()
        
        # 如果指定了结束时间，截断超出部分
        if end_render_time is not None:
            for i in range(len(filtered_notes)):
                note = filtered_notes[i]
                if note['end_time'] > end_render_time:
                    note = note.copy()
                    note['end_time'] = end_render_time
                    note['duration'] = note['end_time'] - note['start_time']
                    filtered_notes[i] = note
    
    if not filtered_notes:
        print("警告：没有符合时间范围的音符，无法生成视频")
        return
    
    # 提取所有唯一音符名称，用于预加载缓存
    unique_note_names = list({note['note_name'] for note in filtered_notes})

    # 预加载视频到缓存
    preload_video_cache(unique_note_names, video_dir)

    # 按开始时间分组（四舍五入到4位小数，处理浮点数精度）
    note_groups = defaultdict(list)
    for note in filtered_notes:
        start_key = round(note['start_time'], 4)
        note_groups[start_key].append(note)

    # 创建合成器并添加片段
    composer = VideoComposer()

    # 处理每个和弦组
    for start_key, group_notes in note_groups.items():
        num_notes = len(group_notes)
        start_time = group_notes[0]['start_time']
        print(f"处理时间点 {start_time:.4f} 的 {num_notes} 个音符")

        # 初始化输出尺寸
        if composer.output_size is None:
            sample_note = group_notes[0]['note_name']
            sample_path = os.path.join(video_dir, f"{sample_note}.mp4")
            composer.output_size = VIDEO_CACHE[sample_path].size
            print(f"输出尺寸: {composer.output_size}")

        output_width, output_height = composer.output_size
        
        # 计算和弦视频尺寸（基于比例）
        chord_width = int(output_width * chord_size_ratio)
        chord_height = int(output_height * chord_size_ratio)
        corner_size = (chord_width, chord_height)  # 和弦视频尺寸
        
        # 计算和弦视频位置（确保完全显示在角落）
        corner_positions = [
            (0, 0),  # 左上角
            (output_width - chord_width, 0),  # 右上角
            (0, output_height - chord_height),  # 左下角
            (output_width - chord_width, output_height - chord_height)  # 右下角
        ]

        # 添加片段（先加角落视频，再加主视频，避免覆盖）
        for i, note in enumerate(group_notes):
            note_name = note['note_name']
            duration = note['duration'] + sustained  # 应用延音
            video_path = os.path.join(video_dir, f"{note_name}.mp4")

            if num_notes == 1:
                # 单个音符：全屏显示
                composer.add_clip(
                    video_path,
                    start_time=start_time,
                    duration=duration,
                    position=(0, 0)
                )
            else:
                if i == 0:
                    # 主音符：全屏显示（顶层）
                    composer.add_clip(
                        video_path,
                        start_time=start_time,
                        duration=duration,
                        position=(0, 0)
                    )
                else:
                    # 和弦音符：角落显示（最多4个）
                    if i-1 < len(corner_positions):
                        composer.add_clip(
                            video_path,
                            start_time=start_time,
                            duration=duration,
                            position=corner_positions[i-1],
                            custom_size=corner_size
                        )
                    else:
                        print(f"警告：超过5个和弦音符，{note_name} 未添加")

    # 保存最终视频（支持GPU加速，需修改codec参数）
    composer.save(output_video_path, threads=16)
    print("视频合成完成！")
    

if __name__ == "__main__":
    import ast
    # 测试用音符数据
    notes_str = '''[{'note_name': 'G5', 'note_number': 79, 'channel': 0, 'velocity': 104, 'start_time': 222.12499999999983, 'track': 2, 'track_name': '轨道', 'end_time': 222.17708333333317, 'duration': 0.05208333333334281}, {'note_name': 'F5', 'note_number': 77, 'channel': 0, 'velocity': 104, 'start_time': 222.18749999999983, 'track': 2, 'track_name': '轨道', 'end_time': 222.23958333333317, 'duration': 0.05208333333334281}, {'note_name': 'D5', 'note_number': 74, 'channel': 0, 'velocity': 104, 'start_time': 222.24999999999983, 'track': 2, 'track_name': '轨道', 'end_time': 222.35937499999983, 'duration': 0.109375}, {'note_name': 'D3', 'note_number': 50, 'channel': 0, 'velocity': 96, 'start_time': 222.37499999999983, 'track': 2, 'track_name': '轨道', 'end_time': 222.42708333333317, 'duration': 0.05208333333334281}, {'note_name': 'G3', 'note_number': 55, 'channel': 0, 'velocity': 96, 'start_time': 222.37499999999983, 'track': 2, 'track_name': '轨道', 'end_time': 222.42708333333317, 'duration': 0.05208333333334281}]'''
    notes = ast.literal_eval(notes_str)
    
    VideoRendering(
        notes,
        video_dir="test\\sounds",
        sustained=3,
        output_video_path="output_video.mp4",
        chord_size_ratio=0.44,  # 和弦视频大小为44%
        start_render_time=222.2,  # 开始时间
        end_render_time=222.4     # 结束时间
    )
