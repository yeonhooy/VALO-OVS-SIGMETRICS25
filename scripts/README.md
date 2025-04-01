## Overview

* [Part 1](#Repository-organization) describes the source-code organization of this repository.
* [Part 2](#Settings) contains the steps to configure dependencies and compilation to run VALO. We provide pre-requisite/steps for how to install and compile VALO.

## 1. Repository organization 

The repository is organized as follows:

* `script/`: contains scripts for running experiments based on [Mininet](https://github.com/mininet/mininet.git)

## 2. Settings

#### 2-1. Pre-requisite for experiment

1. Install mininet    
     - Download & Install Mininet with all it’s dependencies via git
  
        $ `git clone https://github.com/mininet/mininet.git && cd mininet` 

        $ `sudo ./util/install.sh -a`

     - Remove the auto-installed OVS package   
     $ `sudo ./util/install.sh -r && cd ..`

2. Compile OVS
    - Stop current OVS daemon (if OVS has already installed.)

      $ `sudo ovs-ctl stop`

    - Go to `ovs-valo/` directory and compile, install

      $ `cd ovs-valo`

      $ `sudo ./boot.sh`

      $ `sudo ./configure`

      $ `sudo make`

      $ `sudo make install`

    - Start OVS daemon

      $ `sudo ovs-ctl start`
3. Download Traffic Generator   
$ `git clone https://github.com/HKUST-SING/TrafficGenerator.git`


#### 2-2. How to use
You can use the VALO implementation and others by passing boolean values as arguments to `main.py`   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$ `sudo main.py <server#> <client#> <serverEdge#> <clientEdge#> <paths#> [weights ...] <valo> <wcmp> <random> <wrr> <port#> <flowsPerPair#>`
