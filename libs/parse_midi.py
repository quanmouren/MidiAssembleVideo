from mido import MidiFile, tick2second
import time

def parse_midi_notes(midi_path):
    """
    解析MIDI文件，提取每个音符的详细信息
    start_time : 音符开始时间
    duration : 音符持续时间
    note_name : 音符名称
    note_number : 音符编号
    channel : 通道
    velocity : 音量
    track : 轨道编号
    track_name : 轨道名称
    """
    def get_note_name(note_number):
        """将音符编号转换为音符名称"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note_number // 12) - 1  # 中央C
        note_index = note_number % 12
        return f"{note_names[note_index]}{octave}"
    
    try:
        mid = MidiFile(midi_path)
        print(f"成功加载MIDI文件: {midi_path}")
        print(f"格式: {mid.type}, 轨道数: {len(mid.tracks)}, 每拍ticks: {mid.ticks_per_beat}\n")
        # 存储所有音符信息
        notes = []
        # 用于跟踪未结束的音符
        active_notes = {}
        # 遍历每个轨道
        for track_idx, track in enumerate(mid.tracks):
            print(f"处理轨道 {track_idx}: {track.name if track.name else '未命名'}")
            current_time = 0.0  # 以秒为单位的当前时间
            tempo = 500000  # 默认速度
            # 遍历轨道中的每个事件
            for msg in track:
                # 转换ticks为秒
                current_time += tick2second(msg.time, mid.ticks_per_beat, tempo)             
                # 处理速度变化
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                
                # 处理音符开始事件
                elif msg.type == 'note_on' and msg.velocity > 0:
                    note_name = get_note_name(msg.note)
                    # 记录活跃音符
                    active_notes[(msg.note, msg.channel)] = {
                        'note_name': note_name,
                        'note_number': msg.note,
                        'channel': msg.channel,
                        'velocity': msg.velocity,
                        'start_time': current_time,
                        'track': track_idx,
                        'track_name': track.name if track.name else '未命名'
                    }
                
                # 处理音符结束事件
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    key = (msg.note, msg.channel)
                    if key in active_notes:
                        # 计算持续时间
                        start_time = active_notes[key]['start_time']
                        duration = current_time - start_time
                        # 完善音符信息
                        note_info = active_notes[key]
                        note_info['end_time'] = current_time
                        note_info['duration'] = duration
                        # 添加到音符列表
                        notes.append(note_info)
                        # 从活跃音符中移除
                        del active_notes[key]
        
        # 检查是否有未结束的音符
        for note in active_notes.values():
            note['end_time'] = note['start_time'] + 1.0  # 默认1秒
            note['duration'] = 1.0
            notes.append(note)
            print(f"警告: 音符 {note['note_name']} 没有结束事件，已添加默认持续时间")
        
        # 按开始时间排序
        notes.sort(key=lambda x: x['start_time'])
        
        return notes
    
    except FileNotFoundError:
        print(f"错误: 找不到文件 {midi_path}")
    except Exception as e:
        print(f"解析MIDI文件时出错: {str(e)}")
        return None

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    print("解析midi文件:")
    midi_file_path = filedialog.askopenfilename(filetypes=[("MIDI文件", "*.mid")])
    #midi_file_path = "test/input_test.mid"
    parse_midi_notes(midi_file_path)
