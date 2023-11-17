import os
import subprocess
import sys

def find_target_image(target_folder):
    # Find the target image with '_border.jpg' suffix
    for file in os.listdir(target_folder):
        if file.endswith('_border.jpg'):
            return os.path.join(target_folder, file)
    return None

def process_images_in_folder(folder):
    # Path to the target image in the current folder
    target_image_path = find_target_image(os.path.join(folder, 'target'))
    if not target_image_path:
        print(f"No target image found in {folder}/target")
        return

    # Iterating through each subdirectory in the current folder
    for subdir in os.listdir(folder):
        subdir_path = os.path.join(folder, subdir)
        if os.path.isdir(subdir_path) and subdir != 'target':
            # Processing each file in the subdirectory
            for file in os.listdir(subdir_path):
                if file.endswith('_border.jpg'):
                    source_image_path = os.path.join(subdir_path, file)
                    result_image_path = os.path.join(subdir_path, file.replace('_border.jpg', '_result.jpg'))

                    # Constructing command and running FaceFusion
                    command = [
                        'python', 'run.py', 
                        '-s', source_image_path, 
                        '-t', target_image_path, 
                        '-o', result_image_path, 
                        '--face-swapper-model', 'inswapper_128', 
                        '--face-enhancer-model', 'gfpgan_1.4', 
                        '--execution-providers', 'cpu', 
                        '--headless', 
                        '--frame-processors', 'face_swapper', 'face_enhancer'
                    ]
                    subprocess.run(command)

def main():
    if len(sys.argv) != 2:
        print("Usage: python processor.py [path/to/root/folder]")
        sys.exit(1)

    root_folder = sys.argv[1]
    process_images_in_folder(os.path.join(root_folder, 'men'))
    process_images_in_folder(os.path.join(root_folder, 'women'))

if __name__ == "__main__":
    main()
