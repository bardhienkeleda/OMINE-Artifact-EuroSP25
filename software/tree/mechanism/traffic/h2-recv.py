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
import signal
import pdb
signal.signal(signal.SIGINT, lambda signum, frame: exit(1))

from scapy.all import *
import importlib

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
pred_outputs7 = list()
pred_outputs8 = list()
pred_outputs9 = list()
pred_outputs10= list()
true_labels = list()

import argparse


args = None

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
        return (voted_ones > voted_zero) #assumption here is we have odd number of voters
    else:
        return 0    



def calc_inc_count (outputs, final_pred):
    count = 0
    for output in outputs:
        if output != final_pred:
            count += 1
    return count


def parse_args():
    global args
    parser = argparse.ArgumentParser(description="Select a host (h1, h2, h3, or h4). Default is h4.")
    parser.add_argument(
        "--host",
        choices=["h1", "h2", "h3", "h4"],  # Restricts input to these values
        default="h4",                      # Default value if not provided
        help="Specify the host (h1, h2, h3, or h4). Default is h4."
    )
    
    parser.add_argument(
        "--num-hops", type=int,
        choices=[3,5,7,9], default=5,
        help="Specify the number of hops you are collecting the results for."
    )

    args = parser.parse_args()

def debug_output(pkt):
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
    print("packet received")
    for field in FeatureHeader.fields_desc:
        print "{}: {}".format(field.name, pkt[FeatureHeader].getfieldval(field.name))
    if run_pkt_count % 100 == 0:
        print("Received {} packets".format(run_pkt_count))
        
    if run_pkt_count == MAX_PKT_COUNT :
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


