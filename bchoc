#!/usr/bin/python
'''
Luis Claramunt
Jacob Babik 
Ben Downes
CSE 469 Group Project
April 28, 2020
'''
import sys
import struct
import os
import hashlib
import time
import uuid
import random
import datetime
import argparse

global uid              #Remove later, used to verify case ID match

class Block:
    def __init__(self, state, parent = None, time = round(time.time(), 2), 
    caseId = uuid.uuid4(), itemID = random.getrandbits(32),
    dataLength = 14, bData = b'Initial block\0'):
        self.parent_hash = parent
        self.local_time = time
        self.case_ID = caseId
        self.evidence_item_ID = itemID
        self.state = state
        self.data_length = dataLength
        self.data = bData
        print("Case ID: ", self.case_ID.int)

    def getHash(self):
        return self.parent_hash

    def getTime(self):
        return self.local_time

    def getCaseID(self):
        return self.case_ID

    def getItemID(self):
        return self.evidence_item_ID
    
    def getState(self):
        return self.state

    def getDataLength(self):
        return self.data_length
    
    def getData(self):
        return self.data
    
    def setState(self, newState):
        self.state = newState

chain = []
transaction = []
#self.ids = []

def update():
    readFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
    readBytes = readFile.read(68)
    while len(readBytes) == 68:
        block = struct.unpack('20s d 16s I 11s I', readBytes)
        print("Hash: ", block[0])
        print("Time: ", block[1])
        print("Case ID: ", block[2])
        print("Item ID: ", block[3])
        print("State: ", block[4])
        print("Data Length: ", block[5])
        print("Data: ", readFile.read(block[5]))
        newBlock = Block(block[4], parent=block[0], time=block[1], caseId=block[2], itemID=block[3], 
                dataLength=block[5], 
                bData=readFile.read(block[5]))
        chain.append(newBlock)
        print(block[2])
        readBytes = readFile.read(68) 


def initialize(args)  :
    try:
        newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
        readBytes = newFile.read(68)
        while len(readBytes) == 68:
            block = struct.unpack('20s d 16s I 11s I', readBytes)
            newBlock = Block(block[4], parent=block[0], time=block[1], caseId=block[2], itemID=block[3], 
                dataLength=block[5], bData=readBytes.read(block[5]))
            chain.append(newBlock)
            readBytes = newFile.read(68)  
        print('Blockchain file found with INITIAL block.')
    except:
        newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'wb')
        block = Block(state='INITIAL')
        chain.append(block)
        structBlock = struct.pack('20s d 16s I 11s I', str(block.getHash()), block.getTime(), 
            str(block.getCaseID().int), block.getItemID(), block.getState(), block.getDataLength())
        newFile.write(structBlock)
        newFile.write(block.getData().encode())
        newFile.close()
        print('Blockchain file not found. Created INITIAL block.')

def getBlockCaseId(caseID):
    print(len(chain))
    for block in list(chain):
        print("Block ", block)
        if block.getCaseID() == caseID:
            print(block.getCaseID())
            return block
    return False

def checkInBlockItemId(itemId):
    for block in list(chain):
        if block.getItemID() == itemId:
            block.setState('CHECKEDIN')
            return block
    return False
    
