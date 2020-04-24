#!/usr/bin/python3
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
import collections
from datetime import datetime as dt
import datetime
from uuid import UUID
import pdb
import subprocess
#Convert from bytes to UUID uuid.UUID(bytes=b'\xf0\xe2\xfc\xe7\xf6\xdcL\xe3\x85\xb8\x12\x00u\x82\x1c\x0b')
Block = collections.namedtuple('Block', ['prev_block_hash', 'time', 'caseID', 'itemID', 'state', 'data_length', 'data'])
states = {'initial': b'INITIAL\x00\x00\x00\x00', 'checkin': b'CHECKEDIN\x00\x00', 'checkout': b'CHECKEDOUT\x00', 'DISPOSED': b'DISPOSED\x00\x00\x00', 'DESTROYED':b'DESTROYED\x00\x00', 'RELEASED': b'RELEASED\x00\x00\x00'}
chain = []
ids = []
parent = None       #The last block read

def update_info():
    global parent
    newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
    readBytes = newFile.read(68)
    readBlock = struct.unpack('20s d 16s I 11s I', readBytes)
    hashBlock = readBlock[0]
    assert hashBlock == bytearray(20)       #Assert to verify syntax of given blocks

    case_id = uuid.UUID(bytes=readBlock[2])         #Convert case ID from bytes to string
    assert case_id == uuid.UUID(int=0)

    item_id = readBlock[3]
    assert item_id == 0
    ids.append(item_id)         #Keep track of block IDs

    state = readBlock[4]
    assert state == states['initial']

    length = readBlock[5]
    assert length == 14

    data = newFile.read(readBlock[5])
    assert data == b'Initial block\x00'

    block = Block(prev_block_hash=hashBlock,time=readBlock[1],caseID=case_id,
        itemID=item_id,state=state,data_length=length, data=data.decode())
    chain.append(block)

    readBytes = newFile.read(68)
    parent = block
    while len(readBytes) == 68:
        readBlock = struct.unpack('20s d 16s I 11s I', readBytes)   #Unpack next block
        item_id = readBlock[3]
        ids.append(item_id)                 #Keep track of block IDs
        data = newFile.read(readBlock[5]).decode()
        block = Block(prev_block_hash=readBlock[0],
            time=readBlock[1],
            caseID=uuid.UUID(bytes=readBlock[2]),
            itemID=readBlock[3],
            state=readBlock[4],
            data_length=readBlock[5], data=data)
        chain.append(block)
        parent = block                  #The last to be read will be the parent of the ones to be added
        readBytes = newFile.read(68)
    newFile.close()

def initialize(args)  :
    try:
        global parent
        newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
        readBytes = newFile.read(68)
        readBlock = struct.unpack('20s d 16s I 11s I', readBytes)
        hashBlock = readBlock[0]
        assert hashBlock == bytearray(20)

        case_id = uuid.UUID(bytes=readBlock[2])         #Convert case ID from bytes to string
        assert case_id == uuid.UUID(int=0)

        item_id = readBlock[3]
        assert item_id == 0
        ids.append(item_id)         #Keep track of block IDs

        state = readBlock[4]
        assert state == states['initial']

        length = readBlock[5]
        assert length == 14

        data = newFile.read(readBlock[5])
        assert data == b'Initial block\x00'

        block = Block(prev_block_hash=hashBlock,
            time=readBlock[1],
            caseID=case_id,
            itemID=item_id,
            state=state,
            data_length=length, data=data.decode())
        chain.append(block)
 
        readBytes = newFile.read(68)
        parent = block
        while len(readBytes) == 68:
            readBlock = struct.unpack('20s d 16s I 11s I', readBytes)
            hashBlock = readBlock[0]
            case_id = uuid.UUID(bytes=readBlock[2])         #Convert case ID from bytes to string
            item_id = readBlock[3]
            ids.append(item_id)         #Keep track of block IDs
            state = readBlock[4]                #Keep track of block ID since they have to be unique
            length = readBlock[5]

            data = newFile.read(readBlock[5]).decode()
            block = Block(prev_block_hash=readBlock[0],
                time=readBlock[1],
                caseID=case_id,
                itemID=readBlock[3],
                state=readBlock[4],
                data_length=readBlock[5], data=data)
            chain.append(block)
            parent = block
            readBytes = newFile.read(68)
        newFile.close()
        print('Blockchain file found with INITIAL block.')
    except FileNotFoundError:
        newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'ab')
        initialBlock = Block(bytearray(20),
            datetime.datetime.utcnow().timestamp(),
            uuid.UUID(int=0),
            0,
            states['initial'],
            14,
            b'Initial block\0')
        chain.append(initialBlock)
        newFile.write(struct.pack('20s d 16s I 11s I', bytearray(20),
            initialBlock.time,
            bytearray(16),
            initialBlock.itemID,
            initialBlock.state,
            initialBlock.data_length))
        newFile.write(initialBlock.data)
        newFile.close()
        print('Blockchain file not found. Created INITIAL block.')
    except:
        print('Invalid Blockchain')
        sys.exit(1)

