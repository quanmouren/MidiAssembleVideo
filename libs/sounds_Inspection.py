import mido
from mido import MidiFile
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import webbrowser
from threading import Timer, Event, Thread
import time
import sys
from collections import defaultdict

def get_note_name(note_number):
    """将音符编号转换为音符名称（如60 -> C4）"""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note_number // 12) - 1  # MIDI中60是中央C（C4）
    note_index = note_number % 12
    return f"{note_names[note_index]}{octave}"

def analyze_midi_file(midi_path):
    """
    分析MIDI文件并返回详细统计信息
    返回:
        dict: 包含文件信息、轨道统计、音符统计等
    """
    try:
        mid = MidiFile(midi_path)
        file_info = {
            'filename': os.path.basename(midi_path),
            'filepath': os.path.abspath(midi_path),
            'duration': mid.length,
            'tracks': len(mid.tracks),
            'ticks_per_beat': mid.ticks_per_beat,
            'type': mid.type
        }

        # 轨道统计
        track_stats = []
        note_counts = defaultdict(int)
        note_details = defaultdict(list)
        
        for i, track in enumerate(mid.tracks):
            track_name = track.name if track.name else f"轨道_{i+1}"
            track_note_count = 0
            track_notes = set()
            
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    note = msg.note
                    note_name = get_note_name(note)
                    note_counts[note_name] += 1
                    track_note_count += 1
                    track_notes.add(note_name)
                    
                    # 记录音符详情
                    note_details[note_name].append({
                        'time': msg.time,
                        'velocity': msg.velocity,
                        'track': track_name
                    })

            track_stats.append({
                'name': track_name,
                'note_count': track_note_count,
                'unique_notes': len(track_notes),
                'notes': sorted(track_notes)
            })

        # 按出现频率排序音符
        sorted_notes = sorted(note_counts.items(), key=lambda x: x[1], reverse=True)
        note_list = [note for note, count in sorted(note_counts.items())]

        return {
            'status': 'success',
            'file_info': file_info,
            'track_stats': track_stats,
            'total_notes': sum(note_counts.values()),
            'unique_notes': len(note_counts),
            'note_counts': dict(sorted_notes),
            'note_list': note_list,
            'most_frequent_note': sorted_notes[0][0] if sorted_notes else None
        }
    
    except FileNotFoundError:
        return {'status': 'error', 'message': f'找不到文件: {midi_path}'}
    except Exception as e:
        return {'status': 'error', 'message': f'处理MIDI文件时出错: {str(e)}'}

def check_missing_note_videos(note_names, video_folder="sounds"):
    """
    检查视频文件夹中缺少的音符视频文件
    
    返回:
        dict: 包含检查结果和缺失音符列表
    """
    if not os.path.exists(video_folder):
        return {
            'status': 'error',
            'message': f"文件夹 '{video_folder}' 不存在",
            'missing_notes': note_names
        }
    
    if not os.path.isdir(video_folder):
        return {
            'status': 'error',
            'message': f"'{video_folder}' 不是一个文件夹",
            'missing_notes': note_names
        }
    
    # 获取现有文件
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'}
    existing_files = set()
    
    for filename in os.listdir(video_folder):
        name, ext = os.path.splitext(filename)
        if ext.lower() in video_extensions:
            existing_files.add(name.lower())
    
    # 检查缺失的音符
    missing_notes = [note for note in note_names if note.lower() not in existing_files]
    
    return {
        'status': 'success',
        'video_folder': os.path.abspath(video_folder),
        'total_checked': len(note_names),
        'existing': len(note_names) - len(missing_notes),
        'missing': len(missing_notes),
        'missing_notes': missing_notes,
        'existing_notes': [note for note in note_names if note.lower() in existing_files]
    }

