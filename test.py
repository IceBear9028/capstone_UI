import os

dir_path = os.getcwd()


video_path = []
dir_path = os.getcwd()
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.mp4' in file:
            file_path = os.path.join(root, file)
            file_path = file_path.replace(dir_path, '')
            video_path.append(file_path)

print(video_path)