def getBlockCaseId(case_ID):
    uuid_case_id = uuid.UUID(case_ID)        #Convert from string to UUID for comparison
    b = False
    for block in chain:
        if block.caseID == uuid_case_id:
            b = block
    return b                            #Return false if block is never found

def getBlockItemId(item_ID):
    id = int(item_ID)
    b = False
    for block in chain:
        if block.itemID == id:
            b = block
    return b                        #Return false if block is never found

def hash(block):
    stringBlock = ""
    for item in block:
        stringBlock += str(item)
    return hashlib.sha1(stringBlock.encode()).digest()

def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str

def addBlock(args):
    try:
        update_info()           #Get info in the file into the chain list
    except:
        initialize(args)        #If there is no info, initialize the blockchain

    try:
        update_info()
        global parent

        #addFile = open('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH', 'ab')
        addFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'ab')
        print('Case: {}'.format(args.case_ID))
        for id in args.item_ID:
            #pdb.set_trace()
            if int(id) in ids: sys.exit(1)     #Check for duplicate item_ID
            ids.append(int(id))                #Keep track of IDS
            newBlock = Block(prev_block_hash=hash(parent),
                time=datetime.datetime.utcnow().timestamp(),
                caseID= (UUID(str(args.case_ID))),
                itemID=int(id),
                state=states['checkin'],
                data_length=0,
                data=b'')
            chain.append(newBlock)

            addFile.write(struct.pack('20s d 16s I 11s I', newBlock.prev_block_hash,
                newBlock.time,
                #reverse(newBlock.caseID),
                newBlock.caseID.int.to_bytes(16, byteorder="little"),
                newBlock.itemID,
                newBlock.state,
                newBlock.data_length))
            addFile.write(newBlock.data)
            print('Added item: {}\n  Status: {}\n  Time of action: {}'.
                format(id, 'CHECKEDIN', dt.fromtimestamp(newBlock.time).isoformat()))
        addFile.close()
        #print(chain)
    except:
        sys.exit(1)

def checkOut(args):
    try:
        update_info()
        block = getBlockItemId(args.item_ID)
        #print(block.state)
        if block is False:
            print('No block under such ID')
            sys.exit(1)
        elif block.state != states['checkin']:
            print('Error: Cannot check out a checked out item. Must check it in first.')
            sys.exit(404)
        elif block.state is states['DISPOSED'] or block.state is states['RELEASED'] or block.state is states['DESTROYED']:
            print('Error: Cannot check out a block that has already been removed!')
            sys.exit(404)
        else:
            addFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'ab')
            #addFile = open('BCHOC_FILE_PATH', 'ab')
            time = datetime.datetime.utcnow().timestamp()
            addFile.write(struct.pack('20s d 16s I 11s I', block.prev_block_hash,
                time,
                block.caseID.bytes,
                block.itemID,
                states['checkout'],
                block.data_length))
            addFile.write(bytes(block.data, 'utf-8'))
            addFile.close()
            print('Case {}\nChecked in item: {}\n  Status: {}\n  Time of action: {}.'.
                format(block.caseID, args.item_ID, 'CHECKEDOUT', dt.fromtimestamp(time).isoformat()))
    except:
        sys.exit(1)

