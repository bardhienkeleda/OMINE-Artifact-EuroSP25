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

import signal
signal.signal(signal.SIGINT, lambda signum, frame: exit(1))

from scapy.all import *
from helper import *

MAX_PKT_COUNT = 5000

# Parse and process incoming packets
run_pkt_count = 0
pred_outputs = list()
true_labels = list()

def parse_output(pkt):
    global run_pkt_count, pred_outputs, true_labels

    run_pkt_count += 1

    pred_outputs.append(pkt[FeatureHeader].output)
    true_labels.append(pkt[FeatureHeader].label)

    if run_pkt_count % 100 == 0:
        print("Received {0} packets.".format(run_pkt_count))

        calc_metrics(pred_outputs, true_labels)
        calc_fp_fn(pred_outputs, true_labels)

    # Calculate metrics for every 60 packets
    if run_pkt_count == MAX_PKT_COUNT:
        print("Received {0} packets.".format(MAX_PKT_COUNT))

        calc_metrics(pred_outputs, true_labels)
        #print("FPR for baseline (measured in switch1): ")
        calc_fp_fn(pred_outputs, true_labels)
        
        run_pkt_count = 0
        pred_outputs = list()
        true_labels = list()

# Sniff packets with feature headers
while True:
    sniff(iface='h2-eth0', prn=lambda x:parse_output(x), count=MAX_PKT_COUNT, 
          lfilter=lambda x: (IP in x) and (x[IP].proto == 253))
