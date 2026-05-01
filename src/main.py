from MIDITool.parse_midi import parse_midi_notes
from renderer.corner_layout import VideoRendering
from sounds_Inspection import runwebserver
if __name__ == "__main__":
    midi_file_path = "test/input_test.mid"  
    sounds_file_path = "sounds"
    notes = parse_midi_notes(midi_file_path)
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