def checkIn(args):
    # try:
        update_info()
        block = getBlockItemId(args.item_ID)
        global parent
        #print(block.state)
        if block is False:
            print('No block under such ID')
            sys.exit(1)
        elif block.state == b'CHECKEDIN\x00\x00':
            print('That block is already checked in')
            sys.exit(404)
        elif block.state == b'DISPOSED\x00\x00\x00' or block.state == b'RELEASED\x00\x00\x00' or block.state == b'DESTROYED\x00\x00':
            print('Error: Cannot check in a block that has already been removed!')
            sys.exit(404)
        else:
            addFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'ab')
            #addFile = open('BCHOC_FILE_PATH', 'ab')
            time = datetime.datetime.utcnow().timestamp()
            addFile.write(struct.pack('20s d 16s I 11s I', block.prev_block_hash,
                time,
                block.caseID.bytes,
                block.itemID,
                states['checkin'],
                block.data_length))
            addFile.write(bytes(block.data, 'utf-8'))
            addFile.close()
            print('Case: {}\nChecked in item: {}\n  Status: {}\n  Time of action: {}.'.
                format(block.caseID, args.item_ID, 'CHECKEDIN', dt.fromtimestamp(time).isoformat()))
    # except:
    #     sys.exit(1)

def remove_(args):
    if args.reason == 'RELEASED':
        if not args.owner:
            print('-o owner name is required')
            sys.exit(404)
    try:
        #pdb.set_trace()
        update_info()
        block = getBlockItemId(args.item_ID)
        if block is False:
            print('No block under such ID')
            sys.exit(4)
        if block.state == states['checkin']:
            #Find block in file
            found = False
            total = 0  #total bytes read
            offset = 0
            #filePath = os.environ['BCHOC_FILE_PATH']
            file = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')

            while not found:
                bytes = file.read(68)
                if not bytes:
                    break

                block = struct.unpack('20s d 16s I 11s I', bytes)
                item_id = block[3]   #This is item ID
                if item_id == int(args.item_ID):
                    found = True
                    offset = total

                blockData = file.read(block[5])  #Skip over data
                total = total + 68 + block[5]

            file.close()

            #Create new block based on user input  
            length = block[5] if args.owner == None else len(args.owner)+1      #Set the length of the content to be written 
            data = blockData if args.owner == None else (args.owner + "\x00").encode()      #The owner's info could be written in this block
            modifiedBlock = Block(prev_block_hash=block[0],
                time=datetime.datetime.utcnow().timestamp(),
                caseID=block[2],
                itemID=int(block[3]),
                state=states[str(args.reason)],
                data_length=length,  ##Elected to not add owner info to modified block, might be necessary later??? - Now we write it 
                data=data)

            #Overwrite old block with modified block
            #fh = open(filePath, 'r+b')\
            print(modifiedBlock.state)
            fh = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'ab')
            #fh.seek(total)
            fh.write(struct.pack('20s d 16s I 11s I', modifiedBlock.prev_block_hash,
                modifiedBlock.time,
                modifiedBlock.caseID,
                modifiedBlock.itemID,
                modifiedBlock.state,
                modifiedBlock.data_length))
            fh.write(modifiedBlock.data)
            fh.close()

            #Update chain here !!!!

            if args.reason == 'RELEASED':
                print('Case: {}\nRemoved item: {}\n  Status: {}\n  Owner info: {}\n  Time of action: {}'.
                    format(uuid.UUID(bytes=modifiedBlock.caseID), args.item_ID, args.reason, args.owner, dt.fromtimestamp(modifiedBlock.time).isoformat()))

            else:
                print('Case: {}\nRemoved item: {}\n  Status: {}\n  Time of action: {}'.
                    format(uuid.UUID(bytes=modifiedBlock.caseID), args.item_ID, args.reason, dt.fromtimestamp(modifiedBlock.time).isoformat()))

        else:
            print('Block with that ID was not CHECKEDIN')
            sys.exit(404)
    except:
        print('5')
        sys.exit(404)

