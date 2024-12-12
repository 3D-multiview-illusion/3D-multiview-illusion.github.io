import os
import subprocess
import argparse

def compress_videos(input_folder, crf):
    output_folder = os.path.join(input_folder, 'compressed')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.mp4'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            compress_video(input_path, output_path, crf)

def compress_video(input_path, output_path, crf):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vcodec', 'libx264',  # Using H.264 codec for better compatibility
        '-crf', str(crf),      # Constant Rate Factor (lower value means better quality)
        '-preset', 'slow',     # Preset for better compression
        '-profile:v', 'high',  # Profile for better compatibility
        '-level', '4.0',       # Level for better compatibility
        output_path
    ]
    subprocess.run(command, check=True)
# python compress.py /Users/fengyue/Desktop/mirror  --crf 24
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compress MP4 videos in a folder using ffmpeg.')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing MP4 files.')
    parser.add_argument('--crf', type=int, default=28, help='Constant Rate Factor (lower value means better quality). Default is 28.')

    args = parser.parse_args()
    compress_videos(args.input_folder, args.crf)