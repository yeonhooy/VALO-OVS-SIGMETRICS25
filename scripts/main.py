import sys, os, re, time
from mininet.cli import CLI

from topoBuilder_lb import topoBuilder
from ruleInstaller_lb import ruleInstaller
from flowGenerator_parll import flowGenerator

if __name__ == "__main__":

    if len (sys.argv) < 2:
        print ('Usages: %s <server#> <client#> <serverEdge#> <clientEdge#> <paths#> [weights ...] <valo> <wcmp> <random> <wrr> <port#> <flowsPerPair#>')
        sys.exit ()

    # compile traffic generator
    os.system ('cd TrafficGenerator && make && cd ..')
    
    server = int(sys.argv[1])
    client = int(sys.argv[2])
    serverEdge = int(sys.argv[3])
    clientEdge = int(sys.argv[4])
    paths = int(sys.argv[5])
    weights = []
    for i in range (paths):
        weights.append (int(sys.argv[6+i]))
    valo = sys.argv[6+paths]
    wcmp = sys.argv[7+paths]
    random = sys.argv[8+paths]
    wrr = sys.argv[9+paths]
    port = int(sys.argv[10+paths])
    flowsPerPair = int(sys.argv[11+paths]) 

    network = topoBuilder (server, client, serverEdge, clientEdge, 1, 1, paths, weights)
    network.start()

    coreSwitches = []
    for switch in network.switches:
        if 'core' in switch.name:
            coreSwitches.append (switch)
    
    
    ruleInstaller(network, server, client, serverEdge, clientEdge, paths, weights, valo, wcmp, random, wrr)
    flowGenerator(network, port, flowsPerPair)

    time.sleep(1)

    # cleanup
    os.system('mn -c')
    os.system('pkill -KILL tshark')
