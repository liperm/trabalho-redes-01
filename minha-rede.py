#!/usr/bin/python

from mininet.node import Host
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call


def myNetwork():

    net = Mininet_wifi(
      topo=None,
      build=False, 
      link=wmediumd, 
      wmediumd_mode=interference, 
      ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches/APs\n')
    ap1 = net.addAccessPoint(
      'ap1', 
      cls=OVSKernelAP, 
      ssid='minha-rede',
      channel='1', 
      mode='g', 
      passwd='123456789a', 
      encrypt='wpa2',
      position='738.0,294.0,0')

    info( '*** Add hosts/stations\n')
    sta1 = net.addStation(
      'sta1', 
      ip='192.168.1.2/24',
      position='460.0,290.0,0', 
      radius_identity='minha-rede', 
      passwd='123456789a', 
      encrypt='wpa2',
      range=116)

    sta2 = net.addStation(
      'sta2', ip='192.168.1.3/24',
      position='1014.0,279.0,0', 
      radius_identity='minha-rede',
      passwd='123456789a',
      encrypt='wpa2',
      range=174)

    sta3 = net.addStation(
      'sta3', 
      ip='192.168.1.4/24',
      position='742.0,569.0,0', 
      radius_identity='minha-rede', 
      passwd='123456789a', 
      encrypt='wpa2',
      range=232)

    h1 = net.addHost('h1', cls=Host, ip='192.168.1.254/24', defaultRoute=None)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(sta3, ap1)
    net.addLink(ap1, h1)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap1').start([])

    info( '*** Post configure nodes\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

