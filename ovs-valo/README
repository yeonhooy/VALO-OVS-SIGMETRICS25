# VALO 
* VALO provides accurate and efficient multipath routing for software switch. We implement VALO with Open VSwitch.    
* This repository contains the implementation of VALO-OVS and also other multipath routing schemes of Random/WRR/WCMP/Scoring, which produce results in our paper.

## Overview

We provide all source codes, including VALO-OVS implementation and Random/WRR/WCMP-OVS implementation.

* [Part 1](#Repository-organization) describes the source-code organization of this repository.
* [Part 2](#Settings) contains the steps to configure dependencies and compilation to run VALO. We provide pre-requisite/steps for how to install and compile VALO.
* [Part 3](#Modified-Part) contains the information about which parts of OVS are modified to implement VALO and other multipath routing schemes.

## 1. Repository organization 

The repository is organized as follows:

* `ovs-valo/`: contains VALO/Random/WRR/WCMP/OVS implementation based on [Open vSwitch](https://github.com/openvswitch/ovs)
* We provide a separate command parser in OVS to enable all multipath routing schemes to operate within a single source code.

## 2. Settings

#### 2-1. Pre-requisite
  1. Stop current OVS daemon (if OVS has already installed.)

      $ `sudo ovs-ctl stop`

  2. Go to `ovs-valo/` directory and compile, install

      $ `cd ovs-valo`

      $ `sudo ./boot.sh`

      $ `sudo ./configure`

      $ `sudo make`

      $ `sudo make install`

  3. Start OVS daemon

      $ `sudo ovs-ctl start`

 #### 2-2. How to use
 You can use the implementation VALO by giving boolean values as the parameters when you add group rule using `ovs-ofctl` <br>
    
    - VALO 
    $ ovs-ofctl -O OpenFlow13 add-group <switch-name> group_id=<groud-id>,type=select,valo=true,wrr=false,wcmp=false,random=false
    
    - Random
    $ ovs-ofctl -O OpenFlow13 add-group <switch-name> group_id=<groud-id>,type=select,valo=false,wrr=false,wcmp=false,random=true
    
    - WRR 
    $ ovs-ofctl -O OpenFlow13 add-group <switch-name> group_id=<groud-id>,type=select,valo=false,wrr=true,wcmp=false,random=false
    
    - Scoring 
    $ ovs-ofctl -O OpenFlow13 add-group <switch-name> group_id=<groud-id>,type=select,valo=false,wrr=false,wcmp=false,random=false
    
    - WCMP 
    $ ovs-ofctl -O OpenFlow13 add-group <switch-name> group_id=<groud-id>,type=select,valo=false,wrr=false,wcmp=true,random=false

 
## 3. Modified-Part (Implementation)

- This repository contains the implementation of VALO and the implementation of Random/WRR/WCMP/Scoring, which produce results in our paper. <be>

- We provide all source codes, including VALO-OVS implementation and Random/WRR/WCMP-OVS implementation. <be>

- Note that Scoring is a default implementation of OVS, so we just use the default implementation of OVS.

- We confirm that no other Open vSwitch code has been modified, except for the files listed below.<br>

* Our changes: `ovs-valo/`
    * ovs-valo/lib/ofp-util.c
    * ovs-valo/lib/ofp-parse.c
    * ovs-valo/include/openvswitch/ofp-util.h
