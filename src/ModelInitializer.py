# Initialize single word model
# By using Viterbi estimate formulae
import sys
from ModelIO import ReadPreModel, WriteModel
import math
import numpy as np
from Utility import ParseConfig, GetDictionary
from pdb import set_trace
from x64.Release.TrainCore import VTrain
from os import getcwd
from MFCC import load
from glob import glob


MAIN_DIR = getcwd() + '/'
MFCC_FOLDER = MAIN_DIR + 'mfcc/single/'
MODEL_FOLDER = MAIN_DIR + 'model/'
PREMODEL_FOLDER = MAIN_DIR + 'premodel/'
DICT_DIR = MAIN_DIR + 'dict/'
CONFIG_DIR = MAIN_DIR + 'config/'

#########################################################################
#                          MAIN ENTRY #
#########################################################################
if len(sys.argv) < 3:
    sys.exit("Usage: ModelIitializer.py <dict> <config>")


# Get dictionary
# dict_file = open(sys.argv[1])
# words = []
# model_id = []
# for line in dict_file:
# 	tokens = line.strip().split()
#         model_id.append(tokens[0])
# 	words.append(tokens[1])
# dict_file.close()
words, model_id = GetDictionary(DICT_DIR + sys.argv[1] + '.txt')

num_components_key = 'NUMCOMPONENTS'
num_repeat_key = 'NUMREPEAT'
# Get configuration
conf_filename = CONFIG_DIR + sys.argv[2] + '.conf'
num_components = ParseConfig(conf_filename, num_components_key)
num_repeat = ParseConfig(conf_filename, num_repeat_key)
if num_components != '':
    num_components = int(num_components)
else:
    # Use only 1 component in GMM by default
    num_components = 1
if num_repeat != '':
    num_repeat = int(num_repeat)
else:
    num_repeat = 1

# For each model
for k in range(len(model_id)):
    # Load MFCC data
    # To compute the global mean and log_var
    MFCC_filename_list = glob(MFCC_FOLDER + '*' + model_id[k] + '*.txt')
    # MFCC_filename_list = [MFCC_FOLDER+model_id[k]+'-'+str(num)+'.xml' for num
    # in range(num_repeat)]
    # feat_list,dim_observation_list,num_frames_list =
    # MFCCIO.ReadMFCCs(MFCC_filename_list)
    feat_list = []
    for filename in MFCC_filename_list:
        feat_list.append(load(filename))

    # dim_observation = dim_observation_list[0] # All dim_observation are the
    # same
    dim_observation = len(feat_list[0][0])

    # Load pre model
    pre_model_file = PREMODEL_FOLDER + model_id[k] + '.xml'
    name, states, num_states, nnz, network = ReadPreModel(pre_model_file)
    print('Viterbi Training: ' + str(k + 1) + '/' + str(len(model_id)))

    log_trans, log_coef, mean, log_var = VTrain(num_states, num_components, network, feat_list)
    
    
    # Write in model file
    WriteModel(name, states, num_states, num_components, dim_observation,
               log_trans, log_coef, mean, log_var, MODEL_FOLDER + model_id[k] + '.xml')