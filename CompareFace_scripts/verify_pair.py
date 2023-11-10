import json
import sys
import pprint

from compreface import CompreFace
from compreface.service import VerificationService

DOMAIN: str = 'http://localhost'
PORT: str = '8000'
API_KEY: str = '814d9acc-aa5a-493d-9134-c33390e8e58b'

compre_face: CompreFace = CompreFace(DOMAIN, PORT)
# VERIFICATION_API_KEY: str = 'your_face_verification_key'

verify: VerificationService = compre_face.init_face_verification(API_KEY)


def main():
    if len(sys.argv) != 3:
        print('Usage:\n'
              'python verify_pair.py <source_file> <target_file>\n'
              '<source_file> = Original face\n'
              '<target_file> = Face to compare to the original face', file=sys.stderr)
        exit(1)
    src_file = sys.argv[1]
    target_file = sys.argv[2]
    response = verify.verify(src_file, target_file, options={
        "face_plugins": "landmarks",
    })
    print(response)


if __name__ == '__main__':
    main()