def logs(args):
    #try:
        update_info()
        #pdb.set_trace()
        printOnlyOneCaseId = False
        printOnlyOneItemId = False
        reverse = False if args.reverse == None else True                  #Determine if print them in reverse order
        numEntries = len(chain) if args.num == None else args.num        #Determine if print all block or only a specific number
        if numEntries < 0: sys.exit(1)
        if args.case_ID != None:                                           #If the user only wants one case ID
            printOnlyOneCaseId = True
            #specificCaseId = uuid.UUID(args.case_ID)
            specificCaseId = UUID(args.case_ID)
        else:
            printOnlyOneCaseId = False

        if args.item_ID != None:                                            #If the user only wants one item ID
            printOnlyOneItemId = True
            specificItemId = int(args.item_ID)
        else:
            printOnlyOneItemId = False

        chain.sort(key=lambda x: x.time, reverse=reverse)           #Sort it, reverse or bot
        i = 0
        #pdb.set_trace()
        if printOnlyOneCaseId and printOnlyOneItemId:
            for block in chain:
                if i < numEntries:
                    ba = bytearray((block.caseID).bytes)
                    ba.reverse()
                    s = ''.join(format(x, '02x') for x in ba)
                    s = UUID(s)                                      #Keep track of how many we have printed
                    if specificCaseId == s and specificItemId == block.itemID:
                        print('Case: {}\nItem: {}\nAction: {}\nTime: {}\n'.
                        format(s, block.itemID, block.state.decode("utf-8").rstrip('\x00'), dt.fromtimestamp(block.time).isoformat()+'Z'))
                i += 1
        if printOnlyOneCaseId:
            for block in chain:
                if i < numEntries:
                    ba = bytearray((block.caseID).bytes)
                    ba.reverse()
                    s = ''.join(format(x, '02x') for x in ba)
                    s = UUID(s)                                      #Keep track of how many we have printed
                    if specificCaseId == s:
                        print('Case: {}\nItem: {}\nAction: {}\nTime: {}\n'.
                        format(s, block.itemID, block.state.decode("utf-8").rstrip('\x00'), dt.fromtimestamp(block.time).isoformat()+'Z'))
                i += 1
        elif printOnlyOneItemId:
            for block in chain:
                if i < numEntries:
                    ba = bytearray((block.caseID).bytes)
                    ba.reverse()
                    s = ''.join(format(x, '02x') for x in ba)
                    s = UUID(s)                                      #Keep track of how many we have printed
                    if specificItemId == block.itemID:
                        print('Case: {}\nItem: {}\nAction: {}\nTime: {}\n'.
                        format(s, block.itemID, block.state.decode("utf-8").rstrip('\x00'), dt.fromtimestamp(block.time).isoformat()+'Z'))
                i += 1
        else:
            for block in chain:
                if i < numEntries:
                    ba = bytearray((block.caseID).bytes)
                    ba.reverse()
                    s = ''.join(format(x, '02x') for x in ba)
                    s = UUID(s)                                      #Keep track of how many we have printed
                    print('Case: {}\nItem: {}\nAction: {}\nTime: {}\n'.
                    format(s, block.itemID, block.state.decode("utf-8").rstrip('\x00'), dt.fromtimestamp(block.time).isoformat()+'Z'))
                i += 1
    #except:
        #sys.exit(1)

