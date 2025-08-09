import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, CompositeVideoClip, ColorClip, ImageClip

def create_text_image(text, size, bg_color, fontsize=30, text_color=(255, 255, 255)):
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", fontsize)
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", fontsize)
        except:
            font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    draw.text((x, y), text, font=font, fill=text_color)

    return np.array(img)

def create_note_video(audio_path, output_path, size=(320, 240)):
    note_name = os.path.splitext(os.path.basename(audio_path))[0]
    bg_color = (
        random.randint(50, 200),
        random.randint(50, 200),
        random.randint(50, 200)
    )
    
    with AudioFileClip(audio_path) as audio:
        duration = audio.duration
        background = ColorClip(size=size, color=bg_color, duration=duration)
        fontsize = min(size[0], size[1]) // 4
        text_image = create_text_image(
            text=note_name,
            size=size,
            bg_color=bg_color,
            fontsize=fontsize
        )
        text_clip = ImageClip(text_image).set_duration(duration).set_position('center')
        
        final_clip = CompositeVideoClip([background, text_clip])
        final_clip = final_clip.set_audio(audio)
        
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=10, 
            preset='fast'
        )
        
        final_clip.close()
        background.close()
        text_clip.close()
    
    print(f"已生成视频: {output_path} (背景色: {bg_color})")

def process_audio_folder(input_folder, output_folder, video_size=(320, 240)):
    os.makedirs(output_folder, exist_ok=True)
    audio_extensions = ('.mp3', '.wav', '.ogg', '.flac', '.m4a')
    audio_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(audio_extensions)
    ]
    
    if not audio_files:
        print(f"在 {input_folder} 中未找到音频文件")
        return
    print(f"找到 {len(audio_files)} 个音频文件，开始生成视频...")
    for audio_file in audio_files:
        audio_path = os.path.join(input_folder, audio_file)
        # 保持文件名，将扩展名改为.mp4
        video_filename = os.path.splitext(audio_file)[0] + '.mp4'
        video_path = os.path.join(output_folder, video_filename)
        
        try:
            create_note_video(audio_path, video_path, video_size)
        except Exception as e:
            print(f"处理 {audio_file} 时出错: {str(e)}")
    
    print("所有视频生成完成！")

if __name__ == "__main__":
    input_folder = "test\\soundsForMP3"
    output_folder = "test\\sounds"
    
    # 视频尺寸
    video_size = (540, 960) 
    process_audio_folder(input_folder, output_folder, video_size)