class WebServer:
    def __init__(self, midi_path, video_folder="sounds"):
        self.app = Flask(__name__)
        self.midi_path = midi_path
        self.video_folder = video_folder
        self.last_heartbeat = time.time()
        self.shutdown_event = Event()
        self.setup_routes()
        CORS(self.app)
        
        # 初始分析结果
        self.analysis_result = analyze_midi_file(midi_path)
        self.missing_notes_result = None
        
        if self.analysis_result['status'] == 'success':
            self.missing_notes_result = check_missing_note_videos(
                self.analysis_result['note_list'], 
                video_folder
            )

    def setup_routes(self):
        """设置所有路由"""
        @self.app.route('/api/analysis', methods=['GET'])
        def get_analysis():
            """返回MIDI文件分析结果"""
            return jsonify(self.analysis_result)

        @self.app.route('/api/missing_notes', methods=['GET'])
        def get_missing_notes():
            """返回缺失的音符列表"""
            if self.missing_notes_result:
                return jsonify(self.missing_notes_result)
            return jsonify({'status': 'error', 'message': '尚未完成分析'})

        @self.app.route('/api/notes', methods=['GET'])
        def get_notes():
            """兼容旧API，只返回需要高亮显示的音符列表"""
            if self.missing_notes_result and self.missing_notes_result['status'] == 'success':
                return jsonify({
                    'status': 'success',
                    'notes': self.missing_notes_result['missing_notes']
                })
            return jsonify({'status': 'error', 'message': '无法获取音符列表'})

        @self.app.route('/api/heartbeat', methods=['GET'])
        def heartbeat():
            """接收前端心跳信号"""
            self.last_heartbeat = time.time()
            return jsonify({'status': 'alive', 'time': time.ctime()})

        @self.app.route('/api/file_info', methods=['GET'])
        def file_info():
            """返回文件基本信息"""
            info = {
                'midi_file': os.path.abspath(self.midi_path),
                'video_folder': os.path.abspath(self.video_folder),
                'analysis_time': time.ctime(),
                'status': 'running'
            }
            if self.analysis_result['status'] == 'success':
                info.update(self.analysis_result['file_info'])
            return jsonify(info)

        @self.app.route('/')
        def serve_frontend():
            """提供前端页面访问"""
            return send_from_directory(os.getcwd(), 'HTML/piano.html')

    def check_heartbeat(self):
        """检查心跳信号，超时则关闭程序"""
        while not self.shutdown_event.is_set():
            if time.time() - self.last_heartbeat > 5:
                print("检测到网页已关闭，自动终止程序...")
                self.shutdown_event.set()
                os._exit(0)
            time.sleep(1)

    @staticmethod
    def open_browser():
        """自动打开浏览器"""
        webbrowser.open_new('http://127.0.0.1:5000/')

    def run(self):
        """启动服务器和相关线程"""
        heartbeat_thread = Thread(target=self.check_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        
        Timer(1, self.open_browser).start()
        
        print("\n===== MIDI 文件分析结果 =====")
        print(f"文件: {self.midi_path}")
        if self.analysis_result['status'] == 'success':
            print(f"总音符数: {self.analysis_result['total_notes']}")
            print(f"唯一音符数: {self.analysis_result['unique_notes']}")
            print(f"最频繁的音符: {self.analysis_result['most_frequent_note']}")
        
        if self.missing_notes_result and self.missing_notes_result['status'] == 'success':
            print("\n===== 缺失视频检查结果 =====")
            print(f"视频文件夹: {self.video_folder}")
            print(f"缺失音符数: {self.missing_notes_result['missing']}")
            print(f"缺失的音符: {', '.join(self.missing_notes_result['missing_notes'])}")
        
        print("\n服务器运行中，访问 http://localhost:5000")
        try:
            self.app.run(debug=True, use_reloader=False)
        except KeyboardInterrupt:
            print("用户中断程序")
            self.shutdown_event.set()
def runwebserver(midi_file_path, video_folder):
    server = WebServer(midi_file_path, video_folder)
    server.run()
    
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    print("解析midi文件:")
    midi_file_path = filedialog.askopenfilename(filetypes=[("MIDI文件", "*.mid")]) # 获得选择好的MIDI文件
    video_folder = "sounds"           # 视频文件夹
    
    # 启动服务器
    server = WebServer(midi_file_path, video_folder)
    server.run()