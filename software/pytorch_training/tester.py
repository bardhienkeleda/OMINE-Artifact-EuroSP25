# *************************************************************************
#
# Copyright 2025 Enkeleda Bardhi (TU Delft),
#                Chenxing Ji (TU Delft),
#                Ali Imran (University of Michigan),
#                Muhammad Shahbaz (University of Michigan),
#                Riccardo Lazzeretti (Sapienza University of Rome),
#                Mauro Conti (University of Padua),
#                Fernando Kuipers (TU Delft)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# *************************************************************************

import os
import torch
import shutil
import argparse
import sklearn
import numpy as np
import pandas as pd
from trainer import get_device, TorchModel
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import recall_score


def define_settings():
    parser = argparse.ArgumentParser(description="Settings for testing the switches models.") 
    parser.add_argument("--test_batch", type=int, required=True)
    parser.add_argument("--nn_batch_size", type=int, default=32)
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--node_number", type=int, required=True) 
    parser.add_argument("--feature_type", type=str, required=True)
    parser.add_argument("--max_switches", type=int, default=5)
    parser.add_argument("--test_full", type=bool, default=False)
    parser.add_argument("--full_dataset", type=bool, default=False)
    parser.add_argument("--scarsity_level", type=float, default=0.8)
    
    args = parser.parse_args()
    return args
    
