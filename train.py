#! /usr/local/bin/python3
"""Main training file for face recognition
"""
# MIT License
# 
# Copyright (c) 2018 Debayan Deb
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import time
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from argparse import ArgumentParser
import utils
import tflib
from network import Network
# from tensorflow.contrib.tensorboard.plugins import projector
import evaluate
import splits
import shutil


def train(config_file, counter):
    # I/O
    config = utils.import_file(config_file, 'config')
    splits_path = config.splits_path + '/split{}'.format(counter)

    trainset = utils.Dataset(splits_path + '/train_' + str(config.fold_number) + '.txt')
    trainset.images = utils.preprocess(trainset.images, config, True)

    network = Network()
    network.initialize(config, trainset.num_classes)

    # Initalization for running
    log_dir = utils.create_log_dir(config, config_file)
    summary_writer = tf.compat.v1.summary.FileWriter(log_dir, network.graph)
    if config.restore_model:
        network.restore_model(config.restore_model, config.restore_scopes)

    # Load gallery and probe file_list
    print('Loading images...')
    probes = []
    gal = []
    with open(splits_path + '/fold_' + str(config.fold_number) + '/probe_1.txt' ,'r') as f:
        for line in f:
            probes.append(line.strip())

    probe_set = evaluate.ImageSet(probes, config)
    #probe_set.extract_features(network, len(probes))
    #
    with open(splits_path + '/fold_'+ str(config.fold_number) + '/gal_1.txt', 'r') as f:
        for line in f:
            gal.append(line.strip())
    gal_set = evaluate.ImageSet(gal, config)
    #gal_set.extract_features(network, len(gal))

    trainset.start_batch_queue(config, True)

    #
    # Main Loop
    #
    print('\nStart Training\n# epochs: {}\nepoch_size: {}\nbatch_size: {}\n'.\
        format(config.num_epochs, config.epoch_size, config.batch_size))

    global_step = 0
    start_time = time.time()
    for epoch in range(config.num_epochs):
        # Training
        for step in range(config.epoch_size):
            # Prepare input
            learning_rate = utils.get_updated_learning_rate(global_step, config)
            image_batch, label_batch = trainset.pop_batch_queue()

            wl, sm, global_step = network.train(image_batch, label_batch, learning_rate, config.keep_prob)

            # Display
            if step % config.summary_interval == 0:
                # visualize.scatter2D(_prelogits[:,:2], _label_batch, _pgrads[0][:,:2])
                duration = time.time() - start_time
                start_time = time.time()
                utils.display_info(epoch, step, duration, wl)
                summary_writer.add_summary(sm, global_step=global_step)

        # Testing
        print('Testing...')
        probe_set.extract_features(network, len(probes))
        gal_set.extract_features(network, len(gal))

        rank1, rank5 = evaluate.identify(log_dir, probe_set, gal_set)
        print('rank-1: {:.3f}, rank-5: {:.3f}'.format(rank1[0], rank5[0]))
        
        # Output test result
        summary = tf.Summary()
        summary.value.add(tag='identification/rank1', simple_value=rank1[0])
        summary.value.add(tag='identification/rank5', simple_value=rank5[0])
        summary_writer.add_summary(summary, global_step)

        # Save the model
        network.save_model(log_dir, global_step)
    results_copy = os.path.join('log/result_{}_{}.txt'.format(config.model_version, counter))
    shutil.copyfile(os.path.join(log_dir,'result.txt'), results_copy)

def main():
    parser = ArgumentParser(description='Train SealNet', add_help=False)
    parser.add_argument('-c','--config_file', dest='config_file', action='store', 
        type=str, required=True, help='Path to training configuration file', )
    parser.add_argument('-d', '--directory', dest='directory', action='store',
        type=str, required=True, help='Directory containing subdirectories that contain photos')
    parser.add_argument('-s', '--splits', dest='splits', action='store', type=bool,
        required=False, help='Flag to use existing splits for training and testing data')
    parser.add_argument('-n', '--number', dest='number', action='store', type=int,
        required=False, help='Number of times to run the training(default is 3)')

    settings = parser.parse_args()
    num_trainings = 3 if not settings.number else settings.number
    print('Running training {} times'.format(num_trainings))
    if not settings.splits:
        print('Making new splits')
        # clean splits directory
        if os.path.exists(os.path.expanduser('./splits')):
            shutil.rmtree(os.path.expanduser('./splits')) 
        splits.create_splits(settings.directory, num_trainings)
    else:
        print('Using existing splits in the splits folder')

    for i in range(num_trainings):
        print('Starting training #{}'.format(i+1))
        train(settings.config_file, i+1)

if __name__ == '__main__':
    main()
