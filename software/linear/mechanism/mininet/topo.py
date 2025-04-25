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

import argparse
import json
import sys

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import Intf, Link
from stratum import StratumBmv2Switch


class SingleSwitchTopo(Topo):
    """Single Switch topology"""

    def __init__(self, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)

        self.addSwitch('s1') # grpc: 50001
        self.addSwitch('s2') # grpc: 50002
        self.addSwitch('s3') # grpc: 50003
        self.addSwitch('s4') # grpc: 50004
        self.addSwitch('s5') # grpc: 50005

        self.addHost('h1', ip="10.0.0.1", mac="00:00:00:00:00:01")
        self.addHost('h2', ip="10.0.0.2", mac="00:00:00:00:00:02")

        self.addLink('h1', 's1')
        self.addLink('s1', 's2')
        self.addLink('s2', 's3')
        self.addLink('s3', 's4')
        self.addLink('s4', 's5')
        self.addLink('s5', 'h2')


topos = {'singleswitch': (lambda: SingleSwitchTopo())}


def main(num_switches, ingress_intf=None, egress_intf=None):

    net = Mininet(
        topo=SingleSwitchTopo(),
        switch=StratumBmv2Switch,
        controller=None)

    # s1 = net.get('s1')
    # s2 = net.get('s2')
    # i = 1

    for i in range(len(num_switches)):
    # Add external interfaces
        print(i+1)
        switch = net.get('s'+str(i+1)) 

        # ingress interface setup for switch i
        Intf(ingress_intfs[i], node=switch, port=3)
        # egress interface setup for switch i
        Intf(egress_intfs[i], node=switch, port=4)

    # if ingress_intf:
    #     Intf(ingress_intf, node=s1, port=3)
    # # if ingress_intf_1:
    # #     Intf(ingress_intf_1, node=s2, port=3)

    # if ingress_intf:
    #     Intf(egress_intf, node=s1, port=4)
    # if ingress_intf_1:
    #     Intf(egress_intf_1, node=s2, port=4)
    # import pdb
    # pdb.set_trace()
    net.start()
    CLI(net)
    net.stop()

# returns a list of the names of ingress interface
def ingress_interface_names_gen(num_switches):
    ingress_names = []
    for i in range(1,num_switches+1):
        ingress_names.append("vs"+str(i))
    return ingress_names

# returns a list of the names of ingress interface
def egress_inferfaces_names_gen(num_switches):
    egress_names = []
    for i in range(1,num_switches+1):
        egress_names.append("s"+str(i)+"v")
    return egress_names

if __name__ == "__main__":
    setLogLevel('info')
    parser = argparse.ArgumentParser(
        description='Mininet script (single switch topology)')

    parser.add_argument('--num-switches', type=str, action="store", required=True)
    # parser.add_argument('--ingress-intf', type=str, action="store", required=True)
    # parser.add_argument('--egress-intf', type=str, action="store", required=True)
    # parser.add_argument('--ingress-intf_1', type=str, action="store", required=True)
    # parser.add_argument('--egress-intf_1', type=str, action="store", required=True)
    args = parser.parse_args()

    ingress_intfs = ingress_interface_names_gen(num_switches = int(args.num_switches))
    egress_intfs = egress_inferfaces_names_gen(num_switches = int(args.num_switches))

    if(len(ingress_intfs) != len(egress_intfs)): 
        print("ERROR: the number of interfaces for ingress and egress does not match!!!")
        sys.exit(-1)

    main(ingress_intfs, egress_intfs, args.num_switches)