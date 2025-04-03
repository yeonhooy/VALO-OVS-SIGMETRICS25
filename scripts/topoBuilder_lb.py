"""A simple topology builder to build a 2-stage clos network.

   serverHost --- serverEdgeSwitch --- coreSwitch --- clientEdgeSwitch --- clientHost

   Server side network is 20.0.0.0/24
   Client side network is 20.0.1.0/24
   
   All stages can be multipath.
   Edge <-> Core links can be symmetric or asymmetric. Bandwidths are decided by each link's weight. (weight * 100Mbps)
   Host <-> Edge link bandwidths are fixed to 1000Mbps.
   
   *Note that max bandwidth of each link is 1000Mbps."""

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

def topoBuilder (server, client, serverEdge, clientEdge, serverHostEdge, clientHostEdge, paths, weights):
    class topo(Topo):
        serverList = []
        clientList = []
        serverEdgeList = []
        clientEdgeList = []
        serverHostEdgeList = []
        clientHostEdgeList = []
        coreList = []

        # number of cores should be equal to number of paths
        def __init__ (self, server, client, serverEdge, clientEdge, serverHostEdge, clientHostEdge, core, weights):
            Topo.__init__ (self)

            # Make server hosts
            for i in range (1, server+1):
                self.serverList.append (self.addHost ('server%s' % i, mac='00:00:00:00:00:%s' % str(i).zfill(2), ip='20.0.0.%s' % i))
            
            # Make client hosts
            for i in range (1, client+1):
                self.clientList.append (self.addHost ('client%s' % i, mac='00:00:00:00:01:%s' % str(i).zfill(2), ip='20.0.1.%s' % i))
            
            # Make server-side edge switches
            for i in range (1, serverEdge+1):
                self.serverEdgeList.append (self.addSwitch('Edges%s' % i, protocols=['OpenFlow10,OpenFlow13']))

            # Make client-side edge switches
            for i in range (1, clientEdge+1):
                self.clientEdgeList.append (self.addSwitch('Edgec%s' % i, protocols=['OpenFlow10,OpenFlow13']))

            # Make core switches
            for i in range (1, core+1):
                self.coreList.append (self.addSwitch('core%s' % i, protocols=['OpenFlow10,OpenFlow13']))
            
            
            # Make serverHostside switches
            for i in range (1, serverHostEdge+1):
                self.serverHostEdgeList.append (self.addSwitch('Hedges%s' % i, protocols=['OpenFlow10,OpenFlow13']))
            
            # Make clientHostside switches
            for i in range (1, clientHostEdge+1):
                self.clientHostEdgeList.append (self.addSwitch('Hedgec%s' % i, protocols=['OpenFlow10,OpenFlow13']))
            
            ###############################################
            
            # Add serverHostEdge-server links
            for i in range (serverHostEdge):
                for j in range (server):
                    self.addLink (self.serverHostEdgeList[i], self.serverList[j], bw=1000)

            # Add clientHostEdge-client links
            for i in range (clientHostEdge):
                for j in range (client):
                    self.addLink (self.clientHostEdgeList[i], self.clientList[j], bw=1000)
                    
            ################################################        
            


            baseBw = 10

            # Add serverEdge-core links
            for i in range (serverEdge):
                for j in range (core):
                    bw = int(baseBw*weights[j])
                    self.addLink (self.serverEdgeList[i], self.coreList[j], bw=bw)

            # Add clientEdge-core links
            for i in range (clientEdge):
                for j in range (core):
                    bw = int(baseBw*weights[j])
                    self.addLink (self.clientEdgeList[i], self.coreList[j], bw=bw)
                    
            # Add serverHostEdge-serverEdge links
            for i in range (serverHostEdge):
                for j in range (serverEdge):
                    self.addLink (self.serverHostEdgeList[i], self.serverEdgeList[j], bw=1000)

            # Add clientHostEdge-clientEdge links
            for i in range (clientHostEdge):
                for j in range (clientEdge):
                    self.addLink (self.clientHostEdgeList[i], self.clientEdgeList[j], bw=1000)
            
    
    topology = topo (server=server, client=client, serverEdge=serverEdge, clientEdge=clientEdge, serverHostEdge=serverHostEdge, clientHostEdge=clientHostEdge, core=paths, weights=weights)
    
    controller = RemoteController ('controller')
    network = Mininet (topo=topology, controller=controller, link=TCLink)

    return network