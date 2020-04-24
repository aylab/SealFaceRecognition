#! /usr/local/bin/python3

'''
 Gets a directory and outputs file names and individual names for use in splits
 Assumes each subdir contains only one individual, and the name of the subdir is the name of the individual
 Image extensions are expected, append to the tuple below to extend
'''

import os 
from pathlib import Path

def create_splits(directory):
    prefix = Path(directory).resolve()
    splits_dir = os.path.join(os.path.expanduser('./splits'))

    if not os.path.isdir(splits_dir):  
        os.makedirs(splits_dir)
    
    for item in os.listdir(directory):
        if item.endswith('training'):
            training = get_individuals(os.path.join(prefix, item))
        if item.endswith('testing'):
            testing = get_individuals(os.path.join(prefix, item))

    create_testing_set(testing)
    create_training_set(training)

def create_training_set(individuals):
    with open('./splits/train_1.txt', 'w') as f:
        for key, value in individuals.items():
            for v in value:
                f.write(v + ' ' + key + '\n')
    
def create_testing_set(individuals):
    splits_dir = os.path.join(os.path.expanduser('./splits/fold_1/'))
    if not os.path.isdir(splits_dir):  
        os.makedirs(splits_dir)
    splits = min([len(value) for key, value in individuals.items()])

    for i in range(splits):
        gallery = open('./splits/fold_1/gal_{}.txt'.format(i+1),'w')
        probe = open('./splits/fold_1/probe_{}.txt'.format(i+1),'w')
        # verification = open('./splits/fold_1/verification.txt'.format(i+1),'w')
        for key, value in individuals.items():
            if i >= len(value):
                continue
            probe.write(value[i]+ ' ' + key + '\n')
            for j in range(len(value)):
                # verification.write(value[j] + ' ' + key + '\n')
                if j != i:
                    gallery.write(value[j] + ' ' + key + '\n')
            
        gallery.close()
        probe.close()
        # verification.close()


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
            if file_name.lower().endswith(extensions):
                file_path = os.path.join(path, file_name)
                individuals[name].append(str(file_path))
    
    return individuals