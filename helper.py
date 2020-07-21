#!/usr/bin/python
"""
Helper script
"""

import subprocess
import sys
import time
import logger as lg

TCPFile = 'tcp.csv'
UDPFile = 'udp.csv'
RTTFile = 'rtt.csv'

def killServer():
    lg.success("[+] Done...")
    cli(['killall', 'iperf'])

def cli(command):
    res = subprocess.Popen(command, stdout=subprocess.PIPE)
    return res.stdout.read()

def iperf(args):
    params = ['iperf']
    params.extend(args)
    return params

def iperf_udp(n1, n2, args):
    lg.warning('...')
    cli(iperf(args))
    rtt(n1, n2, args, 'UDP')
    killServer()

def server(n1, n2, args, isTCP):
    start = time.time()
    lg.warning('Started server...')
    res = []
    for x in cli(iperf(args)).splitlines():
        res.append(x)
    #print(res)
    if isTCP == True:
        lg.warning('TCP')
        # pass tcp output
        data = parseTCP(start, res, args)
        # log data
        handler = open(TCPFile, 'a')
        dData = ''
        for d in data['data']:
            interval = d['interval'].split(' ')[-2]
            transfer = d['transfer'].split(' ')[-2]
            bandwidth = d['bandwidth'].split(' ')[-2]

            dData += '{}, {}, {}, {}, {}\n'.format(n1, n2, interval, transfer, bandwidth)
        handler.write(dData)
        handler.close()
    else:
        res.pop()
        lg.warning('UDP')
        data = parseUDP(start, res, args)
        #print(data)
        # log data
        handler = open(UDPFile, 'a')
        dData = ''
        for d in data['data']:
            interval = d['interval'].split(' ')[-2].split('-')[-1]
            transfer = d['transfer'].split(' ')[-2]
            bandwidth = d['bandwidth'].split(' ')[-2]
            jitter = d['jitter'].split(' ')[-2]
            loss = d['loss']
            totalData = d['totalData']
            lossPercent = d['lossPercent']
            dData += '{}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(n1, n2, interval, transfer, bandwidth, jitter, loss, totalData, lossPercent)
        handler.write(dData)
        handler.close()

def iperf_tcp(n1, n2, args):
    lg.warning('...')
    cli(iperf(args))
    rtt(n1, n2, args, 'TCP')
    killServer()

def rtt(n1, n2, args, proto):
    lg.warning('Running RTT..')
    serverIP = args[args.index('-c') + 1]
    for res in cli(['ping', '-c', '12', serverIP]).splitlines():
        handler = open(RTTFile, 'a')
        resData = ''
        if res.lower().find('icmp_seq') != -1:
            duration = res.split(' ')[-2].split('=')[-1]
            resData += '{}, {}, {}, {}\n'.format(n1, n2, duration, proto)
        handler.write(resData)
        handler.close()

def parseUDP(start, res, args):
    init = False
    SUM = {}
    data = []
    counter = 1
    for x in res:
        if x.lower().find('transfer') != -1:
            init = True

        if init == True and x.lower().find('transfer') == -1 and x != '':
            rcv = x.split('  ')
            #print(rcv)
            data.append({'interval': rcv[1], 'transfer': rcv[2], 'bandwidth': rcv[3], 'jitter': rcv[4], 'loss': rcv[6].split('/')[0], 'totalData': rcv[6].split(' ')[1], 'lossPercent': rcv[6].split(' ')[-1].strip('()').split('%')[0]})
            counter = counter + 1
    if counter - 2 == 0:
        counter = 3

    if counter < 0:
        counter = 2
    return { 'data': data, 'sum': SUM, 'duration': time.time() - start, 'command': ' '.join(args), 'threads': counter - 2}

def parseTCP(start, res, args):
    init = False

    SUM = {}
    data = []
    counter = 1
    for x in res:
        if x.lower().find('transfer') != -1:
            init = True

        if init == True and x.lower().find('transfer') == -1 and x != '':
            rcv = x.split('  ')

            if rcv[0] == '[SUM]' or counter == 1:
                SUM = {'interval':  rcv[-3], 'transfer':  rcv[-2], 'bandwidth':  rcv[-1]}
            else:
                data.append({'interval': rcv[-3], 'transfer': rcv[-2], 'bandwidth': rcv[-1]})
            if counter == 1:
                data.append(SUM)
            counter = counter + 1
    if counter - 2 == 0:
        counter = 3

    if counter < 0:
        counter = 2
    return { 'data': data, 'sum': SUM, 'duration': time.time() - start, 'command': ' '.join(args), 'threads': counter - 2}
