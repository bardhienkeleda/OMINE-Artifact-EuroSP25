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

import signal
import pdb
signal.signal(signal.SIGINT, lambda signum, frame: exit(1))

from scapy.all import *
from helper import *

MAX_PKT_COUNT = 5000

# Parse and process incoming packets
run_pkt_count = 0
batch_count = 0
pred_outputs1 = list()
pred_outputs2 = list()
pred_outputs3 = list()
pred_outputs4 = list()
pred_outputs5 = list()
pred_outputs6 = list()

true_labels = list()

prev_incorrect_count = 0



def compute_majority_voting_results(outputs, weights):
    if(len(outputs) != len(weights)):
        print("Error: incompatible size for outputs and weights")

    # mimic the switch code
    sum_ones = 0
    sum_zero = 0
    voted_ones = 0
    voted_zero = 0

    for i in range(len(outputs)):
        if(outputs[i] == 1):
            sum_ones = sum_ones + weights[i]
            voted_ones = voted_ones + 1
        elif(outputs[i] == 0):
            sum_zero = sum_zero + weights[i]
            voted_zero = voted_zero + 1
        else:
            print("Eror: unsupported output value")
    
    if(sum_ones > sum_zero):
        return 1 
    elif(sum_ones == sum_zero):
        return (voted_ones > voted_zero)
    else:
        return 0    



def calc_inc_count (outputs, final_pred):
    count = 0
    for output in outputs:
        if output != final_pred:
            count += 1
    return count

