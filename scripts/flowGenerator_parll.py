"""Generate flows using the TrafficGenerator tool.
   https://github.com/HKUST-SING/TrafficGenerator """

import os, time
import multiprocessing 
from multiprocessing import Pool
from itertools import product
from contextlib import contextmanager

from mininet.cli import CLI

def flowGenerator (network, port, flowsPerPair):
    workDirectory = os.getcwd()

    allHosts = network.hosts
    serverHosts = []
    clientHosts = []

    for host in allHosts:
        if host.name[0] == 's':
            serverHosts.append (host)
    for host in allHosts:
        if host.name[0] == 'c':
            clientHosts.append (host)



    for clientIndex in range (len (clientHosts)):
        configLines = []


        serverIp = serverHosts[clientIndex % len (serverHosts)].params['ip']
        line = 'server %s %s' % (serverIp, port)
        configLines.append (line)

        cdf = 'temp_CDF.txt' # originally DCTCP_CDF
        line = 'req_size_dist TrafficGenerator/conf/%s' % cdf
        configLines.append (line)

        with open ('TrafficGenerator/conf/client%s_config.txt' % clientIndex, 'w') as configFile:
            for line in configLines:
                configFile.write (line)
                configFile.write ('\n')
    
    # Delete previous results

    resultText = 'flows.txt'
    if os.path.exists ('TrafficGenerator/%s' % resultText):
        os.remove ('TrafficGenerator/%s' % resultText)

    # Start server daemons

    startServer(serverHosts, flowsPerPair, port)
    
    time.sleep (1)
    print ('opened all servers...')

    # CLI (network)
    
    # Start client requests
    poolcount = multiprocessing.cpu_count()
    print(poolcount)
    pool = Pool(poolcount)
    #parll_func = partial(startClient, clientHosts, flowsPerPair)
    lenHosts = len(clientHosts)
    
    processes = []
    print("lenHosts",lenHosts)
    for cIndex in range(0,lenHosts): 
        p = multiprocessing.Process(target=startClient, args=(clientHosts, flowsPerPair,cIndex))  
        p.start()
        processes.append(p)
 
    for process in processes:
        process.join()
    
    print ('client requests done...')

def startServer(serverHosts, flowsPerPair, port):
  for server in serverHosts:
        print ('open ' + server.name + ' port#%s' % (port))
        server.cmd ('TrafficGenerator/bin/server -p %s -d ' % (port))
          
def startClient(clientHosts, flowsPerPair, clientIndex):
  print ('start flows from ' + clientHosts[clientIndex].name)
  print (clientHosts[clientIndex].name+ ' client flow generate current time' + time.strftime('%Y.%m.%d - %H:%M:%S'))
  clientHosts[clientIndex].cmd ('TrafficGenerator/bin/client -b 900 -c TrafficGenerator/conf/client%s_config.txt -n %s -l flows.txt -s 1 -v > log_%s.txt' % (clientIndex, flowsPerPair, clientIndex))
def merge_startClinet(args):
  startClient(*args)