def verifyChain(args):
    global parent
    error = False               #Keep track if an error was found
    total = 0                   #Total number of blocks 
    errorCaseId = None          #Case id of block with error
    parentError = None          #Case id of block's parent 
    message = None              #Message explaining error

    newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
    readBytes = newFile.read(68)
    if len(readBytes) == 68:
        readBlock = struct.unpack('20s d 16s I 11s I', readBytes)
    else:
        print('Invalid initial block. Not enough information')
        sys.exit(404)
    if readBlock[0] != bytearray(20): error = True  #Check format of initial block
    case_id = uuid.UUID(bytes=readBlock[2])         #Convert case ID from bytes to string
    if case_id != uuid.UUID(int=0): error = True
    if readBlock[3] != 0: error = True
    if readBlock[4] != states['initial']: error = True
    if readBlock[5] != 14: error = True
    if newFile.read(readBlock[5]) != b'Initial block\x00': error = True
    
    if error: 
        errorCaseId = case_id
        error = False
    else:
        parentError = case_id
    total += 1
    readBytes = newFile.read(68)    #Read next block  
    parentBlock = {}                #Dictionaries to keep track of information read 
    stateDict = {}

    while len(readBytes) == 68:
        readBlock = struct.unpack('20s d 16s I 11s I', readBytes)   #Unpack next block
        parent = readBlock[0]
        itemId = readBlock[3]
        state = readBlock[4]
        data = newFile.read(readBlock[5])
        if not isinstance(parent, bytes): error = True              #Check format of information written in block 
        if not isinstance(readBlock[1], float): error = True
        if not isinstance(readBlock[2], bytes): error = True   
        if not isinstance(itemId, int): error = True
        if not isinstance(state, bytes): error = True
        if not isinstance(readBlock[5], int): error = True
        if not isinstance(data, bytes): error = True

        if parent in parentBlock.values():                  #Look for repeated parents
            for name, value in parentBlock.items():
                if parent == value and name != itemId:
                    error = True
                    message = 'Two blocks found with same parent'
        else:
            parentBlock[itemId] = parent
        
        if state not in states.values():                  #Check state of blocks 
            error = True
            message = 'Unknown state - ' + str(state)
        if itemId in stateDict:  
            if state == b'RELEASED\x00\x00\x00' and data == b'':        #If released owner data must be provided
                error = True
                message = 'No owner information'
            elif stateDict[itemId] == b'CHECKEDOUT\x00' and state == b'CHECKEDOUT\x00':         #Double checkout is not permited 
                error = True
                message = 'Error double checkout'
            elif stateDict[itemId] == b'CHECKEDIN\x00\x00' and state == b'CHECKEDIN\x00\x00':   #Double checkin is not permited
                error = True
                message = 'Double checkin'
            elif stateDict[itemId] == b'DISPOSED\x00\x00\x00' or stateDict[itemId] == b'DESTROYED\x00\x00' or stateDict[itemId] == b'RELEASED\x00\x00\x00':
                if state == b'CHECKEDIN\x00\x00' or state == b'CHECKEDOUT\x00':     #If removed if cannot be checkin
                    error = True
                    message = 'Error, checkin/checkout after remove'
                elif state == b'DISPOSED\x00\x00\x00' or state == b'DESTROYED\x00\x00' or state == b'RELEASED\x00\x00\x00':
                    error = True
                    message = 'Block removed twice'
            else:
                stateDict[itemId] = state
        elif state == b'DISPOSED\x00\x00\x00' or state == b'DESTROYED\x00\x00' or state == b'RELEASED\x00\x00\x00':
            message = 'Deleting a block that has not been added.'           #Item Id not in the dictionary and state is removed
            error = True
        else:
            stateDict[itemId] = state
       
        if error and errorCaseId is None:                   #Keep track of the first error
            errorCaseId = uuid.UUID(bytes=readBlock[2])
        elif not error and errorCaseId is None:
            parentError = uuid.UUID(bytes=readBlock[2])
        
        readBytes = newFile.read(68)        #Read next block
        total += 1                          #Keep track of number of blocks
    newFile.close()

    if errorCaseId != None:
        print('Transactions in blockchain: {}\nState of blockchain: ERROR\nBad block: {}\nParent Block: {}\n{}'.
            format(total, errorCaseId, parentError, message))
        sys.exit(1)
    else:
        print('Transactions in blockchain: {}\nState of blockchain: CLEAN'.format(total))

        
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

    checkout = subParser.add_parser('checkout')
    checkout.add_argument('-i', dest="item_ID", type=str, required=True)
    checkout.set_defaults(func=checkOut)

    checkin = subParser.add_parser('checkin')
    checkin.add_argument('-i', dest="item_ID", type=str, required=True)
    checkin.set_defaults(func=checkIn)

    remove = subParser.add_parser('remove')
    remove.add_argument('-i', dest="item_ID", type=str, required=True)
    remove.add_argument('--why', '-y', dest="reason", type=str, required=True)
    remove.add_argument('-o', dest="owner", type=str)
    remove.set_defaults(func=remove_)

    log = subParser.add_parser('log')
    log.add_argument('--reverse', '-r', dest='reverse', nargs='*', required=False)
    log.add_argument('-n', dest='num', type=int, required=False,)
    log.add_argument('-c', dest='case_ID', type=str, required=False)
    log.add_argument('-i', dest='item_ID', type=int, required=False)
    log.set_defaults(func=logs)

    verify = subParser.add_parser('verify')
    verify.set_defaults(func=verifyChain)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()