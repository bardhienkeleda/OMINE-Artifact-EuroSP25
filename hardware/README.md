# O'MINE FPGA Testbed

This part of the source code contains the scripts and instructions for setting up the correct testbed environment for the O'MINE evaluation. As shown in `platform/testbed.png` file, the testbed relies on [Taurus Platform ASPLOS22](https://gitlab.com/dataplane-ai/taurus/applications/anomaly-detection-asplos22). 

> **Note:** we assume the user has access to the following hardware and tools to run O'MINE architecture:
> - FPGA Xilinx Alevo U250 
> - Programmable Tofino Wedge 100BF-32X switch
> - ONOS: Open Network Operating Systems and MoonGen Traffic Generator

## Content
- `spatial/`: contains the spatial code to compile the FPGA bitstream for both CICIDS-2017 and UNSW-NB15 datasets
- `sendrecv/`: contains the code for the packet sender and receiver for traffic generation
