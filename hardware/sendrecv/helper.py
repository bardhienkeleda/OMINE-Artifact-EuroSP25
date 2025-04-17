# *************************************************************************
#
# Copyright 2022 Tushar Swamy (Stanford University),
#                Alexander Rucker (Stanford University),
#                Annus Zulfiqar (Purdue University),
#                Muhammad Shahbaz (Stanford/Purdue University)
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

from sklearn import metrics
from scapy.all import *
import numpy as np


# Feature Header Protocol for Scapy
class FeatureHeader(Packet):
    name = "Feature Header"
    fields_desc=[BitField("field0", 0, 32),    # DNN Input Feature 0
                BitField("field1", 0, 32),    # DNN Input Feature 1
                BitField("field2", 0, 32),    # DNN Input Feature 2
                BitField("field3", 0, 32),    # DNN Input Feature 3
                BitField("field4", 0, 32),    # DNN Input Feature 4
                BitField("field5", 0, 32),    # DNN Input Feature 5
                BitField("field6", 0, 32),    # DNN Input Feature 6
                ByteField("label", 0),   # DNN Label (Ground Truth)
                ByteField("output", 0)]  # DNN Output

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
    print("")
    
def calc_fp_fn(pred_outputs=[], true_labels=[]):
    tpr = metrics.recall_score(true_labels, pred_outputs)
    tnr = metrics.recall_score(true_labels, pred_outputs, pos_label = 0)
    fpr = 1 - tnr
    fnr = 1 - tpr

    print('FPR = {:.2f}%'.format(fpr * float(100)))
