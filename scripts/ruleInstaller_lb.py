"""A simple rule installer to install flow/group rules for the topology built by topoBuilder.py.
   Flow rules include:
        arp traffic flooding rules
        ip forwarding rules
        ip multipath routing rules
        
   Group rules are used to support ip multipath routing."""

def ruleInstaller (network, server, client, serverEdge, clientEdge, paths, weights, valo, wcmp, random, wrr):

    c = network.controller
    
    """First install simple flow rules"""

    core = paths
    # for cores
    c.cmd ('ovs-ofctl -O OpenFlow13 add-flow core1 arp,actions=flood')
    for i in range (1, core+1):
        for j in range (1, server+1):
            for k in range (1, client+1):
                c.cmd ('ovs-ofctl -O OpenFlow13 add-flow core%s ip,in_port=1,nw_src=20.0.0.%s,nw_dst=20.0.1.%s,actions=output:2' % (i, j, k))
                c.cmd ('ovs-ofctl -O OpenFlow13 add-flow core%s ip,in_port=2,nw_src=20.0.1.%s,nw_dst=20.0.0.%s,actions=output:1' % (i, k, j))
    
    
    # for Host server side edges
    for i in range (1, 2):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Hedges%s arp,actions=flood' % i)
        for j in range (1, server+1):
            c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Hedges%s ip,nw_dst=20.0.1.%s,actions=output:%s' % (i, j, i+server))
            c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Hedges%s ip,nw_dst=20.0.0.%s,actions=output:%s' % (i, j, j))
    
    # for Host client side edges
    for i in range (1, 2):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Hedgec%s arp,actions=flood' % i)
        for j in range (1, client+1):
            c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Hedgec%s ip,nw_dst=20.0.0.%s,actions=output:%s' % (i, j, i+client))
            c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Hedgec%s ip,nw_dst=20.0.1.%s,actions=output:%s' % (i, j, j))
            

    
    
    # for server side edges
    for i in range (1, serverEdge+1):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Edges%s arp,actions=flood' % i)
        for j in range (1, server+1):
          for k in range (1, paths+1):
            c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Edges%s ip,nw_dst=20.0.0.%s,actions=output:%s' % (i, j, i+paths))
    
    # for client side edges
    for i in range (1, clientEdge+1):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Edgec%s arp,actions=flood' % i)
        for j in range (1, client+1):
            for k in range (1, paths+1):
              c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Edgec%s ip,nw_dst=20.0.1.%s,actions=output:%s' % (i, j, i+paths))

    
    """Install group rules in server side edge switches"""

    group_id = 1

    buckets = ''

    for i in range (paths):
        if i == 0:
            buckets += 'bucket=bucket_id:%s,weight:%s,output:%s' % (i+1, weights[i], i+1)
        else:
            buckets += ',bucket=bucket_id:%s,weight:%s,output:%s' % (i+1, weights[i], i+1)
    for i in range (1, serverEdge+1):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-group Edges%s group_id=%s,type=select,valo=%s,wcmp=%s,random=%s,wrr=%s,%s' % (i, group_id, valo, wcmp,random,wrr,buckets))
        group_id += 1
    
    buckets = ''
    for i in range (paths):
        if i == 0:
            buckets += 'bucket=bucket_id:%s,weight:%s,output:%s' %(i+1, weights[i], i+1)
        else:
            buckets += ',bucket=bucket_id:%s,weight:%s,output:%s' %(i+1, weights[i], i+1)
    for i in range (1, clientEdge+1):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-group Edgec%s group_id=%s,type=select,valo=%s,wcmp=%s,random=%s,wrr=%s,%s' % (i, group_id, valo,wcmp, random, wrr, buckets))
        group_id += 1
    
    """Install flow rules that use group rules"""

    group_id = 1

    for i in range (1, serverEdge+1):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Edges%s ip,in_port=%s,actions=group:%s' % (i, i+paths, group_id))
        group_id += 1
    
    for i in range (1, clientEdge+1):
        c.cmd ('ovs-ofctl -O OpenFlow13 add-flow Edgec%s ip,in_port=%s,actions=group:%s' % (i, i+paths, group_id))
        group_id += 1
    