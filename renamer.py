import os
import sys
import pandas as pd
from collections import defaultdict

def load_mapping(csv_path):
    df = pd.read_csv(csv_path)
    mapping = {int(os.path.splitext(row['idx'])[0]): row['value'] for _, row in df.iterrows()}
    return mapping

def rename_files(folder_path, mapping):
    files = os.listdir(folder_path)
    renamed_files = defaultdict(int)
    for old_name in files:
        if old_name.endswith('.jpg'):
            file_number = int(os.path.splitext(old_name)[0])
            if file_number in mapping:
                new_base_name = str(mapping[file_number])
                renamed_files[new_base_name] += 1
                sequence_number = renamed_files[new_base_name]
                new_name = f"{new_base_name}_{sequence_number:02d}.jpg"
                os.rename(os.path.join(folder_path, old_name), os.path.join(folder_path, new_name))
                print(f"Renamed {old_name} to {new_name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python renamer.py [mapping.csv] [path to folder containing files to rename]")
        sys.exit(1)

    mapping_csv_path = sys.argv[1]
    target_folder_path = sys.argv[2]

    if not os.path.exists(mapping_csv_path):
        print(f"The file {mapping_csv_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(target_folder_path):
        print(f"The folder {target_folder_path} does not exist.")
        sys.exit(1)

    file_mapping = load_mapping(mapping_csv_path)
    rename_files(target_folder_path, file_mapping)
