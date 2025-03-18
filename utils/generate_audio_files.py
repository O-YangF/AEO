import os
import subprocess

def load_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    data = [line.strip().rsplit(' ', 1) for line in lines]
    paths, labels = zip(*data)
    return paths, labels

def convert(v, output_path):
    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)
    
    # 生成输出文件名（保留类别目录结构）
    output_file = os.path.join(output_path, os.path.relpath(v, '/kaggle/working/EPIC-KITCHENS')).replace('.mp4', '.wav')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    subprocess.check_call([
        'ffmpeg',
        '-n',
        '-i', os.path.join('/kaggle/working/EPIC-KITCHENS', v),  # 完整输入路径
        '-acodec', 'pcm_s16le',
        '-ac','1',
        '-ar','16000',
        output_file
    ])

valid_paths, _ = load_txt_file('/kaggle/working/AEO/HAC-rgb-flow-audio/splits/Kinetics_test_100.txt')
folder_path = '/kaggle/working/EPIC-KITCHENS'
output_path = '../epic-kitchens'
num = 0

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.mp4'):
            # 生成相对于 folder_path 的路径（如 'building sandcastle/file.mp4'）
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            
            if relative_path in valid_paths:
                try:
                    convert(relative_path, output_path)
                    num += 1
                except Exception as e:
                    print(f"转换失败: {relative_path}, 错误: {str(e)}")

print(f"Created {num} files")