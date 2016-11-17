# doctor.py
# ------------------------------------------------------------------
# Script for generating generic data, which is then used as
# background test information in an Elastic Stack architecture.
# ------------------------------------------------------------------
# POC: Red Thomas <red.thomas@redknightllc.com>
# ------------------------------------------------------------------

import datetime
import json
import os
import random
import time

# Load all the config files and return dictionaries
def loadConfig():
    with open("/opt/doctor/conf/doc_conf.json") as data_file:
        config = json.load(data_file)

    with open("/opt/doctor/conf/doc_system.json") as data_file:
        system = json.load(data_file)

    with open("/opt/doctor/conf/doc_interface.json") as data_file:
        interface = json.load(data_file)

    with open("/opt/doctor/conf/doc_process.json") as data_file:
        process = json.load(data_file)

    with open("/opt/doctor/conf/doc_user.json") as data_file:
        user = json.load(data_file)

    return (config, system, interface, process, user)


# Build random event
def genEvent(system, interface, process, user):

    randSys = {}
    randSys['interfaces'] = []
    randSys['users'] = []
    randSys['processes'] = []

    #Create a system
    randSys['hostname'] = random.choice(system['prefix']) + "-" + random.choice(system['hostname']) + "-" + str(random.randint(0,system['postfix']))
    
    #Create random number of interfaces (lower numbers more common)
    numInts = random.sample([1,1,1,1,2,2,2,3,3,4], 1)
    intNum = 0
    while intNum <= numInts[0]:
        intf = {}
        intf['mac'] = random.choice(interface['mac'])
        intf['id'] = random.choice(interface['id'])


        # Read in IP and Subnet as a CIDR, and split IP into octets
        addr = interface['ip'].split('.')
        mask = [0, 0, 0, 0]
        for i in range(interface['subnet']):
            mask[i/8] = mask[i/8] + (1 << (7 - i % 8))

        # Setup the Network
        net = []
        for i in range(4):
            net.append(int(addr[i]) & mask[i])

        # Calculate the Broadcast IP
        broad = list(net)
        brange = 32 - interface['subnet']
        for i in range(brange):
            broad[3 - i/8] = broad[3 - i/8] + (1 << (i % 8))

        # Use broadcast and network values to generate random IP
        randIP = []
        for i in range(4):
            randIP.append(random.randint(net[i],broad[i]))

        intf['ip'] = ".".join(map(str,randIP))

        # Append new interface to randSys and ++i
        randSys['interfaces'].append(intf)

        intNum = intNum + 1

    # Create random number of users
    numUsers = random.randint(1,10)
    intNum = 0
    while intNum <= numUsers:
        randUser = {}
        randUser['session'] = random.randint(0,9999)
        randUser['name'] = random.choice(user['username'])

        # User logged on random amount of time
        randTime = random.randint(1,3600)
        randUser['startime'] = str(datetime.datetime.now() - datetime.timedelta(seconds=randTime))

        randSys['users'].append(randUser)
        intNum = intNum + 1

    # Generate random number of processes
    numProcs = random.randint(10,20)
    intNum = 0
    while intNum <= numProcs:
         randSys['processes'].append(random.choice(process['process']))
         intNum = intNum + 1


    print(randSys)







# Main Loop
def main():

    (config, system, interface, process, user) = loadConfig()
    genEvent(system, interface, process, user)


if __name__ == '__main__':
    main()
