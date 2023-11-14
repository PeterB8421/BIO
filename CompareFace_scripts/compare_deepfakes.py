import json
import os.path
import sys
import glob
import re

from compreface import CompreFace
from compreface.service import VerificationService

DOMAIN: str = 'http://localhost'
PORT: str = '8000'
API_KEY: str = 'dabc631b-38a9-435a-b75a-e3b7340ebfb4'

compre_face: CompreFace = CompreFace(DOMAIN, PORT)

verify: VerificationService = compre_face.init_face_verification(API_KEY)


def create_json_directories(directory):
    for root, dirs, files in os.walk(directory):
        json_dir = os.path.join(root, 'json')
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)


def main():
    if len(sys.argv) != 2:
        print('Usage: python compare_results.py <dir>\n'
              '<dir> = Directory containing subdirectories with files ending as "_deepfake.jpg"', file=sys.stderr)
        exit(1)
    path = sys.argv[1]
    json_dirs = glob.glob(os.path.join(path, '*/json'))
    if not json_dirs:
        create_json_directories(path)
    pattern_obscure = os.path.join(path, '*/*_obscure_result.jpg')
    pattern_glasses = os.path.join(path, '*/*_glasses_result.jpg')
    pattern_hair = os.path.join(path, '*/*_hair_result.jpg')
    pattern_ref = os.path.join(path, '*/*_ref_result.jpg')

    matching_files_obscure = glob.glob(pattern_obscure)
    matching_files_glasses = glob.glob(pattern_glasses)
    matching_files_hair = glob.glob(pattern_hair)
    matching_files_ref = glob.glob(pattern_ref)

    files = matching_files_obscure + matching_files_glasses + matching_files_hair + matching_files_ref

    refs = glob.glob(os.path.join(path, '*/*_ref.jpg'))
    results = []
    for src in refs:
        prefix = re.search(r'\\(\d+)\\', src)
        prefix = prefix.group(1)
        for target in files:
            if target == src:
                continue
            target_prefix = re.search(r'\\(\d+)\\', target)
            target_prefix = target_prefix.group(1)
            if prefix != target_prefix:
                continue
            current = verify.verify(src, target)
            current['src'] = src
            current['target'] = target
            results.append(current)
        filename = os.path.basename(src)
        json_path = os.path.join(path, prefix, 'json', f'{filename.replace(".jpg", ".json")}')
        with open(json_path, 'w') as json_file:
            json.dump(results, json_file, indent=2)
        results = []


if __name__ == '__main__':
    main()