def addBlock(args):
    update()
    block = getBlockCaseId(args.case_ID)
    

    if block is False:
        print('There is no Block under such Case ID')
    # else:
    #     blockFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
    #     print("Case: {}".format(caseId))
    #     newOnes = list(argv[0])
    #     for itemId in newOnes:
    #         newBlock = Block('CHECKEDIN', parent=block, itemID=itemId)
    #         self.chain.append(newBlock)
    #         structBlock = struct.pack('20s d 16s I 11s I', str(newBlock.getHash()), newBlock.getTime(), 
    #             str(newBlock.getCaseID()), newBlock.getItemID(), newBlock.getState(), newBlock.getDataLength())
    #         blockFile.write(structBlock)
    #         blockFile.write(newBlock.getData().encode())
        
    #         print("Added item: {}\n  Status: 'CHECKEDIN'\n  Time of action: {}".
    #             format(itemId, datetime.datetime.now()))
    #     blockFile.close()

    # def checkOut(self, itemId):
    #     found = False
    #     for block in list(self.chain):
    #         if block.getItemID() == itemId and block.getState() == 'CHECKEDIN':
    #             block.setState('CHECKEDOUT')
    #             print('Case: {}\nChecked out item: {}\n  Status: CHECKEDOUT\n  Time of action: {}'.
    #                 format(block.getCaseID(), itemId, datetime.datetime.now()))
    #             found = True
    #         elif block.getItemID() == itemId and block.getState() == 'CHECKEDOUT':
    #             print('Error: Cannot check out a checked out item. Must check it in first.\n$ echo $?\n1')      #Might remove the $ part later
    #             found = True

    #     if found is False:
    #         print('There is no Block under such Item ID')
    

    # #Adjust to take care of different states DISPOSED, DESTROYED, RELEASED...
    # def checkIn(self, itemId):
    #     found = False
    #     for block in list(self.chain):
    #         if block.getItemID() == itemId:
    #             block.setState('CHECKEDIN')
    #             print('Case: {}\nChecked in item: {}\n  Status: CHECKEDIN\n  Time of action: {}'.
    #             format(block.getCaseID(), itemId, datetime.datetime.now()))
    #             found = True

    #     if found is False:
    #         print('There is no Block under such Item ID')

    # def log(self, reverse=False):
    #     self.chain.sort(key=lambda x: x.evidence_item_ID, reverse=False)
    #     for block in list(self.chain):
    #         print('Item: {}\nAction: {}\nTime: {}\n'.
    #         format(block.getItemID(), block.getState(), block.getTime()))

def hello_world(args):
    print("HELLO WE MADE IT!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('./bchoc', nargs='?', type=str, help='Enter the command you like to execute')
    subParser = parser.add_subparsers(title='commands')

    '''Initialize the Blockchain'''
    bchoc_init = subParser.add_parser('init', description='Initialize the Blockchain.')
    bchoc_init.set_defaults(func=initialize)

    '''Add a Block to the Blockchain'''
    add = subParser.add_parser('add')
    add.add_argument('-c', dest="case_ID", type=str, required=True)
    add.add_argument('-i', dest="item_ID", type=str, required=True, action='append')
    add.set_defaults(func=addBlock)

    # checkout = subParser.add_parser('checkout')
    # checkout.add_argument('-i', dest="item_ID", type=str, required=True, nargs='1')
    # checkout.set_defaults(func=Blockchain.checkOut)

    # checkin = subParser.add_parser('checkin')
    # checkin.add_argument('-i', dest="item_ID", type=str, required=True, nargs='1')
    # checkin.set_defaults(func=Blockchain.checkIn)

    # log =subParser.add_parser('log')
    # log.add_argument('-r', required=False)
    # log.add_argument('-n', dest='num', type=int, nargs='*')
    # log.add_argument('-c', dest='case_ID', type=int, nargs='*')
    # log.add_argument('-i', dest='item_ID', type=int, nargs='*')  
    args = parser.parse_args()
    args.func(args)

    # if len(sys.argv) > 1:
    #     if sys.argv[1] == 'init':           #Initialize
    #         blockChain = Blockchain()
    #         blockChain.initialize()
    #     elif sys.argv[1] == 'add':
    #         blockChain = Blockchain()       #Initialize, part of the test, delete later
    #         blockChain.initialize()
    #         #blockChain.addBlock(uid, sys.argv[5:len(sys.argv)])        #Use the line below, uid is for testing 
    #         blockChain.log()
    #         #blockChain.addBlock(sys.argv[3], sys.argv[5:len(sys.argv)])
    #     elif sys.argv[1] == 'checkout':
    #         blockChain.checkOut(sys.argv[3])
    #     elif sys.argv[1] == 'checkin':
    #         blockChain.checkIn(sys.argv[3])
   
if __name__ == "__main__":
    main()
    