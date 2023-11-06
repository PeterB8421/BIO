import os
import shutil
import re
import sys

# Regular expression to match files of the format '[id]_[number].jpg'
file_pattern = re.compile(r'(\d+)_(\d+)\.jpg')

def organize_files(directory):
    files_by_id = {}

    # Scan the directory for matching files
    for filename in os.listdir(directory):
        match = file_pattern.match(filename)
        if match:
            file_id = match.group(1)
            if file_id not in files_by_id:
                files_by_id[file_id] = []
            files_by_id[file_id].append(filename)

    # Move the files to their respective folders
    for file_id, filenames in files_by_id.items():
        target_directory = os.path.join(directory, file_id)
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        for filename in filenames:
            shutil.move(os.path.join(directory, filename), target_directory)

    print("Files have been organized.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python batcher.py [path to the folder containing files]")
        sys.exit(1)

    path_to_folder = sys.argv[1]

    if not os.path.isdir(path_to_folder):
        print("The provided path does not exist or is not a directory.")
        sys.exit(1)

    organize_files(path_to_folder)
