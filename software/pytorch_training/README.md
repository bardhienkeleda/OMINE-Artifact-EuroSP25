# Code for O'MINE PyTorch Training 

This directory comprises various aspects included in the paper, i.e., ablation study, training and testing of neural networks used for DDoS detection in the switches. The `datasets/` directory contains the train and test data that we use for all the experiments in our paper.

## Ablation study

The scripts in `ablation/` directory contains the scripts for running the ablation study and ploting the results (see Figure 3 in the paper). 

## Train models

To train models, we use a fixed neural network structure, i.e., [8x4x4x4x2]. Also, we use three state-of-the-art network security datasets for training the models, i.e., UNSW-NB15, NSL-KDD and CICIDS-2017. Models can be trained in the full set of data or with different scarcity levels (as described in the paper). 

To train a specific model on the full dataset, the following command should do the trick:

```sh
python3 trainer.py --epochs 10 --node_number 1 --dataset "cicids" --type_features "best_7_features" --full_dataset True
```
> **Note:** Following the results from the ablation study, the following parameters should be fixed: batch_size=32, lr=0.001, epochs=10 (only for CICIDS-2017) and epochs=30 (for NSL-KDD and UNSW-NB15).

Instead, to train a specific model on a data scarcity setting, the following command should do the trick:

```sh
python3 trainer.py --epochs 10 --node_number 1 --dataset "cicids" --type_features "best_7_features" --full_dataset False --scarsity_level 0.01
```
> **Note:** In the O'MINE paper we run experiments considering a scarsity level of 0.5% (0.0005) for the CICIDS-2017 and 1% (0.01) for the UNSW-NB15.

To automatize the process of training, `trainer.sh` script should be able to train multiple models by varying different hyperparameters.

## Test models

After the models training and saving the models in `full_{dataset}` or `scarcity_{scarcity_level}_{dataset}` directories, the user can test the models by running the following command:

```sh
python3 tester.py --test_batch 2500 --node_number 1 --data "cicids" --feature_type "best_7_features" --full_dataset False --scarsity_level 0.01
```
> **Note:** Similarly as for training, the user can select either a full or a scarce training dataset as a setting for testing the models. Aditionally, the `test_batch` parameter should be kept 2500 to reproduce the same results represented in the paper. Lastly, to automatize the process of testing, `tester.sh` script should do the job.