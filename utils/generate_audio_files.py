import os
import glob
import subprocess

def load_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    data = [line.strip().rsplit(' ', 1) for line in lines]
    paths, labels = zip(*data)
    return paths, labels

def convert(v, output_path):
    subprocess.check_call([
    'ffmpeg',
    '-n',
    '-i', v,
    '-acodec', 'pcm_s16le',
    '-ac','1',
    '-ar','16000',
    output_path + '%s.wav' % v[:-4]])

    
valid_paths, _ = load_txt_file('/kaggle/working/AEO/HAC-rgb-flow-audio/splits/Kinetics_test_100.txt')

folder_path = '/kaggle/working/EPIC-KITCHENS'
output_path = '/kaggle/working/EPIC-KITCHENS'
num = 0

# 添加调试代码
print("valid_paths 示例（前5条）:", valid_paths[:5])
print("当前目录文件示例（前5个）:")
for root, dirs, files in os.walk(folder_path):
    for file in files[:5]:
        file_path_1 = os.path.join(root[2:], file)
        print("生成的 file_path_1:", file_path_1)
    break  # 只检查第一层

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_path_1 = os.path.join(root[2:], file)
        if file_path_1 in valid_paths and file_path.endswith('.mp4'):
            # Delete the file
            try:
                convert(file_path_1, output_path)
                num = num + 1
            except:
                print("no audio: ")
                print(file_path_1)

print(f"Created {str(num)} files")