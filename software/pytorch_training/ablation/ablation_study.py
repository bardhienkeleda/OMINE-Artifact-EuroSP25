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
import torch
import os
import argparse

import sklearn
import numpy as np

from trainer import TorchModel
from trainer import get_device
from trainer import load_unsw
from trainer import load_cicids
from trainer import load_and_preprocess_kdd_data
from trainer import build_dataset_tensors
from trainer import train_NN
from tester import load_and_return_full_and_batched
from torchsummary import summary


def define_settings():
    parser = argparse.ArgumentParser(description="Settings for NN hyperparameter tuning.")
    parser.add_argument('--layers',  nargs="+", type=int, default=[8, 4, 4, 4, 2])
    parser. add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--test_batch", type=int, default=2500)
    parser.add_argument("--number_features", type=int, default=7)
    parser.add_argument("--write_train_test", type=bool, default=False)
    parser.add_argument("--run_repetitions", type=int, default=5)
    parser.add_argument("--dataset", type=str, default="cicids")
    parser.add_argument("--type_features", type=str, default="simple")
    parser.add_argument("--full_dataset", type=bool, default=True)
    parser.add_argument("--scarsity_level", type=float, default=0.8)
    
    args = parser.parse_args()
    return args


def test_model(model_bin_pt, test_loader_bin_pt, layers, learning_rate):
        
    model_bin_pt.eval()
    predictions_bin_pt = []
    labels_bin_pt = []

    # Iterate over batches of the training loader
    for batch_index, batch in enumerate(test_loader_bin_pt):
        # Input batch to the model
        features = batch[0].to(get_device())
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

    print('Model performance with full test dataset')
    print('  acc = {:.2f}%'.format(accuracy_bin_pt * float(100)))
    print('  f1 = {:.2f}%'.format(f1_score_bin_pt * float(100)))

    layer_suffix = ''.join(str(l) for l in layers)

    results_directory = "ablation_results" + "/" + layer_suffix
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    
    with open(results_directory + '/performance_with_lr_%s_epochs_%d.txt' %(str(learning_rate), args.epochs), 'a') as file:
        file.write('  acc = {:.2f}%'.format(accuracy_bin_pt * float(100)) + '\n')
        file.write('  f1 = {:.2f}%'.format(f1_score_bin_pt * float(100)) +  '\n')

    return accuracy_bin_pt,f1_score_bin_pt

def main(args):
    print(args)

    #load data and build dataset tensors
    if args.dataset == "kdd":
        train_data, train_labels = load_and_preprocess_kdd_data(args.full_dataset, args.type_features)
    elif args.dataset == "unsw":
        train_data, train_labels = load_unsw(args.full_dataset, args.scarsity_level, args.type_features)
    else:
        train_data, train_labels = load_cicids(args.full_dataset, args.scarsity_level, args.type_features)
    
    train_loader = build_dataset_tensors(train_data, train_labels, args.batch_size)
    test_loader, batched_test_loader = load_and_return_full_and_batched(args.dataset, args.test_batch)

    #build the model and print a summary
    model_bin_pt = TorchModel(layers=args.layers, input_dim=torch.Tensor(train_data.values).shape[1])
    model_bin_pt.to(get_device())
    summary(model_bin_pt, (torch.Tensor(train_data.values).shape[1],))

    # train the model
    accuracy_list = []
    f1_score_list = []
    for i in range (args.run_repetitions):
        model_bin_pt = train_NN(model_bin_pt, train_loader, lr=args.learning_rate, epochs=args.epochs, dataset=args.dataset)
        accuracy, f1_score = test_model(model_bin_pt, test_loader, args.layers, args.learning_rate)
        accuracy_list.append(accuracy)
        f1_score_list.append(f1_score)

    print(np.mean(accuracy_list))
    print(np.mean(f1_score_list))

if __name__ == '__main__':
    args=define_settings()
    main(args)
