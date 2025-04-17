# OMINE-Artifact-EuroSP25

This repository contains the source code and instructions for building and running the mechanism proposed in the O'MINE: A Novel Collaborative Mechanism for Programmable Data-Planes paper (to appear in EuroS&P25).

O'MINE DDoS detection mechanism comprises multiple programmable components (e.g., ONOS, P4/Tofino, Spatial/MapReduce, Python). The source code is organized as follows:

```sh
O'MINE Artifact
 |-- software
     |--linear                      # Scripts to run the experiments in the linear topology that comprises 5 switches
     |--pytorch_training            # Scripts for training and testing models
     |--reproducibility             # Trained models that run key experiments from the paper and reproduce the corresponding tables/figures
     |--tree                        # Scripts to run the experiments regarding O'MINE scalability
 |-- hardware
```

## Clone the repository to your host machine
 
Clone the `OMINE-Artifact-EuroSP25` repository.

```sh
cd ~
git clone https://github.com/bardhienkeleda/OMINE-Artifact-EuroSP25.git
cd OMINE-Artifact-EuroSP25
```
O'MINE software relies on [Taurus Platform](https://gitlab.com/dataplane-ai/taurus/platform-bm/-/tree/main), 
specifically on the MapReduce block that runs on Docker for running the Machine Learning (ML) models. 
Therefore, start the MapReduce BM dockers according to the topology to be tested---i.e., linear, tree.
```sh
cd ~/OMINE-Artifact-EuroSP25/software/{topology}
make mapreduce-start-<> {linear, tree} 
```

> **Note:** you can stop the docker by running `make mapreduce-stop`
> **Note:** sometimes there is a docker permission denied error that should be fixable by running:
```sh
sudo chmod 666 /var/run/docker.sock
```

## Running Tests

Check `README.md` files for each topology in the `software` folder to run and test O'MINE.

## Contact Us 

- [Enkeleda Bardhi](mailto:E.Bardhi-1@tudelft.nl)
- [Chenxing Ji (Gabriel)](mailto:C.Ji@tudelft.nl)

