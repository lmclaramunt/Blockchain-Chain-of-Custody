#!/usr/bin/python
'''
Luis Claramunt
Jacob Babik 
Ben Downes
CSE 469 Group Project
April 28, 2020
'''
import sys
import hashlib
import time
import uuid
import random
import datetime

global uid              #Remove later, used to verify case ID match

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction = []
        #self.ids = []

    def initialize(self):
        if not self.chain:
            block = Block(0, 'INITIAL')
            global uid                  #Remove later, used to verify case ID match
            uid = block.getCaseID()     #Remove later
            self.chain.append(block)
            print('Blockchain file not found. Created INITIAL block.')
        else:
            print('Blockchain file found with INITIAL block.')

    def getCaseId(self, caseID):
        for block in list(self.chain):
            if block.getCaseID() == caseID:
                return block
        return False

    def getItemId(self, itemId):
        for block in list(self.chain):
            if block.getItemID() == itemId:
                block.setState('CHECKEDIN')
                return block
        return False
    
    def addBlock(self, caseId, *argv):
        block = self.getCaseId(caseId)

        if block is False:
            print('There is no Block under such Case ID')
        else:
            print("Case: {}".format(caseId))
            newOnes = list(argv[0])
            for itemId in newOnes:
                newBlock = Block(block, 'CHECKEDIN', itemId)
                self.chain.append(newBlock)
                print("Added item: {}\n  Status: 'CHECKEDIN'\n  Time of action: {}".
                format(itemId, datetime.datetime.now()))

    def checkOut(self, itemId):
        found = False
        for block in list(self.chain):
            if block.getItemID() == itemId and block.getState() == 'CHECKEDIN':
                block.setState('CHECKEDOUT')
                print('Case: {}\nChecked out item: {}\n  Status: CHECKEDOUT\n  Time of action: {}'.
                format(block.getCaseID(), itemId, datetime.datetime.now()))
                found = True
            elif block.getItemID() == itemId and block.getState() == 'CHECKEDOUT':
                print('Error: Cannot check out a checked out item. Must check it in first.\n$ echo $?\n1')      #Might remove the $ part later
                found = True

        if found is False:
            print('There is no Block under such Item ID')
    

    #Adjust to take care of different states DISPOSED, DESTROYED, RELEASED...
    def checkIn(self, itemId):
        found = False
        for block in list(self.chain):
            if block.getItemID() == itemId:
                block.setState('CHECKEDIN')
                print('Case: {}\nChecked in item: {}\n  Status: CHECKEDIN\n  Time of action: {}'.
                format(block.getCaseID(), itemId, datetime.datetime.now()))
                found = True

        if found is False:
            print('There is no Block under such Item ID')

    def log(self, reverse=False):
        self.chain.sort(key=lambda x: x.evidence_item_ID, reverse=False)
        for block in list(self.chain):
            print('Item: {}\nAction: {}\nTime: {}\n'.
            format(block.getItemID(), block.getState(), block.getTime()))

class Block:
    def __init__(self, parent, state, itemID=random.getrandbits(32)):
        self.parent_hash = 0
        self.local_time = round(time.time(), 2)
        self.case_ID = uuid.uuid4()
        self.evidence_item_ID = itemID
        self.state= state
        self.data_length = 14
        self.data = b'Initial block\0'   

    def getCaseID(self):
        return self.case_ID

    def getItemID(self):
        return self.evidence_item_ID
    
    def getState(self):
        return self.state

    def getTime(self):
        return self.local_time
    
    def setState(self, newState):
        self.state = newState

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':           #Initialize
            blockChain = Blockchain()
            blockChain.initialize()
        elif sys.argv[1] == 'add':
            blockChain = Blockchain()       #Initialize, part of the test, delete later
            blockChain.initialize()
            blockChain.addBlock(uid, sys.argv[5:len(sys.argv)])        #Use the line below, uid is for testing 
            blockChain.log()
            #blockChain.addBlock(sys.argv[3], sys.argv[5:len(sys.argv)])
        elif sys.argv[1] == 'checkout':
            blockChain.checkOut(sys.argv[3])
        elif sys.argv[1] == 'checkin':
            blockChain.checkIn(sys.argv[3])

    

if __name__ == "__main__":
    main()
    