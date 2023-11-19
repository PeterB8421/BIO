"""
Script to compare all photos from dataset.
This compares all references with each other to see,
what value represents if there are two different people in the photos.
"""
from recognition_lib.FaceRecognition import FaceRecognition
import sys
import glob
import os
import json
import re
import platform


def create_json_directories(directory):
    for root, dirs, files in os.walk(directory):
        json_dir = os.path.join(root, 'json')
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

def main():
    if len(sys.argv) != 2:
        print('Usage: python compare_dataset.py <dir>\n'
              '<dir> = Directory containing subdirectories with files to compare.\n',
              file=sys.stderr)
        exit(1)
    path = sys.argv[1]
    json_dirs = glob.glob(os.path.join(path, '*/json'))
    if not json_dirs:
        create_json_directories(path)
    fce = FaceRecognition('magface', detection_device='gpu', recognition_device='gpu')

    # Comparing references
    print('Comparing references between themselves')

    files = glob.glob(os.path.join(path, '*/*_ref.jpg'))

    refs = glob.glob(os.path.join(path, '*/*_ref.jpg'))
    results = []
    for src in refs:
        if platform.system() == 'Windows':
            prefix = re.search(r'\\(\d+)\\', src)
        else:
            prefix = re.search(r'\/(\d+)\/', src)
        prefix = prefix.group(1)
        for target in files:
            if target == src:
                continue
            if platform.system() == 'Windows':
                target_prefix = re.search(r'\\(\d+)\\', target)
            else:
                target_prefix = re.search(r'\/(\d+)\/', target)
            target_prefix = target_prefix.group(1)
            if prefix == target_prefix:
                continue
            current = {}
            current['distance'] = str(fce.verify(src, target)) # Named similarity because of compatibility with plotting script, this is actually distance
            current['src'] = src
            current['target'] = target
            results.append(current)
        filename = os.path.basename(src)
        json_path = os.path.join(path, prefix, 'json', f'cross_{filename.replace(".jpg", ".json")}')
        with open(json_path, 'w') as json_file:
            json.dump(results, json_file, indent=2)
        results = []

if __name__ == '__main__':
    main()
