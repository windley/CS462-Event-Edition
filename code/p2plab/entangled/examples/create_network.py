#!/usr/bin/env python
#
# This library is free software, distributed under the terms of
# the GNU Lesser General Public License Version 3, or any later version.
# See the COPYING file included in this archive
#

# Thanks to Paul Cannon for IP-address resolution functions (taken from aspn.activestate.com)

import os, sys, time, signal

def destroyNetwork(nodes):
    print 'Destroying Kademlia network...'
    i = 0
    for node in nodes:
        i += 1
        hashAmount = i*50/amount
        hashbar = '#'*hashAmount
        output = '\r[%-50s] %d/%d' % (hashbar, i, amount)
        sys.stdout.write(output)
        time.sleep(0.15)
        os.kill(node, signal.SIGTERM)
    print

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage:\n%s AMOUNT_OF_NODES [NIC_IP_ADDRESS]' % sys.argv[0]
        print '\nNIC_IP_ADDRESS should be the IP address of the network interface through'
        print 'which other systems will access these Kademlia nodes.\n'
        print 'If omitted, the script will attempt to determine the system\'s IP address'
        print 'automatically, but do note that this may result in 127.0.0.1 being used (i.e.'
        print 'the nodes will only be reachable from this system).\n'
        sys.exit(1)
    amount = int(sys.argv[1])
    if len(sys.argv) >= 3:
        ipAddress = sys.argv[2]
    else:
        import socket
        ipAddress = socket.gethostbyname(socket.gethostname())
        print 'Network interface IP address omitted; using %s...' % ipAddress
    
    startPort = 4000
    port = startPort+1
    nodes = []
    print 'Creating Kademlia network...'
    try:
        nodes.append(os.spawnlp(os.P_NOWAIT, 'python', 'python', '../entangled/node.py', str(startPort)))
        for i in range(amount-1):
            time.sleep(0.15)
            hashAmount = i*50/amount
            hashbar = '#'*hashAmount
            output = '\r[%-50s] %d/%d' % (hashbar, i, amount)
            sys.stdout.write(output)
            nodes.append(os.spawnlp(os.P_NOWAIT, 'python', 'python', '../entangled/node.py', str(port), ipAddress, str(startPort)))
            port += 1
    except KeyboardInterrupt:
        '\nNetwork creation cancelled.'
        destroyNetwork(nodes)
        sys.exit(1)
    
    print '\n\n---------------\nNetwork running\n---------------\n'
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        destroyNetwork(nodes)
