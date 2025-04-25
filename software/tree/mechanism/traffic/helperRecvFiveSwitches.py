# *************************************************************************
# 
#  Copyright 2025 Enkeleda Bardhi (TU Delft),
#                 Chenxing Ji (TU Delft),
#                 Ali Imran (University of Michigan),
#                 Muhammad Shahbaz (University of Michigan),
#                 Riccardo Lazzeretti (Sapienza University of Rome),
#                 Mauro Conti (University of Padua),
#                 Fernando Kuipers (TU Delft)
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# 
# *************************************************************************
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from scapy.all import *
import numpy as np


class FeatureHeader(Packet):
    name = "Feature Header"
    
    fields_desc=[IEEEFloatField("field0", 0),    # DNN Input Feature 0
                IEEEFloatField("field1", 0),    # DNN Input Feature 1
                IEEEFloatField("field2", 0),    # DNN Input Feature 2
                IEEEFloatField("field3", 0),    # DNN Input Feature 3
                IEEEFloatField("field4", 0),    # DNN Input Feature 4
                IEEEFloatField("field5", 0),    # DNN Input Feature 5
                IEEEFloatField("field6", 0),    # DNN Input Feature 6
                ByteField("label", 0),   # DNN Label (Ground Truth)
                ByteField("count", 0),
                ByteField("weight5", 2),
                ByteField("weight5_2", 2),
                ByteField("output5", 2),
                ByteField("output6", 7),
                ByteField("ing_port", 0),
                ByteField("weight4", 3),
                ByteField("weight4_2", 3),
                ByteField("output4", 3),

                ByteField("weight3", 4),
                ByteField("weight3_2", 4),
                ByteField("output3", 4),
                
                ByteField("weight2", 5),
                ByteField("weight2_2", 5),
                ByteField("output2", 5),
                
                ByteField("weight1", 6),
                ByteField("weight1_2", 6),
                ByteField("output1", 0)
                ]


bind_layers(IP, FeatureHeader, proto=253)


# Function of calculating DNN metrics
def calc_metrics(pred_outputs=[], true_labels=[]):
    accuracy = 100 * metrics.accuracy_score(true_labels, pred_outputs)
    precision = 100 * metrics.precision_score(true_labels, pred_outputs, average="weighted", labels=np.unique(pred_outputs))
    recall = 100 * metrics.recall_score(true_labels, pred_outputs, average="weighted")
    f1 = 100 * metrics.f1_score(true_labels, pred_outputs, average="weighted", labels=np.unique(pred_outputs))

    print("Weighted Accuracy Across 2 Classes: {0:.2f}".format(accuracy))
    print("Weighted Precision Across 2 Classes: {0:.2f}".format(precision))
    print("Weighted Recall Across 2 Classes: {0:.2f}".format(recall))
    print("Weighted F1-Score Across 2 Classes: {0:.2f}".format(f1))
    if(accuracy < 0.1):
        print("Predicted Outputs: ")
        print(pred_outputs)
        print("Truth label:")
        print(true_labels)
    return accuracy, precision, recall, f1 

def calc_fp_fn(pred_outputs=[], true_labels=[]):
    tpr = metrics.recall_score(true_labels, pred_outputs)
    tnr = metrics.recall_score(true_labels, pred_outputs, pos_label = 0)
    fpr = 1 - tnr
    fnr = 1 - tpr

    print('FPR = {:.2f}%'.format(fpr * float(100)))

def calc_fp_fn_confusion_matrix(pred_outputs=[], true_labels=[]):
    cnf_matrix = confusion_matrix(true_labels, pred_outputs)

    FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix)
    FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
    TP = np.diag(cnf_matrix)
    TN = cnf_matrix.sum() - (FP + FN + TP)

    FP = float(np.sum(FP))
    FN = float(np.sum(FN))
    TP = float(np.sum(TP))
    TN = float(np.sum(TN))

# Compute TPR and FPR for each class
    if (TP == 0 or FN ==0):
        TPR=0
        FPR=0
    else:
        TPR = TP / (TP + FN)
        FPR = FP / (FP + TN)

    print("True positive rate: {0:.3f}".format(TPR))
    print("False positive rate: {0:.3f}".format(FPR))

