# Software Tree topology with O'MINE

This directory implements the tree topology used in our paper, as shown in the figure below. In this directory, we provide the code to construct a tree topology of 5 layers. For the experiments discussed in the paper, we used a 14-node subtree extracted from the provided topology. This subtree preserves the same path structure and is used to evaluate the flexibility and scalability of the proposed O'MINE architecture, using the code provided in this folder.

![Tree Topology](mechanism/figures/tree_topology.jpg)


## Download and start MapReduce BM dockers

Since O'MINE Machine learning module depends on the [Taurus Platform BM](https://gitlab.com/dataplane-ai/taurus/platform-bm/-/tree/main), you need to first download and start the MapReduce BM Docker containers. If the containers haven’t been downloaded before, the following command will initiate the download.
The following command starts the same number of MapReduce BM docker instances as Figure 10 in O'MINE has presented. The command utilizes the `mechanism/scripts/mapreduce-bm-n-switches` script.
```sh
make mapreduce-start-treetopo
```

> **Notes:** 
> - As Docker is running these containers for the first time, it will need to download them from https://hub.docker.com. These are large images (hundreds of megabytes), so they may take some time to download depending upon the network speed -- don't worry if the process is slow. It will happen only once, as Docker will cache these images and reuse them whenever the dockers are started again.
> - The docker scripts for Mininet (with Stratum) and ONOS, including other helper code, are located under the [`../scripts`] folder. Please go through them to gain some insight.
> **Note:** you can stop the docker by running `make mapreduce-stop-treetopo`
> **Note:** sometimes there is a docker permission denied error that should be fixable by running:
```sh
sudo chmod 666 /var/run/docker.sock
```

## Running Tests
To run the experiments with tree topology, follow the [README.md](mechanism) under the mechanism folder.

## Content
- `mechanism/`: Contains the mininet, P4, [Onos](https://github.com/opennetworkinglab/onos), spatial code example, and traffic send/receive Python scripts.
- `scripts/`: Contains scripts for setting up the tree topology and running experiments. See the files in this folder for more details.