def parse_output_three_hops(pkt):
    global  batch_count, run_pkt_count, pred_outputs1, pred_outputs2, pred_outputs3,\
        pred_outputs4, pred_outputs5, pred_outputs6, true_labels
    run_pkt_count += 1

    pred_outputs1.append(pkt[FeatureHeader].output1)
    pred_outputs2.append(pkt[FeatureHeader].output2)
    pred_outputs3.append(pkt[FeatureHeader].output3)
    pred_outputs4.append(pkt[FeatureHeader].output4)


    true_labels.append(pkt[FeatureHeader].label)

    # code to check output every packet
    if run_pkt_count % 1 == 0: 
        print("Switch 1 metrics: ")
        accuracy1, precision1, recall1, f11 = calc_metrics(pred_outputs1, true_labels)
        print("Switch 2 metrics: ")
        accuracy2, precision2, recall2, f12 = calc_metrics(pred_outputs2, true_labels)
        print("Switch 3 metrics: ")
        accuracy3, precision3, recall3, f13 = calc_metrics(pred_outputs3, true_labels)
        print("Switch 3 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs4, true_labels)

        print("FPR for baseline (measured in switch1): ")
        calc_fp_fn(pred_outputs1, true_labels)
        print("FPR for baseline (measured in switch2): ")
        calc_fp_fn(pred_outputs2, true_labels)
        print("FPR for baseline (measured in switch3): ")
        calc_fp_fn(pred_outputs3, true_labels)

        print("FPR for our mechanism (measured in switch3): ")
        calc_fp_fn(pred_outputs4, true_labels)

        weights = [pkt[FeatureHeader].weight1 << 8 | pkt[FeatureHeader].weight1_2,
                   pkt[FeatureHeader].weight2 << 8 | pkt[FeatureHeader].weight2_2,
                   pkt[FeatureHeader].weight3 << 8 | pkt[FeatureHeader].weight3_2]

        incorrect_count = calc_inc_count([pkt[FeatureHeader].output1, 
                                          pkt[FeatureHeader].output2, pkt[FeatureHeader].output3], 
                                          pkt[FeatureHeader].output4)
        
        final_decision = compute_majority_voting_results([pkt[FeatureHeader].output1, 
                                          pkt[FeatureHeader].output2, pkt[FeatureHeader].output3],
                                          weights)
        
        if(final_decision != pkt[FeatureHeader].output4):
            print("Prediction result error final decision with python: {} and receved decision: {}").format(
                final_decision, pkt[FeatureHeader].output4)

        print("Computed at recv: {} packets have made the incorrect prediction ".format(incorrect_count))
        if(pkt[FeatureHeader].output1 != pkt[FeatureHeader].output4):
            print("Incorrect Switch 1")     
        if(pkt[FeatureHeader].output2 != pkt[FeatureHeader].output4):
            print("Incorrect Switch 2")     
        if(pkt[FeatureHeader].output3 != pkt[FeatureHeader].output4):
            print("Incorrect Switch 3")     

        
        prev_incorrect_count = incorrect_count
        print("Switch1 weight: {}".format(weights[0]))
        print("Switch2 weight: {}".format(weights[1]))
        print("Switch3 weight: {}".format(weights[2]))


    # Calculate metrics for every max_count packets
    if run_pkt_count == MAX_PKT_COUNT:

        batch_count += 1
        print("Received {0} packets.".format(MAX_PKT_COUNT))

        print("Switch 1 metrics: ")
        accuracy1, precision1, recall1, f11 = calc_metrics(pred_outputs1, true_labels)
        print("Switch 2 metrics: ")
        accuracy2, precision2, recall2, f12 = calc_metrics(pred_outputs2, true_labels)
        print("Switch 3 metrics: ")
        accuracy3, precision3, recall3, f13 = calc_metrics(pred_outputs3, true_labels)
        print("Switch 3 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs4, true_labels)

        print("FPR for baseline (measured in switch1): ")
        calc_fp_fn(pred_outputs1, true_labels)
        print("FPR for baseline (measured in switch2): ")
        calc_fp_fn(pred_outputs2, true_labels)
        print("FPR for baseline (measured in switch3): ")
        calc_fp_fn(pred_outputs3, true_labels)

        print("FPR for our mechanism (measured in switch3): ")
        calc_fp_fn(pred_outputs6, true_labels)

        run_pkt_count = 0
        pred_outputs1 = list()
        pred_outputs2 = list()
        pred_outputs3 = list()
        pred_outputs4 = list()
        pred_outputs5 = list()
        pred_outputs6 = list()
        true_labels = list()


def parse_output_five_hops(pkt):
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

    if run_pkt_count % 1 == 0: # look at the output per batch
        print("\nReceived {} packets.".format(run_pkt_count))        
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
        
        print("FPR for our mechanism (measured in switch3): ")
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

        
        prev_incorrect_count = incorrect_count
        print("Switch1 weight: {}".format(weights[0]))
        print("Switch2 weight: {}".format(weights[1]))
        print("Switch3 weight: {}".format(weights[2]))
        print("Switch4 weight: {}".format(weights[3]))
        print("Switch5 weight: {}".format(weights[4]))
        print("Prediction of 5 switches : {}, final prediction is: {}".format(
            [pkt[FeatureHeader].output1, pkt[FeatureHeader].output2, pkt[FeatureHeader].output3,
             pkt[FeatureHeader].output4, pkt[FeatureHeader].output5], pkt[FeatureHeader].output6))
    
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
    
    # Calculate metrics for the end metrics packets
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


        print(pred_outputs6)

        run_pkt_count = 0
        pred_outputs1 = list()
        pred_outputs2 = list()
        pred_outputs3 = list()
        pred_outputs4 = list()
        pred_outputs5 = list()
        pred_outputs6 = list()
        true_labels = list()

def parse_output_seven_hops(pkt):
    global  batch_count, run_pkt_count, pred_outputs1, pred_outputs2, pred_outputs3,\
        pred_outputs4, pred_outputs5, pred_outputs6, pred_outputs7, \
        pred_outputs8, true_labels



    run_pkt_count += 1

    pred_outputs1.append(pkt[FeatureHeader].output1)
    pred_outputs2.append(pkt[FeatureHeader].output2)
    pred_outputs3.append(pkt[FeatureHeader].output3)
    pred_outputs4.append(pkt[FeatureHeader].output4)
    pred_outputs5.append(pkt[FeatureHeader].output5)
    pred_outputs6.append(pkt[FeatureHeader].output6)
    pred_outputs7.append(pkt[FeatureHeader].output7)
    pred_outputs8.append(pkt[FeatureHeader].output8)
    pred_outputs9.append(pkt[FeatureHeader].output9)
    pred_outputs10.append(pkt[FeatureHeader].output10)


    true_labels.append(pkt[FeatureHeader].label)

    if run_pkt_count % (MAX_PKT_COUNT/10) == 0:
        print("Received 10% packets")

    # Calculate metrics for every X packets
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
        print("Switch 6 metrics: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs6, true_labels)
        print("Switch 7 metrics: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs7, true_labels)
        print("Switch 7 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs8, true_labels)

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
        print("FPR for baseline (measured in switch6): ")
        calc_fp_fn(pred_outputs6, true_labels)
        print("FPR for baseline (measured in switch7): ")
        calc_fp_fn(pred_outputs7, true_labels)
        print("FPR for our mechanism (measured in switch7): ")
        calc_fp_fn(pred_outputs8, true_labels)

 
        run_pkt_count = 0
        pred_outputs1 = list()
        pred_outputs2 = list()
        pred_outputs3 = list()
        pred_outputs4 = list()
        pred_outputs5 = list()
        pred_outputs6 = list()
        pred_outputs7 = list()  
        pred_outputs8 = list()
        true_labels = list()


def parse_output_nine_hops(pkt):
    global  batch_count, run_pkt_count, pred_outputs1, pred_outputs2, pred_outputs3,\
        pred_outputs4, pred_outputs5, pred_outputs6, pred_outputs7, \
        pred_outputs8, pred_outputs9, pred_outputs10, true_labels



    run_pkt_count += 1

    pred_outputs1.append(pkt[FeatureHeader].output1)
    pred_outputs2.append(pkt[FeatureHeader].output2)
    pred_outputs3.append(pkt[FeatureHeader].output3)
    pred_outputs4.append(pkt[FeatureHeader].output4)
    pred_outputs5.append(pkt[FeatureHeader].output5)
    pred_outputs6.append(pkt[FeatureHeader].output6)
    pred_outputs7.append(pkt[FeatureHeader].output7)
    pred_outputs8.append(pkt[FeatureHeader].output8)
    pred_outputs9.append(pkt[FeatureHeader].output9)
    pred_outputs10.append(pkt[FeatureHeader].output10)


    true_labels.append(pkt[FeatureHeader].label)

    if run_pkt_count % 1 == 0: # look at the output per batch
        print("\nReceived {} packets.".format(run_pkt_count))        
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
        print("Switch 6 metrics: ")
        accuracy4, precision4, recall4, f14 = calc_metrics(pred_outputs6, true_labels)
        print("Switch 7 metrics: ")
        accuracy5, precision5, recall5, f15 = calc_metrics(pred_outputs7, true_labels)
        print("Switch 8 metrics: ")
        accuracy4, precision4, recall4, f14 = calc_metrics(pred_outputs8, true_labels)
        print("Switch 9 metrics: ")
        accuracy5, precision5, recall5, f15 = calc_metrics(pred_outputs9, true_labels)
        print("Switch 9 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs10, true_labels)

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
        print("FPR for baseline (measured in switch6): ")
        calc_fp_fn(pred_outputs6, true_labels)
        print("FPR for baseline (measured in switch7): ")
        calc_fp_fn(pred_outputs7, true_labels)
        print("FPR for baseline (measured in switch8): ")
        calc_fp_fn(pred_outputs8, true_labels)
        print("FPR for baseline (measured in switch9): ")
        calc_fp_fn(pred_outputs9, true_labels)
        print("FPR for our mechanism (measured in switch9): ")
        calc_fp_fn(pred_outputs10, true_labels)
        weights = [pkt[FeatureHeader].weight1 << 8 | pkt[FeatureHeader].weight1_2,
                   pkt[FeatureHeader].weight2 << 8 | pkt[FeatureHeader].weight2_2,
                   pkt[FeatureHeader].weight3 << 8 | pkt[FeatureHeader].weight3_2,
                   pkt[FeatureHeader].weight4 << 8 | pkt[FeatureHeader].weight4_2,
                   pkt[FeatureHeader].weight5 << 8 | pkt[FeatureHeader].weight5_2,
                   pkt[FeatureHeader].weight6 << 8 | pkt[FeatureHeader].weight6_2,
                   pkt[FeatureHeader].weight7 << 8 | pkt[FeatureHeader].weight7_2,
                   pkt[FeatureHeader].weight8 << 8 | pkt[FeatureHeader].weight8_2,
                   pkt[FeatureHeader].weight9 << 8 | pkt[FeatureHeader].weight9_2
                   ]
        
        incorrect_count = calc_inc_count([pkt[FeatureHeader].output1, 
                                          pkt[FeatureHeader].output2, pkt[FeatureHeader].output3,
                                          pkt[FeatureHeader].output4, pkt[FeatureHeader].output5,
                                          pkt[FeatureHeader].output6, pkt[FeatureHeader].output7,
                                          pkt[FeatureHeader].output8, pkt[FeatureHeader].output9,
                                          ], 
                                          pkt[FeatureHeader].output10)
        
        final_decision = compute_majority_voting_results([pkt[FeatureHeader].output1, 
                                          pkt[FeatureHeader].output2, pkt[FeatureHeader].output3,
                                          pkt[FeatureHeader].output4, pkt[FeatureHeader].output5,
                                          pkt[FeatureHeader].output6, pkt[FeatureHeader].output7,
                                          pkt[FeatureHeader].output8, pkt[FeatureHeader].output9],
                                          weights)
        
        if(final_decision != pkt[FeatureHeader].output10):
            print("Prediction result error final decision with python: {} and receved decision: {}").format(
                final_decision, pkt[FeatureHeader].output10)

        
        prev_incorrect_count = incorrect_count
        print("Switch1 weight: {}".format(weights[0]))
        print("Switch2 weight: {}".format(weights[1]))
        print("Switch3 weight: {}".format(weights[2]))
        print("Switch4 weight: {}".format(weights[3]))
        print("Switch5 weight: {}".format(weights[4]))
        print("Switch6 weight: {}".format(weights[5]))
        print("Switch7 weight: {}".format(weights[6]))
        print("Switch8 weight: {}".format(weights[7]))
        print("Switch9 weight: {}".format(weights[8]))
        print("Prediction of 9 switches : {}, final prediction is: {}".format(
            [pkt[FeatureHeader].output1, pkt[FeatureHeader].output2, pkt[FeatureHeader].output3,
             pkt[FeatureHeader].output4, pkt[FeatureHeader].output5, pkt[FeatureHeader].output6, 
             pkt[FeatureHeader].output7, pkt[FeatureHeader].output8, pkt[FeatureHeader].output9], 
             pkt[FeatureHeader].output10))
    

        print("Computed at recv: {} packets have made the incorrect prediction ".format(incorrect_count))
        if(pkt[FeatureHeader].output1 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 1")     
        if(pkt[FeatureHeader].output2 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 2")     
        if(pkt[FeatureHeader].output3 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 3")     
        if(pkt[FeatureHeader].output4 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 4")     
        if(pkt[FeatureHeader].output5 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 5")  
        if(pkt[FeatureHeader].output6 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 6")     
        if(pkt[FeatureHeader].output7 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 7")     
        if(pkt[FeatureHeader].output8 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 8")     
        if(pkt[FeatureHeader].output9 != pkt[FeatureHeader].output10):
            print("Incorrect Switch 9")     

    # Calculate metrics for every X packets
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
        print("Switch 6 metrics: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs6, true_labels)
        print("Switch 7 metrics: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs7, true_labels)
        print("Switch 8 metrics: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs8, true_labels)
        print("Switch 9 metrics: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs9, true_labels)
        print("Switch 9 metrics aggregating decisions of other switches: ")
        accuracy6, precision6, recall6, f16 = calc_metrics(pred_outputs10, true_labels)

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
        print("FPR for baseline (measured in switch6): ")
        calc_fp_fn(pred_outputs6, true_labels)
        print("FPR for baseline (measured in switch7): ")
        calc_fp_fn(pred_outputs7, true_labels)
        print("FPR for baseline (measured in switch8): ")
        calc_fp_fn(pred_outputs8, true_labels)
        print("FPR for baseline (measured in switch9): ")
        calc_fp_fn(pred_outputs9, true_labels)
        print("FPR for our mechanism (measured in switch9): ")
        calc_fp_fn(pred_outputs10, true_labels)
 
        run_pkt_count = 0
        pred_outputs1 = list()
        pred_outputs2 = list()
        pred_outputs3 = list()
        pred_outputs4 = list()
        pred_outputs5 = list()
        pred_outputs6 = list()
        pred_outputs7 = list()
        pred_outputs8 = list()
        pred_outputs9 = list()
        pred_outputs10 = list()
        true_labels = list()




if __name__ == "__main__":
    

    parse_args()
    print("Selected host: {}".format(args.host))


    if(args.num_hops == 9):
        from helperRecvNineSwitches import *
        print("Feautre headers contain the following information: ")
        for field in FeatureHeader.fields_desc:
            print(field.name)
        while True:
            sniff(iface="{}-eth0".format(args.host), prn=lambda x: parse_output_nine_hops(x), count=MAX_PKT_COUNT,
            lfilter=lambda x: (IP in x) and (x[IP].proto == 253))
    if(args.num_hops == 7):
        from helperRecvSevenSwitches import *
        print("Feautre headers contain the following information: ")
        for field in FeatureHeader.fields_desc:
            print(field.name)
        while True:
            sniff(iface="{}-eth0".format(args.host), prn=lambda x: parse_output_seven_hops(x), count=MAX_PKT_COUNT,
            lfilter=lambda x: (IP in x) and (x[IP].proto == 253))
    elif(args.num_hops == 5):
        from helperRecvFiveSwitches import *
        print("Feautre headers contain the following information: ")
        for field in FeatureHeader.fields_desc:
            print(field.name)
        while True:
            sniff(iface="{}-eth0".format(args.host), prn=lambda x: parse_output_five_hops(x), count=MAX_PKT_COUNT,
            lfilter=lambda x: (IP in x) and (x[IP].proto == 253))
    elif(args.num_hops == 3):
        from helperRecvThreeSwitches import *
        print("Feautre headers contain the following information: ")
        for field in FeatureHeader.fields_desc:
            print(field.name)
        while True:
            print("Listening on {}-eth0".format(args.host))
            sniff(iface="{}-eth0".format(args.host), prn=lambda x: parse_output_three_hops(x), count=MAX_PKT_COUNT,
            lfilter=lambda x: (IP in x) and (x[IP].proto == 253))
            
