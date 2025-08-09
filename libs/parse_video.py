import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import os
import tempfile

def parse_piano_video(video_path, output_dir, min_duration=0.3, volume_threshold=0.05):
    """
    处理钢琴原始视频,拆分音符片段并识别音高
    - video_path: 输入视频路径
    - output_dir: 输出目录
    - min_duration: 最小片段持续时间(秒)
    - volume_threshold: 音量阈值(0-1)，低于此值视为静音
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载视频并提取音频
    video = VideoFileClip(video_path)
    
    # 临时保存音频文件用于分析
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
        temp_audio_path = tmp_audio.name
    
    video.audio.write_audiofile(temp_audio_path, fps=44100)
    y, sr = librosa.load(temp_audio_path, sr=44100)
    
    # 计算音频能量(音量)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)
    rms_normalized = rms / np.max(rms)
    
    # 检测音符起始点
    onset_frames = librosa.onset.onset_detect(
        y=y, 
        sr=sr,
        units='time',
        pre_max=3,
        post_max=3,
        pre_avg=3,
        post_avg=3,
        delta=0.2,
        wait=0.1
    )
    
    # 筛选有效的起始点
    valid_onsets = []
    for onset in onset_frames:
        # 找到最近的RMS时间点
        idx = np.argmin(np.abs(times - onset))
        if rms_normalized[idx] >= volume_threshold:
            valid_onsets.append(onset)
    
    # 确定切割时间点(确保最小持续时间)
    cut_points = []
    for i in range(len(valid_onsets)):
        start = max(0, valid_onsets[i] - 0.1)  # 开始前0.1秒
        
        # 确定结束时间
        if i < len(valid_onsets) - 1:
            end = min(valid_onsets[i+1] - 0.2, start + 5)  # 不超过5秒
        else:
            end = min(len(y)/sr, start + 5)
        
        # 检查持续时间是否足够
        if end - start >= min_duration:
            # 检查片段平均音量是否足够
            segment_rms = np.mean(rms_normalized[
                (times >= start) & (times <= end)
            ])
            
            if segment_rms >= volume_threshold:
                cut_points.append((start, end))
    
    # 处理每个片段 分析音高并保存
    total = len(cut_points)
    for i, (start, end) in enumerate(cut_points):
        print(f"Processing clip {i+1}/{total} ({start:.2f}s-{end:.2f}s)...")
        
        # 获取视频片段
        clip = video.subclip(start, end)
        
        # 分析这个片段的音高
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_clip_audio:
            temp_clip_audio_path = tmp_clip_audio.name
        
        clip.audio.write_audiofile(temp_clip_audio_path, fps=44100)
        clip_y, clip_sr = librosa.load(temp_clip_audio_path, sr=44100)
        
        # 音高分析
        f0, voiced_flag, _ = librosa.pyin(
            clip_y,
            fmin=librosa.note_to_hz('A0'),  # 钢琴最低音
            fmax=librosa.note_to_hz('C8'),  # 钢琴最高音
            sr=clip_sr,
            frame_length=2048
        )
        
        # 转换为音符并找出主音
        notes = []
        for freq in f0[voiced_flag]:
            if not np.isnan(freq):
                note = librosa.hz_to_note(freq, unicode=False)
                notes.append(note)
        
        main_note = max(set(notes), key=notes.count) if notes else "Unknown"
        
        # 清理片段的临时音频文件
        os.unlink(temp_clip_audio_path)
        
        # 生成新文件名
        new_name = f"{main_note}.mp4"
        new_path = os.path.join(output_dir, new_name)
        
        # 处理重名文件
        counter = 1
        while os.path.exists(new_path):
            new_name = f"{main_note}_{counter}.mp4"
            new_path = os.path.join(output_dir, new_name)
            counter += 1
        
        # 保存最终文件
        clip.write_videofile(new_path, codec="libx264", audio_codec="aac")
    
    # 清理主音频临时文件
    os.unlink(temp_audio_path)
    video.close()
    print(f"完成! 共生成 {len(cut_points)} 个片段")

if __name__ == "__main__":
    parse_piano_video(
        r"微信视频2025-08-08_183450_185.mp4",
        "output_clips_test",
        min_duration=0.3,  # 最小0.3秒
        volume_threshold=0.05  # 音量阈值
    )