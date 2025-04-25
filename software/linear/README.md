# Software Linear Topology with OMINE

This directory implements the linear topology used in our paper, comprising 5 switches.


## Download and start MapReduce BM dockers

Since O'MINE Machine learning module depends on the [Taurus Platform BM](https://gitlab.com/dataplane-ai/taurus/platform-bm/-/tree/main), you need to first download and start the MapReduce BM Docker containers. If the containers haven’t been downloaded before, the following command will initiate the download.

```sh
make mapreduce-start-linear
```

> **Notes:** 
> - As Docker is running these containers for the first time, it will need to download them from https://hub.docker.com. These are large images (hundreds of megabytes), so they may take some time to download depending upon the network speed -- don't worry if the process is slow. It will happen only once, as Docker will cache these images and reuse them whenever the dockers are started again.
> - The docker scripts for Mininet (with Stratum) and ONOS, including other helper code, are located under the [`../scripts`] folder. Please go through them to gain some insight.
> **Note:** you can stop the docker by running `make mapreduce-stop-linear`
> **Note:** sometimes there is a docker permission denied error that should be fixable by running:
```sh
sudo chmod 666 /var/run/docker.sock
```

## Running Tests
To run the experiments with linear topology, follow the [README.md](mechanism) under the mechanism folder.

## Content
- `mechanism/`: Contains the mininet, P4, [Onos](https://github.com/opennetworkinglab/onos), spatial code example, and traffic send/receive Python scripts.
- `scripts/`: Contains scripts for setting up the linear topology and running experiments. See the files in this folder for more details.
