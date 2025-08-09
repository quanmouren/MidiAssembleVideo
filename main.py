from libs.parse_midi import parse_midi_notes
from libs.VideoRendering import VideoRendering
from libs.sounds_Inspection import runwebserver
if __name__ == "__main__":
    midi_file_path = "test/input_test.mid"
    notes = parse_midi_notes(midi_file_path)
    try:
        VideoRendering(notes, video_dir="sounds", sustained=0.4, output_video_path="output_video.mp4",chord_size_ratio=0.44, start_render_time=0, end_render_time=10)
    except Exception as e:
        print("运行错误:", e)
        runwebserver(midi_file_path, "sounds")