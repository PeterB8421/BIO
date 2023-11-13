import json
import os.path
import sys
import glob

from compreface import CompreFace
from compreface.service import VerificationService

DOMAIN: str = 'http://localhost'
PORT: str = '8000'
API_KEY: str = 'dabc631b-38a9-435a-b75a-e3b7340ebfb4'

compre_face: CompreFace = CompreFace(DOMAIN, PORT)

verify: VerificationService = compre_face.init_face_verification(API_KEY)


def main():
    if len(sys.argv) != 2:
        print('Usage: python compare_results.py <dir>\n'
              '<dir> = Directory containing subdirectories with files ending as "_result.jpg"', file=sys.stderr)
        exit(1)
    path = sys.argv[1]
    files = glob.glob(os.path.join(path, '*/*result.jpg'))
    results = []
    for src in files:
        for target in files:
            if target == src:
                continue
            results.append(verify.verify(src, target, options={
                "face_plugins": "landmarks",
            }))
        with open(src.replace('.jpg', '.json'), 'w') as json_file:
            json.dump(results, json_file, indent=4)


if __name__ == '__main__':
    main()
