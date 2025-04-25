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
import argparse
import math
import time
import torch
import sklearn
import datetime
import pandas as pd
import numpy as np
from torch import nn
from torchsummary import summary
from sklearn.feature_selection import chi2
from sklearn.utils import resample
from torch.utils.data import TensorDataset, DataLoader
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import accuracy_score as sk_acc_func, f1_score as sk_f1_func
from collections import Counter

def define_settings():
    parser = argparse.ArgumentParser(description="Settings for training the switches models.") 
    parser.add_argument("--layers", nargs="+", type=int, default=[8, 4, 4, 4, 2])
    parser. add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--epochs", type=int, required=True)
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--node_number", type=int, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--type_features", type=str, required=True)
    parser.add_argument("--full_dataset", type=bool, default=False)
    parser.add_argument("--scarsity_level", type=float, default=0.8)
    
    args = parser.parse_args()
    return args

def load_and_preprocess_kdd_data(full_dataset, type_features):
    # Load the dataset and prepare the data
    train_df = pd.read_csv('datasets/kdd_dataset/kdd_train_processed.csv')
    test_df = pd.read_csv('datasets/kdd_dataset/kdd_test_processed.csv')
    
    # Convert string columns into categories
    dfs = [train_df, test_df]
    for dataframe in dfs:
      for column in dataframe.columns:
        if column != "labels":
            try:
                dataframe[column]=dataframe[column].astype('float')
            except ValueError:
                dataframe[column]=dataframe[column].astype('category').cat.codes.astype('float')
        else:
            dataframe[dataframe[column] != "normal"] = 1
            dataframe[dataframe[column] == "normal"] = 0
            dataframe[column]=dataframe[column].astype('int')
  
    testing_df=test_df

    # Get the data and labels for the binary classification
    train_features_df = train_df[train_df.columns[~train_df.columns.isin(['labels'])]]
    test_features_df = testing_df[testing_df.columns[~testing_df.columns.isin(['labels'])]]

    # Get binary labels
    train_labels_binary_df = train_features_df['labels']
    test_labels_binary_df = testing_df['labels']
    
    # Normalize the data
    scaler = MinMaxScaler()
    scaler.fit(train_features_df)
    train_features_df = pd.DataFrame(scaler.transform(train_features_df), columns=train_features_df.columns)
    test_features_df = pd.DataFrame(scaler.transform(test_features_df), columns=test_features_df.columns)

    # Choose among the type of features (simple, mid or complex)
    if full_dataset==True:
       pass
    else:
      if type_features=="simple":
        other_features_to_keep=['dst_bytes', 'urgent', 'service']
        
      elif type_features=="mid":
        other_features_to_keep=['num_outbound_cmds', 'num_root', 'dst_host_srv_count', 'su_attempted', 
                                'num_shells', 'is_host_login', 'logged_in', 'srv_count']
      
      elif type_features=="simple_mid_features":
        other_features_to_keep=['dst_bytes', 'urgent', 'service', 'num_outbound_cmds', 'num_root', 
                                'dst_host_srv_count', 'su_attempted', 'num_shells', 'is_host_login',
                                'logged_in', 'srv_count']
      
      elif type_features=="best_7_features":
         other_features_to_keep=['dst_host_serror_rate', 'dst_host_diff_srv_rate', 'num_outbound_cmds', 
                                'dst_bytes', 'urgent', 'num_root', 'dst_host_srv_count']
      else:
        other_features_to_keep=['dst_host_serror_rate', 'dst_host_diff_srv_rate', 'rerror_rate', 
                                'same_srv_rate', 'dst_host_srv_serror_rate', 'srv_diff_host_rate',
                                'dst_host_same_srv_rate']

      columns_to_keep_bool = train_features_df.columns.isin(other_features_to_keep)
      train_features_df = train_features_df[train_features_df.columns[columns_to_keep_bool]]
      test_features_df = test_features_df[test_features_df.columns[columns_to_keep_bool]]
    
    print('*** The train data has the following shape: ***')
    print(train_features_df.shape)

    print('*** The test data has the following shape: ***')
    print(test_features_df.shape)

    return train_features_df, train_labels_binary_df

