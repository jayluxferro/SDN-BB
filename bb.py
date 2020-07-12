#!/usr/bin/python

from mininet.topo import Topo

class BB(Topo):
    def addHosts(self, switches={}, hosts=0):
        # add hosts to switches
        counter = 1
        for switch in switches:
            for _ in range(hosts):
                host = self.addHost('h{}'.format(counter))
                self.addLink(switch, host)
                counter += 1

    def build(self):
        # top level access switches
        tl1 = self.addSwitch('s1')
        tl2 = self.addSwitch('s2')
        tl3 = self.addSwitch('s3')
        tl4 = self.addSwitch('s4')
        tl5 = self.addSwitch('s5')
        # bottm level access switches
        bl1 = self.addSwitch('s6')
        bl2 = self.addSwitch('s7')
        bl3 = self.addSwitch('s8')
        bl4 = self.addSwitch('s9')
        bl5 = self.addSwitch('s10')
        # add hosts
        switches = {tl1, tl2, tl3, tl4, tl5, bl1, bl2, bl3, bl4, bl5 }
        hosts = 12
        self.addHosts(switches=switches, hosts=hosts)

        # mid level core switches
        ml1 = self.addSwitch('s11')
        ml2 = self.addSwitch('s12')
        ml3 = self.addSwitch('s13')
        # link core switches
        self.addLink(ml1, ml2)
        self.addLink(ml2, ml3)

        # top 
        self.addLink(tl1, ml1)
        self.addLink(tl1, ml2)
        self.addLink(tl2, ml1)
        self.addLink(tl2, ml2)
        self.addLink(tl3, ml2)
        self.addLink(tl3, ml3)
        self.addLink(tl4, ml2)
        self.addLink(tl4, ml3)
        self.addLink(tl5, ml2)
        self.addLink(tl5, ml3)

        # bottom
        self.addLink(bl1, ml1)
        self.addLink(bl1, ml2)
        self.addLink(bl2, ml1)
        self.addLink(bl2, ml2)
        self.addLink(bl3, ml1)
        self.addLink(bl3, ml2)
        self.addLink(bl4, ml2)
        self.addLink(bl4, ml3)
        self.addLink(bl5, ml2)
        self.addLink(bl5, ml3)



topos = { 'bb': (lambda: BB()) }
