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
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt 

def define_settings():
    parser = argparse.ArgumentParser(description="Settings for ploting the ablation study plots.")
    parser.add_argument("--NN_structure", type=str, required=True)
    parser.add_argument("--learning_rate", nargs="+", type=int, default=[str(0.001), str(0.0025), str(0.01)])
    parser.add_argument("--epochs", nargs="+", type=int, default=[10, 20, 30])
    parser.add_argument("--dataset", type=str, default="cicids")

    args = parser.parse_args()
    return args

def load_results_for_fixed_structure(structure, dataset, learning_rate, epochs):
    print("Loading results for structure %s" %(structure))
    # read text file into dictionary
    results_dict = {lr: {epoch: {"acc": [], "f1": []} for epoch in epochs} for lr in learning_rate}
    for lr_index in learning_rate:
        for epoch_number in epochs:
            results_df_epoch = pd.read_csv("ablation_results/" + structure + '/' + dataset + "/performance_with_lr_" + str(lr_index) + "_epochs_" + str(epoch_number) + ".txt", sep=" ", header=None)
            results_df_epoch.drop([0, 1, 3],axis=1, inplace=True)
            acc, f1 = parse_accuracy_f1(results_df_epoch)
            results_dict[lr_index][epoch_number]["acc"] = acc
            results_dict[lr_index][epoch_number]["f1"] = f1

    return results_dict

def parse_accuracy_f1(results):
    accuracy = []
    f1_score = []
    for index, row in results.iterrows():
        if row[2] == "acc":
            row[4] = row[4][:-1]
            row[4] = float(row[4])
            accuracy.append(row[4])
        else:
            row[4] = row[4][:-1]
            row[4] = float(row[4])
            f1_score.append(row[4])

    return accuracy, f1_score

def plot_accuracy_results(structure, dataset, results, learning_rate, epochs):
    results_dict = {lr: {epoch: {"avg_acc": [], "std_acc": []} for epoch in epochs} for lr in learning_rate}

    for lr_index in learning_rate:
        for epoch in epochs:
            results_dict[lr_index][epoch]["avg_acc"] = np.mean(results[lr_index][epoch]["acc"])
            results_dict[lr_index][epoch]["std_acc"] = np.std(results[lr_index][epoch]["acc"])
        print(results_dict)
    
    plot_shades = ["#a6611a", "#dfc27d", "#018571"]
    for k, epoch in enumerate(epochs):
        averages_acc = []
        std_acc = []
        for lr_index in learning_rate:
            averages_acc.append(results_dict[lr_index][epoch]["avg_acc"])
            std_acc.append(results_dict[lr_index][epoch]["std_acc"])
        xs = [lr_index for lr_index in learning_rate]
        print(xs)
        plt.plot(xs, averages_acc, c=plot_shades[k], marker='s', label="Epochs={}".format(epoch))
        plt.fill_between(xs, [averages_acc[i] - std_acc[i] for i in range(len(learning_rate))], 
                         [averages_acc[i] + std_acc[i] for i in range(len(learning_rate))], alpha=0.5, edgecolor=plot_shades[k], facecolor=plot_shades[k])
    plt.xlabel("Learning rate", size=14)
    plt.ylabel("Average accuracy", size=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc='lower left', prop={'size': 14})
    plt.savefig('ablation_results/' + structure + '/' + dataset + '/accuracy_VS_lr_for_each_epoch.pdf')
    plt.show()

def plot_f1score_results(structure, dataset, results, learning_rate, epochs):
    results_dict = {lr: {epoch: {"avg_f1": [], "std_f1": []} for epoch in epochs} for lr in learning_rate}

    for lr_index in learning_rate:
        for epoch in epochs:
            results_dict[lr_index][epoch]["avg_f1"] = np.mean(results[lr_index][epoch]["f1"])
            results_dict[lr_index][epoch]["std_f1"] = np.std(results[lr_index][epoch]["f1"])
        print(results_dict)
    
    plot_shades = ["#c2a5cf", "#a6dba0", "#008837"]
    for k, epoch in enumerate(epochs):
        averages_f1 = []
        std_f1 = []
        for lr_index in learning_rate:
            averages_f1.append(results_dict[lr_index][epoch]["avg_f1"])
            std_f1.append(results_dict[lr_index][epoch]["std_f1"])
        xs = [lr_index for lr_index in learning_rate]
        print(xs)
        plt.plot(xs, averages_f1, c=plot_shades[k], marker='s', label="Epochs={}".format(epoch))
        plt.fill_between(xs, [averages_f1[i] - std_f1[i] for i in range(len(learning_rate))], 
                         [averages_f1[i] + std_f1[i] for i in range(len(learning_rate))], alpha=0.5, edgecolor=plot_shades[k], facecolor=plot_shades[k])
    plt.xlabel("Learning rate", size=14)
    plt.ylabel("Average F1-score", size=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc='lower left', prop={'size': 14})
    plt.savefig('ablation_results/' + structure + '/' +  dataset + '/f1score_VS_lr_for_each_epoch.pdf')
    plt.show()     