def load_and_return_full_and_batched(data, test_batch):

    print("Loading full test data...")
    data = pd.read_csv('datasets/' + data + '_test_data.csv', index_col=0)
    labels = pd.read_csv('datasets/' + data + '_test_labels.csv', index_col=0)
    labels.reset_index(inplace=True, drop=True)

    print("Loading test batched data with test size {}".format(2*(test_batch)))
    batched_full_data = pd.read_csv('datasets/batched_tests/' + data + '/batched_' + str(2*test_batch) + '_test.csv', sep="\t", index_col=0) 
   
    full_test_data = pd.concat([data, labels], axis=1) #, axis=1
    print(full_test_data.head(10))
    # Get only specific columns from full dataset
    if data == 'cicids':
        test_features_df = full_test_data.loc[:, ['Destination Port', 'Fwd Packet Length Max', 'Fwd Packet Length Mean',
                                                    'Bwd Packet Length Min', 'Packet Length Variance', 'URG Flag Count',
                                                    'Avg Fwd Segment Size', 'Label']]
    
    else:
        test_features_df= full_test_data.loc[:,['dttl', 'swin', 'dload', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_srv_dst', 'sttl', 'label']]

    print("Loading the test batch size test data...")

    if data == 'cicids':
        test_data_df = test_features_df.loc[:, test_features_df.columns != 'Label']
        test_labels_df = test_features_df.loc[:, test_features_df.columns == 'Label']
        batched_test_features_df = batched_full_data.loc[:, batched_full_data.columns != 'Label']
        batched_test_labels_binary_df = batched_full_data.loc[:, batched_full_data.columns == 'Label']
    else:
        test_data_df = test_features_df.loc[:, test_features_df.columns != 'label']
        test_labels_df = test_features_df.loc[:, test_features_df.columns == 'label']
        batched_test_features_df = batched_full_data.loc[:, batched_full_data.columns != 'label']
        batched_test_labels_binary_df = batched_full_data.loc[:, batched_full_data.columns == 'label']

    print('*** The full test data has the following shape: ***')
    print(test_data_df.shape)
    print('*** The batched test data has the following shape: ***')
    print(batched_test_features_df.shape)

    test_tensor_dataset_bin_pt = TensorDataset(torch.Tensor(test_data_df.values), torch.Tensor(test_labels_df.values))
    test_loader_bin_pt = DataLoader(dataset=test_tensor_dataset_bin_pt, batch_size=args.nn_batch_size, shuffle=True)

    batched_test_tensor_dataset_bin_pt = TensorDataset(torch.Tensor(batched_test_features_df.values), torch.Tensor(batched_test_labels_binary_df.values))
    batched_test_loader_bin_pt = DataLoader(dataset=batched_test_tensor_dataset_bin_pt, batch_size=args.nn_batch_size, shuffle=True)

    return test_loader_bin_pt, batched_test_loader_bin_pt


def load_models_and_test_full_dataset(test_loader_bin_pt):

    for node in range(args.node_number, args.max_switches+1):
        #subsubrepo = "./spatial/"
        subrepo = "full" + "_{}".format(args.data) if args.full_dataset else "scarsity_{}".format(args.scarsity_level) + "_{}".format(args.data)
        print(subrepo)
        file_path = subrepo + '/spatial' + args.data + str(node) + "/" + args.feature_type + "/params/torch_model.pt"
        model_bin_pt = torch.load(file_path, weights_only=False, map_location=torch.device('cuda:0'))

        print("Evaluating switch {} model with full dataset".format(node))
        model_bin_pt.eval()
        predictions_bin_pt = []
        labels_bin_pt = []

        # Iterate over batches of the training loader
        for batch_index, batch in enumerate(test_loader_bin_pt):
            features = batch[0].to(get_device())
            label = batch[1].long().to(get_device())
            model_output = model_bin_pt(features)
            predictions_bin_pt.append(np.argmax(model_output.detach().cpu().numpy(), axis=-1))
            labels_bin_pt.append(label.detach().cpu().numpy())
        predictions_bin_pt = [pred for preds in predictions_bin_pt for pred in preds]
        labels_bin_pt = [lbl for lbls in labels_bin_pt for lbl in lbls]

        # Calculcate the metrics
        accuracy_bin_pt = sklearn.metrics.accuracy_score(predictions_bin_pt, labels_bin_pt)
        f1_score_bin_pt = sklearn.metrics.f1_score(predictions_bin_pt, labels_bin_pt)
        tpr = recall_score(labels_bin_pt, predictions_bin_pt) 
        tnr = recall_score(labels_bin_pt, predictions_bin_pt, pos_label = 0) 
        fpr = 1 - tnr

        print('Model performance with full test dataset')
        print('  acc = {:.2f}%'.format(accuracy_bin_pt * float(100)))
        print('  f1 = {:.2f}%'.format(f1_score_bin_pt * float(100)))
        print('  fpr = {:.2f}%'.format(fpr * float(100)))

        sub_directory =  'results/offline_performance_with_full_test_set/' + args.data + '/' + args.feature_type + '/'

        if not os.path.exists(sub_directory):
            os.makedirs(sub_directory)
            
        with open('results/offline_performance_with_full_test_set/' + args.data + '/' + str(node) + '.txt', 'a') as file:
            file.write('Model'+ str(node)+ '\n')
            file.write('  acc = {:.2f}%'.format(accuracy_bin_pt * float(100)) + '\n')
            file.write('  f1 = {:.2f}%'.format(f1_score_bin_pt * float(100)) +  '\n')
            file.write('  fpr = {:.2f}%'.format(fpr * float(100)) +  '\n')

def load_models_and_test_batched_dataset(batched_test_loader_bin_pt):

    for node in range(args.node_number, args.max_switches+1):
        subrepo = "full" + "_{}".format(args.data) if args.full_dataset else "scarsity_{}".format(args.scarsity_level) + "_{}".format(args.data)
        file_path = subrepo + '/spatial' + args.data + str(node) + "/" + args.feature_type + "/params/torch_model.pt"
        model_bin_pt = torch.load(file_path, weights_only=False, map_location=torch.device('cuda:0'))

        print("Evaluating switch {} model with {} batched data".format(node, 2*(args.test_batch)))
        model_bin_pt.eval()
        predictions_bin_pt = []
        labels_bin_pt = []

        # Iterate over batches of the batched testing loader
        for batch_index, batch in enumerate(batched_test_loader_bin_pt):
            # Input batch to the model
            features = batch[0].to(get_device())
            #print(features)
            label = batch[1].long().to(get_device())
            model_output = model_bin_pt(features)
            # Get the predicted categories from the model output
            predictions_bin_pt.append(np.argmax(model_output.detach().cpu().numpy(), axis=-1))
            labels_bin_pt.append(label.detach().cpu().numpy())
        # Restructure predictions and labels into two lists to ease metrics computation
        predictions_bin_pt = [pred for preds in predictions_bin_pt for pred in preds]
        labels_bin_pt = [lbl for lbls in labels_bin_pt for lbl in lbls]


        accuracy_bin_pt = sklearn.metrics.accuracy_score(predictions_bin_pt, labels_bin_pt)
        f1_score_bin_pt = sklearn.metrics.f1_score(predictions_bin_pt, labels_bin_pt)
        tpr = recall_score(labels_bin_pt, predictions_bin_pt)  
        tnr = recall_score(labels_bin_pt, predictions_bin_pt, pos_label = 0) 
        fpr = 1 - tnr
        
        print('Model performance with %d test batch size:' %(2*args.test_batch))
        print('  acc = {:.2f}%'.format(accuracy_bin_pt * float(100)))
        print('  f1 = {:.2f}%'.format(f1_score_bin_pt * float(100)))
        print('  fpr = {:.2f}%'.format(fpr * float(100)))

        main_directory =  'results/offline_performance_batch_size_%d/' %(2*(args.test_batch))
        sub_directory = main_directory + args.data + '/' + args.feature_type + '/'

        if not os.path.exists(sub_directory):
            os.makedirs(sub_directory)
        
        with open(sub_directory + str(node) + '.txt', 'a') as file:
            file.write('Model'+ str(node)+ '\n')
            file.write('  acc = {:.2f}%'.format(accuracy_bin_pt * float(100)) + '\n')
            file.write('  f1 = {:.2f}%'.format(f1_score_bin_pt * float(100)) +  '\n')
            file.write('  fpr = {:.2f}%'.format(fpr * float(100)) +  '\n')
            file.close()

def main(args):
    print(args)
    test_loader, batched_test_loader = load_and_return_full_and_batched(args.data, args.test_batch)
    if args.test_full==True:
        load_models_and_test_full_dataset(test_loader)
    else:
        pass
    load_models_and_test_batched_dataset(batched_test_loader)

if __name__ == '__main__':
    args=define_settings()
    main(args)