def parse_output(pkt):
    global  batch_count, run_pkt_count, pred_outputs1, pred_outputs2, pred_outputs3,\
        pred_outputs4, pred_outputs5, pred_outputs6, true_labels

    run_pkt_count += 1
    pred_outputs1.append(pkt[FeatureHeader].output1)
    pred_outputs2.append(pkt[FeatureHeader].output2)
    pred_outputs3.append(pkt[FeatureHeader].output3)
    pred_outputs4.append(pkt[FeatureHeader].output4)
    pred_outputs5.append(pkt[FeatureHeader].output5)
    pred_outputs6.append(pkt[FeatureHeader].output6)

    true_labels.append(pkt[FeatureHeader].label)


    if run_pkt_count % 1 == 0:
        print("Received {0} packets in total.".format(run_pkt_count))


        print("Switch 1 metrics: ")
        accuracy1, precision1, recall1, f11 = calc_metrics(pred_outputs1, true_labels)
        print("Switch 2 metrics: ")
        accuracy2, precision2, recall2, f12 = calc_metrics(pred_outputs2, true_labels)
        print("Switch 3 metrics: ")
        accuracy3, precision3, recall3, f13 = calc_metrics(pred_outputs3, true_labels)
        print("Switch 4 metrics: ")
        accuracy4, precision4, recall4, f14 = calc_metrics(pred_outputs4, true_labels)
        print("Switch 5 metrics: ")
        accuracy5, precision5, recall5, f15 = calc_metrics(pred_outputs5, true_labels)
        print("Switch 5 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs6, true_labels)

        print("FPR for baseline (measured in switch1): ")
        calc_fp_fn(pred_outputs1, true_labels)
        print("FPR for baseline (measured in switch2): ")
        calc_fp_fn(pred_outputs2, true_labels)
        print("FPR for baseline (measured in switch3): ")
        calc_fp_fn(pred_outputs3, true_labels)
        print("FPR for baseline (measured in switch4): ")
        calc_fp_fn(pred_outputs4, true_labels)
        print("FPR for baseline (measured in switch5): ")
        calc_fp_fn(pred_outputs5, true_labels)

        print("FPR for our mechanism (measured in switch5): ")
        calc_fp_fn(pred_outputs6, true_labels)


        weights = [pkt[FeatureHeader].weight1 << 8 | pkt[FeatureHeader].weight1_2,
                   pkt[FeatureHeader].weight2 << 8 | pkt[FeatureHeader].weight2_2,
                   pkt[FeatureHeader].weight3 << 8 | pkt[FeatureHeader].weight3_2,
                   pkt[FeatureHeader].weight4 << 8 | pkt[FeatureHeader].weight4_2,
                   pkt[FeatureHeader].weight5 << 8 | pkt[FeatureHeader].weight5_2]

        incorrect_count = calc_inc_count([pkt[FeatureHeader].output1, 
                                          pkt[FeatureHeader].output2, pkt[FeatureHeader].output3,
                                          pkt[FeatureHeader].output4, pkt[FeatureHeader].output5], 
                                          pkt[FeatureHeader].output6)
        
        final_decision = compute_majority_voting_results([pkt[FeatureHeader].output1, 
                                          pkt[FeatureHeader].output2, pkt[FeatureHeader].output3,
                                          pkt[FeatureHeader].output4, pkt[FeatureHeader].output5],
                                          weights)
        
        if(final_decision != pkt[FeatureHeader].output6):
            print("Prediction result error final decision with python: {} and receved decision: {}").format(
                final_decision, pkt[FeatureHeader].output6)

        print("Incorrect Count contained in the packet: {}".format(pkt[FeatureHeader].incorrect_count))
        print("Computed at recv: {} packets have made the incorrect prediction ".format(incorrect_count))
        if(pkt[FeatureHeader].output1 != pkt[FeatureHeader].output6):
            print("Incorrect Switch 1")     
        if(pkt[FeatureHeader].output2 != pkt[FeatureHeader].output6):
            print("Incorrect Switch 2")     
        if(pkt[FeatureHeader].output3 != pkt[FeatureHeader].output6):
            print("Incorrect Switch 3")     
        if(pkt[FeatureHeader].output4 != pkt[FeatureHeader].output6):
            print("Incorrect Switch 4")      
        if(pkt[FeatureHeader].output5 != pkt[FeatureHeader].output6):
            print("Incorrect Switch 5")     
        
        prev_incorrect_count = incorrect_count
        # print("Switch1 weight: {}".format(weights[0]))
        # print("Switch2 weight: {}".format(weights[1]))
        # print("Switch3 weight: {}".format(weights[2]))
        # print("Switch4 weight: {}".format(weights[3]))
        # print("Switch5 weight: {}".format(weights[4]))
        
        



    # Calculate metrics for every 60 packets
    if run_pkt_count == MAX_PKT_COUNT:
        batch_count += 1
        print("Received {0} packets.".format(MAX_PKT_COUNT))

        print("Switch 1 metrics: ")
        accuracy1, precision1, recall1, f11 = calc_metrics(pred_outputs1, true_labels)
        print("Switch 2 metrics: ")
        accuracy2, precision2, recall2, f12 = calc_metrics(pred_outputs2, true_labels)
        print("Switch 3 metrics: ")
        accuracy3, precision3, recall3, f13 = calc_metrics(pred_outputs3, true_labels)
        print("Switch 4 metrics: ")
        accuracy4, precision4, recall4, f14 = calc_metrics(pred_outputs4, true_labels)
        print("Switch 5 metrics: ")
        accuracy5, precision5, recall5, f15 = calc_metrics(pred_outputs5, true_labels)
        print("Switch 5 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs6, true_labels)

        print("FPR for baseline (measured in switch1): ")
        calc_fp_fn(pred_outputs1, true_labels)
        print("FPR for baseline (measured in switch2): ")
        calc_fp_fn(pred_outputs2, true_labels)
        print("FPR for baseline (measured in switch3): ")
        calc_fp_fn(pred_outputs3, true_labels)
        print("FPR for baseline (measured in switch4): ")
        calc_fp_fn(pred_outputs4, true_labels)
        print("FPR for baseline (measured in switch5): ")
        calc_fp_fn(pred_outputs5, true_labels)

        print("FPR for our mechanism (measured in switch5): ")
        calc_fp_fn(pred_outputs6, true_labels)

        run_pkt_count = 0
        pred_outputs1 = list()
        pred_outputs2 = list()
        pred_outputs3 = list()
        pred_outputs4 = list()
        pred_outputs5 = list()
        pred_outputs6 = list()
        true_labels = list()


# Sniff packets with feature headers
while True:
    sniff(iface='h2-eth0', prn=lambda x:parse_output(x), count=MAX_PKT_COUNT,
          lfilter=lambda x: (IP in x) and (x[IP].proto == 253))
