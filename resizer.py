import os
import sys
import subprocess

def resize_image(file_path, new_file_path):
    # resize the image using ImageMagick
    resize = f"convert {file_path} -gravity center -background white -extent 1500x1500 {new_file_path}"
    subprocess.run(resize, shell=True)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                original_path = os.path.join(root, file)
                # new image will have suffix _border.jpg
                new_file_name = os.path.splitext(file)[0] + "_border.jpg"
                new_file_path = os.path.join(root, new_file_name)
                resize_image(original_path, new_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resizer.py [path/to/folder]")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print(f"The provided folder path {folder_path} does not exist.")
        sys.exit(1)

    process_directory(folder_path)
    print("Resizing completed.")
