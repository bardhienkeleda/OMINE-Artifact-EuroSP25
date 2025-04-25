
import argparse
import json
import sys

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import Intf, Link
from stratum import StratumBmv2Switch

# The topology used for collecting the experiment results

class ExperimentTopo(Topo):
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


        self.addHost('h1', ip="10.0.0.1", mac="00:00:00:00:00:01") # connects to s17
        self.addHost('h2', ip="10.0.0.2", mac="00:00:00:00:00:02") # connects to s18
        self.addHost('h3', ip="10.0.0.3", mac="00:00:00:00:00:03") # connects to s19
        self.addHost('h4', ip="10.0.0.4", mac="00:00:00:00:00:04") # connects to s20


        self.addLink('h1', 's11')
        self.addLink('h2', 's12')
        self.addLink('h3', 's13')
        self.addLink('h4', 's14')

        # layer 1
        self.addLink('s1', 's3')
        self.addLink('s1', 's4')
        self.addLink('s2', 's3')
        self.addLink('s2', 's4')

        # layer 2
        self.addLink('s3', 's5')
        self.addLink('s3', 's6')
        self.addLink('s4', 's5')
        self.addLink('s4', 's6')

        # layer 3
        self.addLink('s5', 's7')
        self.addLink('s5', 's8')
        self.addLink('s5', 's9')
        self.addLink('s5', 's10')
        self.addLink('s6', 's7')
        self.addLink('s6', 's8')
        self.addLink('s6', 's9')
        self.addLink('s6', 's10')
                        
        # layer 4
        self.addLink('s7', 's11')
        self.addLink('s7', 's12')
        self.addLink('s8', 's11')
        self.addLink('s8', 's12') 
            
        self.addLink('s9', 's13')
        self.addLink('s9', 's14')
        self.addLink('s10', 's13')
        self.addLink('s10', 's14')
 

topos = {'exp': (lambda: ExperimentTopo())}


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



def main(ingress_intf=None, egress_intf=None):
    net = Mininet(
        topo = ExperimentTopo(),
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
            'ingress': 5,
            'egress' : 6,
        },
        's4': {
            'ingress': 5,
            'egress' : 6,
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
            'ingress': 5,
            'egress' : 6,
        },
        's8': {
            'ingress': 5,
            'egress' : 6,
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
            'ingress': 4,
            'egress' : 5,
        },        
        's12': {
            'ingress': 4,
            'egress' : 5,
        },
        's13': {
            'ingress': 4,
            'egress' : 5,
        },
        's14': {
            'ingress': 4,
            'egress' : 5,
        }
    }
    num_switches = len(interfaces)+1

    ingress_intfs = ingress_interface_names_gen(num_switches = int(num_switches))
    egress_intfs = egress_inferfaces_names_gen(num_switches = int(num_switches))
    print(ingress_intfs)
    print(egress_intfs)
    
    if(len(ingress_intfs) != len(egress_intfs)): 
        print("ERROR: the number of interfaces for ingress and egress does not match!!!")
        sys.exit(-1)
        

    switch_names = list(interfaces.keys())
    print("Number of Switches: " + str(len(interfaces)+1))
    for i in range(0,len(interfaces)):
        # Add external interfaces

        sname = "s"+str(i+1)
        switch = net.get(sname) 
        print("Adding interfaces for " + sname)
        # ingress interface setup for switch i
        Intf(ingress_intfs[i], node=switch, port=interfaces[sname]['ingress'])
        # egress interface setup for switch i
        Intf(egress_intfs[i], node=switch, port=interfaces[sname]['egress'])

    net.start()
    CLI(net)
    net.stop()



if __name__ == "__main__":
    setLogLevel('info')
    
    main()