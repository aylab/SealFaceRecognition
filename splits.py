#! /usr/local/bin/python3

'''
 Gets a directory and outputs file names and individual names for use in splits
 Assumes each subdir contains only one individual, and the name of the subdir is the name of the individual
 Image extensions are expected, append to the tuple below to extend
 Usage: ./splits.py -d /path/to/gallery/with/individuals > output_file.txt
 Output: List of absolute paths to individual photos and the individual name
'''

import os 
from pathlib import Path

def create_splits(directory):
    individuals = get_individuals(directory)
    with open('./splits/fold_1/gal_1.txt','w') as f:
        for key, value in individuals.items():
            for item in value:
                f.write(item + ' ' + key + '\n')


def get_individuals(directory):
    prefix = Path(directory).resolve()
    extensions = ('png', 'jpg', 'jpeg')
    individuals = {}
    for item in os.listdir(directory):
        
        path = os.path.join(prefix, item)
        if not os.path.isdir(path):
            continue
        name = str(int(item))
        individuals[name] = []
        for file_name in os.listdir(path):
            if not file_name.lower().endswith(extensions):
                continue
            file_path = os.path.join(path, file_name)
            individuals[name].append(str(file_path))
    
    return individuals