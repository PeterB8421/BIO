import os
import sys
from collections import defaultdict

# This function will scan the directory and group file names by their IDs
def scan_files(directory):
    file_dict = defaultdict(list)
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            file_id, _ = filename.split('_')[0], filename.split('_')[1].split('.')[0]
            file_dict[file_id].append(filename)
    return file_dict

# This function will delete files that have only one file per ID
def delete_single_files(directory, file_dict):
    for file_id, files in file_dict.items():
        if len(files) == 1:
            os.remove(os.path.join(directory, files[0]))
            print(f"Deleted {files[0]}")

if __name__ == '__main__':
    # The first command line argument is the script name, the second one is the directory path
    if len(sys.argv) != 2:
        print("Usage: python remover.py [path to folder containing files]")
        sys.exit(1)

    directory_path = sys.argv[1]

    # Check if the provided directory path exists
    if not os.path.isdir(directory_path):
        print(f"The directory {directory_path} does not exist.")
        sys.exit(1)

    # Scanning the files in the directory
    file_dict = scan_files(directory_path)

    # Deleting the files that only have a single file for their ID
    delete_single_files(directory_path, file_dict)
