#! /usr/local/bin/python3

'''
 Gets a directory and outputs file names and individual names for use in splits
 Assumes each subdir contains only one individual, and the name of the subdir is the name of the individual
 Image extensions are expected, append to the tuple below to extend
 Usage: ./splits.py -d /path/to/gallery/with/individuals > output_file.txt
 Output: List of absolute paths to individual photos and the individual name
'''

from argparse import ArgumentParser
import os 
from pathlib import Path

def main():
    arg_parser = ArgumentParser(description='Create Splits', add_help=False)
    arg_parser.add_argument('-d', '--directory', dest='directory', action='store',
            type=str, required=True, help='''Directory containing subdirectories that contain photos''')

    settings = arg_parser.parse_args()
    prefix = Path(settings.directory).resolve()
    extensions = ('png', 'jpg', 'jpeg')

    for individual in os.listdir(settings.directory):
        name = str(int(individual))
        path = os.path.join(prefix, individual)
        if not os.path.isdir(path):
            continue
        for file_name in os.listdir(path):
            if not file_name.lower().endswith(extensions):
                continue
            file_path = os.path.join(path, file_name)
            print(str(file_path) + ' ' + name)


if __name__=='__main__':
    main()