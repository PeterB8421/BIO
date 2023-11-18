# This Python script verifies two photos and prints the response from CompreFace
import sys

from compreface import CompreFace
from compreface.service import VerificationService

DOMAIN: str = 'http://localhost'
PORT: str = '8000'
API_KEY: str = 'dabc631b-38a9-435a-b75a-e3b7340ebfb4'

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
    response = verify.verify(src_file, target_file)
    print(response)


if __name__ == '__main__':
    main()