def load_unsw(full_dataset, scarsity_level, type_features):

  if full_dataset == True:
    train_data = pd.read_csv("datasets/unsw_train_data.csv")
    train_labels = pd.read_csv("datasets/unsw_train_labels.csv", index_col=0) 
    train_data.reset_index(inplace=True, drop=True)
    train_labels.reset_index(inplace=True, drop=True)
    full_train_data = pd.concat([train_data, train_labels], axis=1) #, axis=1
    full_train_data = full_train_data.sample(frac=1, random_state=12345).reset_index(drop=True)
  else:
    train_data = pd.read_csv("datasets/unsw_train_data.csv",  index_col=0)
    train_labels =  pd.read_csv("datasets/unsw_train_labels.csv", index_col=0)
    train_data.reset_index(inplace=True, drop=True)
    train_labels.reset_index(inplace=True, drop=True)
    full_train_data = pd.concat([train_data, train_labels], axis=1) #, axis=1
    full_train_data = full_train_data.sample(frac=scarsity_level, random_state=12345).reset_index(drop=True)
  
  # Choose among the type of features (simple, mid or complex)
  if type_features=="simple":
    features=['dttl', 'swin', 'sttl', 'dtcpb', 'dwin', 'service', 'stcpb']

  elif type_features=="mid":
    features=['ct_dst_sport_ltm', 'ct_dst_src_ltm', 'dload', 'ct_srv_dst', 'ct_state_ttl',
              'ct_srv_src', 'synack', 'ct_dst_ltm', 'tcprtt', 'sinpkt', 'ackdat']
  
  elif type_features=="simple_mid_features":
    features=['dttl', 'swin', 'sttl', 'dtcpb', 'dwin', 'service', 'stcpb', 'ct_dst_sport_ltm',
              'ct_dst_src_ltm', 'dload', 'ct_srv_dst', 'ct_state_ttl', 'ct_srv_src', 'synack',
              'ct_dst_ltm', 'tcprtt', 'sinpkt', 'ackdat']
  
  elif type_features=="best_7_features":
      features=['dttl', 'swin', 'dload', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_srv_dst', 'sttl']
  else:
    features=['rate', 'dmean']

  columns_to_keep_bool = full_train_data.columns.isin(features)
  train_data = full_train_data[full_train_data.columns[columns_to_keep_bool]]
  train_labels = full_train_data['label']

  print("Training data shape: {}".format(train_data.shape))
  print("Training labels shape: {}".format(train_labels.shape))

  return train_data, train_labels

def load_cicids(full_dataset, scarsity_level, type_features):

  if full_dataset == True:
    train_data = pd.read_csv("datasets/cicids_train_data.csv")
    train_labels = pd.read_csv("datasets/cicids_train_labels.csv", index_col=0)
    train_data.reset_index(inplace=True, drop=True)
    train_labels.reset_index(inplace=True, drop=True)
    full_train_data = pd.concat([train_data, train_labels], axis=1) #, axis=1
    full_train_data = full_train_data.sample(frac=1, random_state=12345).reset_index(drop=True)
  else:
    train_data = pd.read_csv("datasets/train/cicids_train_data.csv",  index_col=0)
    train_labels =  pd.read_csv("datasets/train/cicids_train_labels.csv", index_col=0)
    train_labels.reset_index(inplace=True, drop=True)
    full_train_data = pd.concat([train_data, train_labels], axis=1) #, axis=1
    full_train_data = full_train_data.sample(frac=scarsity_level, random_state=12345).reset_index(drop=True)

  if type_features=="simple":
    features=["Destination Port"]
      
  elif type_features=="mid":
    features=["URG Flag Count", "Bwd IAT Total", "Init_Win_bytes_forward", "PSH Flag Count"]
  
  elif type_features=="simple_mid_features":
    features=["Destination Port","URG Flag Count", "Bwd IAT Total", "Init_Win_bytes_forward", 
              " PSH Flag Count"]
  
  elif type_features=="best_7_features":
    features=["Destination Port", "Bwd Packet Length Min", "Packet Length Variance", 
              "URG Flag Count", "Fwd Packet Length Max", "Avg Fwd Segment Size", 
              "Fwd Packet Length Mean"]
      
  else:
    features=['Bwd Packet Length Min', 'Packet Length Variance', 'Fwd Packet Length Max',
                'Avg Fwd Segment Size', 'Fwd Packet Length Mean', 'Fwd IAT Std', 
                'Avg Bwd Segment Size', 'Flow IAT Std', 'Fwd Packet Length Std', 
                'Bwd Packet Length Std', 'Packet Length Std', 'Bwd Packet Length Max',
                'Bwd Packet Length Mean', 'Max Packet Length', 'Fwd IAT Max']

  
  columns_to_keep_bool = full_train_data.columns.isin(features)
  train_data = full_train_data[full_train_data.columns[columns_to_keep_bool]]
  train_labels = full_train_data['Label']

  print("Training data shape: {}".format(train_data.shape))
  print("Training labels shape: {}".format(train_labels.shape))
  
  return train_data, train_labels 

def get_device():

    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
    return device

def build_dataset_tensors(train_features_df, train_labels_binary_df, batch_size):

    train_tensor_dataset_bin_pt = TensorDataset(torch.Tensor(train_features_df.values), torch.Tensor(train_labels_binary_df.values))
    train_loader_bin_pt = DataLoader(dataset=train_tensor_dataset_bin_pt, batch_size=batch_size, shuffle=True)

    return train_loader_bin_pt #, test_loader_bin_pt

# Setup model
class TorchModel(torch.nn.Module):
  def __init__(self, layers, input_dim):
    super(TorchModel, self).__init__()
    # Use ModuleList to define consecutive layers using a for loop
    self.layers = nn.ModuleList()
    last_dim = input_dim
    for index, layer in enumerate(layers):
      # Append fully connected layer
        self.layers.append(torch.nn.Linear(last_dim, layer))
      # Update last dimension for next layer
        last_dim = layer
      # Append activation layer
        self.layers.append(torch.nn.Softmax(dim=-1) if index==len(layers)-1 else torch.nn.ReLU())
    # Apply the custom initialization to every fully connected layer
        self.apply(TorchModel.initialize_weights)

  @staticmethod
  def initialize_weights(m):
    # Custom weight initialization to make results to be as adherent as possible between PyTorch and Tensorflow
    if isinstance(m, nn.Linear):
      nn.init.xavier_uniform_(m.weight.data)
      nn.init.zeros_(m.bias.data)

  def forward(self, x):
    # Pass input through all consecutive layers
    for layer in self.layers:
      x = layer(x)
    return x

def format_time(elapsed):
  # Function to show elapsed time in decent format
  elapsed_rounded = int(round(elapsed))
  return str(datetime.timedelta(seconds=elapsed_rounded))

def print_message(epoch, tot_epochs, index, size, loss,
                  metrics=None, time=None):
  # Function to print an info message in every step of the pytorch training
  message = '| Epoch: {}/{} |'.format(epoch, tot_epochs)
  # Define bar showing progress update
  bar_length = 10
  progress = float(index) / float(size)
  if progress >= 1.:
    progress = 1
  block = int(round(bar_length * progress))
  message += '[{}]'.format('=' * block + ' ' * (bar_length - block))
  # Add loss, metrics and timing to the message
  message += '| TRAIN: '
  if loss is not None:
    message += 'loss={:.3f} '.format(loss)
  if metrics is not None:
    metrics_message = ''
    for metric_name, metric_value in metrics.items():
        metrics_message += '{}={:.2f}% '.format(metric_name,
                                                metric_value * float(100))
    message += metrics_message
  if time is not None:
    message += '| time: {} '.format(format_time(time))
  message += ''
  message += '|'
  print(message, end='\r')

def train_NN(model_bin_pt, train_loader_bin_pt):
    # Define loss and optimizer
    loss_func_pt = torch.nn.CrossEntropyLoss()
    optimizer_pt = torch.optim.Adam(model_bin_pt.parameters(), args.learning_rate)
    # Setup metrics depending on the choice
    metrics = {'acc': sk_acc_func, 'f1': sk_f1_func}
    # Define initial best loss to infinity
    best_loss = math.inf
    # Keep track of time
    epoch_t0 = time.time()
    # Set model to training mode
    model_bin_pt.train()
    # Log start of training
    print("Training...")
    for epoch in range(args.epochs):
            running_loss = 0.
            running_scores = {met_name: 0.0 for met_name in metrics.keys()}
            epoch_starting_time = time.time()
              # Iterate over batches of the training loader
            for batch_index, batch in enumerate(train_loader_bin_pt):
                # Zero gradient of optimizer
                optimizer_pt.zero_grad()
                # Input batch to the model
                features = batch[0].to(get_device())
                labels = batch[1].long().to(get_device())
                model_output = model_bin_pt(features)
                loss = loss_func_pt(model_output, labels)
                loss.backward()
                # Update model
                optimizer_pt.step()
                # Add loss to total loss for message info
                running_loss += loss.item()

                for metric_name, metric_func in metrics.items():
                    predictions = np.argmax(model_output.detach().cpu().numpy(), axis=-1)
                    running_scores[metric_name] += metric_func(y_pred=predictions, y_true=labels.detach().cpu())
                # Average out loss and metrics
                avg_loss = running_loss / (batch_index + 1)
                avg_scores = {met_name: met_value / (batch_index + 1) for met_name, met_value in running_scores.items()}
                # Print training information
                print_message(epoch=epoch + 1,
                          tot_epochs=args.epochs,
                          index=batch_index + 1,
                          size=len(train_loader_bin_pt),
                          loss=avg_loss,
                          metrics=avg_scores,
                          time=time.time() - epoch_starting_time)
            print('')
    print('Total training time: {}'.format(format_time(time.time() - epoch_t0)))
    return model_bin_pt

def write_parameters(model_bin_pt):

    #os.chdir("../spatial/")
    subrepo = "full" + "_{}".format(args.dataset) if args.full_dataset else "scarsity_{}".format(args.scarsity_level) + "_{}".format(args.dataset)
    if not os.path.exists(subrepo):
      os.makedirs(subrepo)
    if not os.path.exists(subrepo + "/spatial"+ args.dataset + str(args.node_number) + "/" + args.type_features + "/params"):
      os.makedirs(subrepo + "/spatial" + args.dataset + str(args.node_number) + "/" + args.type_features + "/params")

    #os.mkdir("spatial" + "/params")

    print('Dumping the model weights...')
    for indx, layer in enumerate(model_bin_pt.layers):
        if isinstance(layer, torch.nn.Linear):
            #print(indx, layer)
            subrepo = "full" + "_{}".format(args.dataset) if args.full_dataset else "scarsity_{}".format(args.scarsity_level) + "_{}".format(args.dataset)
            weight_file =  subrepo + "/spatial" + args.dataset + str(args.node_number) + "/" + args.type_features + "/params" + "/" + "L" + str(indx) + "_W" + ".csv"
            bias_file = subrepo + "/spatial" + args.dataset + str(args.node_number) + "/" + args.type_features + "/params" + "/" + "L" + str(indx) + "_B" + ".csv"

            weight = layer.state_dict()['weight']
            bias = layer.state_dict()['bias']

            weight = weight.cpu().numpy()
            weight_df = pd.DataFrame(weight)
            weight_df.to_csv(weight_file, header = False, index=False)

            bias = bias.cpu().numpy()
            bias_df = pd.DataFrame(bias)
            bias_df.to_csv(bias_file, header = False, index=False)

    print('Dumping the trained model...')
    dump_path = subrepo + "/spatial" + args.dataset + str(args.node_number) + "/" + args.type_features + "/params" + "/torch_model.pt"
    torch.save(model_bin_pt, dump_path)


def main(args):
    print(args)

    if args.dataset == "kdd":
      train_data, train_labels = load_and_preprocess_kdd_data(args.full_dataset, args.type_features)
    elif args.dataset == "unsw":
      train_data, train_labels = load_unsw(args.full_dataset, args.scarsity_level, args.type_features) 
    else:
      train_data, train_labels = load_cicids(args.full_dataset, args.scarsity_level, args.type_features) 

    train_loader = build_dataset_tensors(train_data, train_labels, args.batch_size)
    # Build the model
    model_bin_pt = TorchModel(layers=args.layers, input_dim=torch.Tensor(train_data.values).shape[1])
    model_bin_pt.to(get_device())

    # Print a summary of the constructed model
    summary(model_bin_pt, (torch.Tensor(train_data.values).shape[1],))

    # Train and write the model down
    trained_model = train_NN(model_bin_pt, train_loader)
    write_parameters(trained_model)

if __name__ == '__main__':
    args=define_settings()
    main(args)