def plot_accuracy_f1score_results(structure, dataset, results, learning_rate, epochs):  
    fig1, ax1 = plt.subplots(1, 2, sharey=True)
    results_dict = {lr: {epoch: {"avg_acc": [], "std_acc": []} for epoch in epochs} for lr in learning_rate}

    for lr_index in learning_rate:
        for epoch in epochs:
            results_dict[lr_index][epoch]["avg_acc"] = np.mean(results[lr_index][epoch]["acc"])
            results_dict[lr_index][epoch]["std_acc"] = np.std(results[lr_index][epoch]["acc"])
        print(results_dict)
    
    plot_shades = ["#a6611a", "#dfc27d", "#018571"]
    for k, epoch in enumerate(epochs):
        averages_acc = []
        std_acc = []
        for lr_index in learning_rate:
            averages_acc.append(results_dict[lr_index][epoch]["avg_acc"])
            std_acc.append(results_dict[lr_index][epoch]["std_acc"])
        xs = [lr_index for lr_index in learning_rate]
        print(xs)
        ax1[0].plot(xs, averages_acc, c=plot_shades[k], marker='s', label="Epochs={}".format(epoch))
        ax1[0].fill_between(xs, [averages_acc[i] - std_acc[i] for i in range(len(learning_rate))], 
                         [averages_acc[i] + std_acc[i] for i in range(len(learning_rate))], alpha=0.5, edgecolor=plot_shades[k], facecolor=plot_shades[k])
    ax1[0].set_xlabel("Learning rate", fontsize=14)
    ax1[0].set_ylabel("Average accuracy", fontsize=14)
    ax1[0].legend(loc='lower left', prop={'size': 14})

    results_dict = {lr: {epoch: {"avg_f1": [], "std_f1": []} for epoch in epochs} for lr in learning_rate}

    for lr_index in learning_rate:
        for epoch in epochs:
            results_dict[lr_index][epoch]["avg_f1"] = np.mean(results[lr_index][epoch]["f1"])
            results_dict[lr_index][epoch]["std_f1"] = np.std(results[lr_index][epoch]["f1"])
        print(results_dict)
    
    plot_shades = ["#c2a5cf", "#a6dba0", "#008837"]
    for k, epoch in enumerate(epochs):
        averages_f1 = []
        std_f1 = []
        for lr_index in learning_rate:
            averages_f1.append(results_dict[lr_index][epoch]["avg_f1"])
            std_f1.append(results_dict[lr_index][epoch]["std_f1"])
        xs = [lr_index for lr_index in learning_rate]
        print(xs)
        ax1[1].plot(xs, averages_f1, c=plot_shades[k], marker='s', label="Epochs={}".format(epoch))
        ax1[1].fill_between(xs, [averages_f1[i] - std_f1[i] for i in range(len(learning_rate))], 
                         [averages_f1[i] + std_f1[i] for i in range(len(learning_rate))], alpha=0.5, edgecolor=plot_shades[k], facecolor=plot_shades[k])
    ax1[1].set_xlabel("Learning rate", fontsize=14)
    ax1[1].set_ylabel("Average F1-score", fontsize=14)
    ax1[1].legend(loc='lower left', prop={'size': 14})
    plt.tight_layout()
    plt.savefig('ablation_results/' + structure + '/' + dataset + '/accuracy_and_f1score_VS_lr_for_each_epoch.pdf')
    plt.show()


def main(args):
    print(args)
    results = load_results_for_fixed_structure(args.NN_structure, args.dataset, args.learning_rate, args.epochs)
    plot_accuracy_results(args.NN_structure, args.dataset, results, args.learning_rate, args.epochs)
    plot_f1score_results(args.NN_structure,  args.dataset, results, args.learning_rate, args.epochs)
    plot_accuracy_f1score_results(args.NN_structure,  args.dataset, results, args.learning_rate, args.epochs)

if __name__=='__main__':
    args = define_settings()
    main(args)