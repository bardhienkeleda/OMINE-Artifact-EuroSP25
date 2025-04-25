#!/usr/bin/env python3

# *************************************************************************
# 
#  Copyright 2025 Enkeleda Bardhi (TU Delft),
#                 Chenxing Ji (TU Delft),
#                 Ali Imran (Purdue University),
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
import argparse
from collections import defaultdict

from utils.rest import install_rule, delete_rule

# h1->s17->s10->s6->s12->s20->h4
def install_rules_5_1():
    
    install_rule(dev_id="device:s17",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=5)
    install_rule(dev_id="device:s17",  table="forward", is_permanent=True, priority=40, ingress_port=4, output=3)
    install_rule(dev_id="device:s17",  table="forward", is_permanent=True, priority=40, ingress_port=3, output=1)

    install_rule(dev_id="device:s10",  table="forward", is_permanent=True, priority=40, ingress_port=3, output=6)
    install_rule(dev_id="device:s10",  table="forward", is_permanent=True, priority=40, ingress_port=5, output=2)  
    install_rule(dev_id="device:s10",  table="forward", is_permanent=True, priority=40, ingress_port=2, output=3)  

    install_rule(dev_id="device:s6",  table="forward", is_permanent=True, priority=40, ingress_port=4, output=8)
    install_rule(dev_id="device:s6",  table="forward", is_permanent=True, priority=40, ingress_port=7, output=6)  
    install_rule(dev_id="device:s6",  table="forward", is_permanent=True, priority=40, ingress_port=6, output=4)  

    install_rule(dev_id="device:s12",  table="forward", is_permanent=True, priority=40, ingress_port=2, output=6)
    install_rule(dev_id="device:s12",  table="forward", is_permanent=True, priority=40, ingress_port=5, output=4)  
    install_rule(dev_id="device:s12",  table="forward", is_permanent=True, priority=40, ingress_port=4, output=2)  

    install_rule(dev_id="device:s20", table="forward", is_permanent=True, priority=40, ingress_port=3, output=5)
    install_rule(dev_id="device:s20", table="forward", is_permanent=True, priority=40, ingress_port=4, output=1)

# h1->s17->s9->s5->s3->s1->s4->s6->s12->s20->h4
def install_rules_9_1():
    
    install_rule(dev_id="device:s17",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=5)
    install_rule(dev_id="device:s17",  table="forward", is_permanent=True, priority=40, ingress_port=4, output=2)
    install_rule(dev_id="device:s17",  table="forward", is_permanent=True, priority=40, ingress_port=2, output=1)

    install_rule(dev_id="device:s9",  table="forward", is_permanent=True, priority=40, ingress_port=3, output=6)
    install_rule(dev_id="device:s9",  table="forward", is_permanent=True, priority=40, ingress_port=5, output=1)  
    install_rule(dev_id="device:s9",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=3)  

    install_rule(dev_id="device:s5",  table="forward", is_permanent=True, priority=40, ingress_port=3, output=8)
    install_rule(dev_id="device:s5",  table="forward", is_permanent=True, priority=40, ingress_port=7, output=1)  
    install_rule(dev_id="device:s5",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=3)  

    install_rule(dev_id="device:s3",  table="forward", is_permanent=True, priority=40, ingress_port=3, output=8)
    install_rule(dev_id="device:s3",  table="forward", is_permanent=True, priority=40, ingress_port=7, output=1)  
    install_rule(dev_id="device:s3",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=3)  

    install_rule(dev_id="device:s1",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=4)
    install_rule(dev_id="device:s1",  table="forward", is_permanent=True, priority=40, ingress_port=3, output=2)  
    install_rule(dev_id="device:s1",  table="forward", is_permanent=True, priority=40, ingress_port=2, output=1)  
    
    install_rule(dev_id="device:s4",  table="forward", is_permanent=True, priority=40, ingress_port=1, output=8)
    install_rule(dev_id="device:s4",  table="forward", is_permanent=True, priority=40, ingress_port=7, output=4)  
    install_rule(dev_id="device:s4",  table="forward", is_permanent=True, priority=40, ingress_port=4, output=1)  
    
    install_rule(dev_id="device:s6",  table="forward", is_permanent=True, priority=40, ingress_port=2, output=8)
    install_rule(dev_id="device:s6",  table="forward", is_permanent=True, priority=40, ingress_port=7, output=6)  
    install_rule(dev_id="device:s6",  table="forward", is_permanent=True, priority=40, ingress_port=6, output=2)  

    install_rule(dev_id="device:s12",  table="forward", is_permanent=True, priority=40, ingress_port=2, output=6)
    install_rule(dev_id="device:s12",  table="forward", is_permanent=True, priority=40, ingress_port=5, output=4)  
    install_rule(dev_id="device:s12",  table="forward", is_permanent=True, priority=40, ingress_port=4, output=2)  

    install_rule(dev_id="device:s20", table="forward", is_permanent=True, priority=40, ingress_port=2, output=5)
    install_rule(dev_id="device:s20", table="forward", is_permanent=True, priority=40, ingress_port=4, output=1)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Mininet (Linear 5-Switch Topology)')
    # parser.add_argument('--enable', action="store_true")
    parser.add_argument('--disable', action="store_true", default = False)
    parser.add_argument("--num-switches", type=int, default=7, help="Number of switches")
    parser.add_argument("--path", type=int, default=4, help="choosing path 1 or 2")
    args = parser.parse_args()

    print("Installing rules for", args.num_switches, "switches via path", args.path)


    if(args.num_switches == 5 and args.path == 1):
        install_rules_5_1()
    elif(args.num_switches == 9 and args.path == 1):
        install_rules_9_1()    
    else:
        print("Unsupported combinations of num_hops={}, path={}".format(
            args.num_switches, args.path))
