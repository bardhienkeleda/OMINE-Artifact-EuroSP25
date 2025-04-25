
import argparse
import json
import sys

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import Intf, Link
from stratum import StratumBmv2Switch

NUM_SWITCHES = 24 

# The datacenter tree topology shown in the paper

class DatacenterSwitchTopo(Topo):
    """Data center switch topology"""

    

    def __init__(self, *args, **kwargs):

        Topo.__init__(self, *args, **kwargs)


        self.addSwitch('s1') # grpc: 50001
        self.addSwitch('s2') # grpc: 50002
        self.addSwitch('s3') # grpc: 50003
        self.addSwitch('s4') # grpc: 50004
        self.addSwitch('s5') # grpc: 50005 
        self.addSwitch('s6') # grpc: 50006
        self.addSwitch('s7') # grpc: 50007
        self.addSwitch('s8') # grpc: 50008
        self.addSwitch('s9') # grpc: 50009
        self.addSwitch('s10')# grpc: 50010
        self.addSwitch('s11')# grpc: 50011
        self.addSwitch('s12')# grpc: 50012
        self.addSwitch('s13')# grpc: 50013
        self.addSwitch('s14')# grpc: 50014
        self.addSwitch('s15')# grpc: 50015
        self.addSwitch('s16')# grpc: 50016
        self.addSwitch('s17')# grpc: 50017
        self.addSwitch('s18')# grpc: 50018
        self.addSwitch('s19')# grpc: 50019
        self.addSwitch('s20')# grpc: 50020
        self.addSwitch('s21')# grpc: 50021
        self.addSwitch('s22')# grpc: 50022
        self.addSwitch('s23')# grpc: 50023
        self.addSwitch('s24')# grpc: 50024




        # print("Adding hosts")
        self.addHost('h1', ip="10.0.0.1", mac="00:00:00:00:00:01") # connects to s17
        self.addHost('h2', ip="10.0.0.2", mac="00:00:00:00:00:02") # connects to s18
        self.addHost('h3', ip="10.0.0.3", mac="00:00:00:00:00:03") # connects to s19
        self.addHost('h4', ip="10.0.0.4", mac="00:00:00:00:00:04") # connects to s20
        self.addHost('h5', ip="10.0.0.5", mac="00:00:00:00:00:05") # connects to s21
        self.addHost('h6', ip="10.0.0.6", mac="00:00:00:00:00:06") # connects to s22
        self.addHost('h7', ip="10.0.0.7", mac="00:00:00:00:00:07") # connects to s23
        self.addHost('h8', ip="10.0.0.8", mac="00:00:00:00:00:08") # connects to s24



        self.addLink('h1', 's17')
        self.addLink('h2', 's18')
        self.addLink('h3', 's19')
        self.addLink('h4', 's20')
        self.addLink('h5', 's21')
        self.addLink('h6', 's22')
        self.addLink('h7', 's23')
        self.addLink('h8', 's24')
        

        # layer 1
        self.addLink('s1', 's3')
        self.addLink('s1', 's4')
        self.addLink('s2', 's3')
        self.addLink('s2', 's4')

        # layer 2
        self.addLink('s3', 's5')
        self.addLink('s3', 's6')
        self.addLink('s3', 's7')
        self.addLink('s3', 's8')
        self.addLink('s4', 's5')
        self.addLink('s4', 's6')
        self.addLink('s4', 's7')
        self.addLink('s4', 's8')

        # layer 3
        self.addLink('s5', 's9')
        self.addLink('s5', 's10')
        self.addLink('s5', 's11')
        self.addLink('s5', 's12')
        self.addLink('s6', 's9')
        self.addLink('s6', 's10')
        self.addLink('s6', 's11')
        self.addLink('s6', 's12')
        self.addLink('s7', 's13')
        self.addLink('s7', 's14')
        self.addLink('s7', 's15')
        self.addLink('s7', 's16')
        self.addLink('s8', 's13')
        self.addLink('s8', 's14')
        self.addLink('s8', 's15')
        self.addLink('s8', 's16')
                        
        # layer 4
        self.addLink('s9', 's17')
        self.addLink('s9', 's18')        
        self.addLink('s10', 's17')
        self.addLink('s10', 's18')     
        self.addLink('s11', 's19')
        self.addLink('s11', 's20')
        self.addLink('s12', 's19')
        self.addLink('s12', 's20')
        self.addLink('s13', 's21')
        self.addLink('s13', 's22')     
        self.addLink('s14', 's21')
        self.addLink('s14', 's22')     
        self.addLink('s15', 's23')
        self.addLink('s15', 's24')     
        self.addLink('s16', 's23')
        self.addLink('s16', 's24')     
        
        # layer 5 already connected
        
topos = {'dctree': (lambda: DatacenterSwitchTopo())}


def main(num_switches, ingress_intf=None, egress_intf=None):
    net = Mininet(
        topo = DatacenterSwitchTopo(),
        switch = StratumBmv2Switch,
        controller = None
    )

    # interfaces
    interfaces = {
        's1': {
            'ingress': 3,
            'egress' : 4,
        },
        's2': {
            'ingress': 3,
            'egress' : 4,
        },
        's3': {
            'ingress': 7,
            'egress' : 8,
        },
        's4': {
            'ingress': 7,
            'egress' : 8,
        },
        's5': {
            'ingress': 7,
            'egress' : 8,
        },
        's6': {
            'ingress': 7,
            'egress' : 8,
        },
        's7': {
            'ingress': 7,
            'egress' : 8,
        },
        's8': {
            'ingress': 7,
            'egress' : 8,
        },
        's9': {
            'ingress': 5,
            'egress' : 6,
        },
        's10': {
            'ingress': 5,
            'egress' : 6,
        },
        's11': {
            'ingress': 5,
            'egress' : 6,
        },        
        's12': {
            'ingress': 5,
            'egress' : 6,
        },
        's13': {
            'ingress': 5,
            'egress' : 6,
        },
        's14': {
            'ingress': 5,
            'egress' : 6,
        },
        's15': {
            'ingress': 5,
            'egress' : 6,
        },
        's16': {
            'ingress': 5,
            'egress' : 6,
        },
        's17': {
            'ingress': 4,
            'egress' : 5,
        },
        's18': {
            'ingress': 4,
            'egress' : 5,
        },        
        's19': {
            'ingress': 4,
            'egress' : 5,
        },      
        's20': {
            'ingress': 4,
            'egress' : 5,
        },
        's21': {
            'ingress': 4,
            'egress' : 5,
        },
        's22': {
            'ingress': 4,
            'egress' : 5,
        },
        's23': {
            'ingress': 4,
            'egress' : 5,
        },
        's24': {
            'ingress': 4,
            'egress' : 5,
        }
    }



    for i in range(0,num_switches):
        # Add external interfaces
        sname = 's'+str(i+1)
        switch = net.get(sname) 

        # ingress interface setup for switch i
        Intf(ingress_intfs[i], node=switch, port=interfaces[sname]['ingress'])
        # egress interface setup for switch i
        Intf(egress_intfs[i], node=switch, port=interfaces[sname]['egress'])

    net.start()
    CLI(net)
    net.stop()

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
    num_switches = NUM_SWITCHES 
    ingress_intfs = ingress_interface_names_gen(num_switches = int(num_switches))
    egress_intfs = egress_inferfaces_names_gen(num_switches = int(num_switches))

    if(len(ingress_intfs) != len(egress_intfs)): 
        print("ERROR: the number of interfaces for ingress and egress does not match!!!")
        sys.exit(-1)
    
    main(num_switches,ingress_intfs, egress_intfs)