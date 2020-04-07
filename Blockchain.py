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
from uuid import UUID
#Convert from bytes to UUID uuid.UUID(bytes=b'\xf0\xe2\xfc\xe7\xf6\xdcL\xe3\x85\xb8\x12\x00u\x82\x1c\x0b')
Block = collections.namedtuple('Block', ['prev_block_hash', 'time', 'caseID', 'itemID', 'state', 'data_length', 'data'])
states = {'initial': b'INITIAL\0\0\0\0', 'checkin': b'CHECKEDIN\0\0', 'checkout': b'CHECKOUT\0', 'disposed': b'DISPOSED\0\0\0', 'destroyed':b'DESTROYED\0\0', 'released': b'RELEASED\0\0\0'}
chain = []

def update_info():
    newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'rb')
    #newFile = open('BCHOC_FILE_PATH', 'rb')
    readBytes = newFile.read(68)
    readBlock = struct.unpack('20s d 16s I 11s I', readBytes)
    hashBlock = readBlock[0]
    assert hashBlock == bytearray(20)
    #Add time

    case_id = uuid.UUID(bytes=readBlock[2])         #Convert case ID from bytes to string
    assert case_id == uuid.UUID(int=0)

    item_id = readBlock[3]
    assert item_id == 0

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
    while len(readBytes) == 68:
        hashBlock = readBlock[0]
        assert isinstance(hashBlock, bytes)
        #Add time

        case_id = uuid.UUID(bytes=readBlock[2])         #Convert case ID from bytes to string
        assert isinstance(case_id, uuid.UUID)

        item_id = readBlock[3]
        assert isinstance(item_id, int)

        state = readBlock[4]
        assert isinstance(state, bytes)

        length = readBlock[5]
        assert isinstance(length, int)

        readBlock = struct.unpack('20s d 16s I 11s I', readBytes)
        data = newFile.read(readBlock[5]).decode()
        block = Block(prev_block_hash=readBlock[0],
            time=readBlock[1],
            caseID=case_id,
            itemID=readBlock[3],
            state=readBlock[4],
            data_length=readBlock[5], data=data)
        chain.append(block)
        readBytes = newFile.read(68)
    newFile.close()


def initialize(args)  :
    try:
        update_info()
        print('Blockchain file found with INITIAL block.')
    except:
        newFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'wb')
        initialBlock = Block(bytearray(20),
            0,
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

def getBlockCaseId(case_ID):
    uuid_case_id = uuid.UUID(case_ID)        #Convert from string to UUID for comparison
    for block in chain:
        if block.caseID == uuid_case_id:
            return block
    return False                        #Return false if block is never found

def hash(block):
    stringBlock = ""
    for item in block:
        stringBlock += str(item)
    return hashlib.sha1(stringBlock.encode()).digest()

def addBlock(args):
    try:
        update_info()                   #Get info in the file into the chain list
        previousBlock = getBlockCaseId(args.case_ID)

        if previousBlock is False:
            print('Block under such case ID does not exists')
        else:
            addFile = open(os.environ.get('BCHOC_FILE_PATH', 'BCHOC_FILE_PATH'), 'wb')
            #addFile = open('BCHOC_FILE_PATH', 'wb')
            print('Case: {}'.format(args.case_ID))
            for id in args.item_ID:
                newBlock = Block(prev_block_hash=hash(previousBlock),
                    time=0,
                    caseID=uuid.uuid4(),
                    itemID=int(id),
                    state=states['checkin'],
                    data_length=0,
                    data=b'')
                chain.append(newBlock)
                addFile.write(struct.pack('20s d 16s I 11s I', newBlock.prev_block_hash,
                    newBlock.time,
                    newBlock.caseID.bytes,
                    newBlock.itemID,
                    newBlock.state,
                    newBlock.data_length))
                addFile.write(newBlock.data)
                print('Added item: {}\n  Status: {}\n  Time of action: {}'.
                    format(id, newBlock.state.decode(), newBlock.time))
            addFile.close()
    except:
        sys.exit(404)


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

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 14d6a4570025daa8a9b8c93a103095d6fd123f40
