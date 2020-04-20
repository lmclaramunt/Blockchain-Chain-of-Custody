# CSE 469 - Blockchain Chain of Custody
Developers: 
  #Luis Claramunt
  Jacob Babik 
  Ben Downes

Chain of custody is the chronological documentation that records the sequence of custody, control, transfer, analysis, and disposition of physical or electronic evidence.

# Installation
In order to get the executable ```bchoc``` you will need the Makefile for this project. Open your terminal and simply execute the command
```make```
# Blocks
Before describing the commands that are available is important to understand what is the structure of the blocks that can be stored in the blockchain. 
Each block has:
```Blocks
Hash of parent block - Using SHA-1 Hash
Timestamp - indicating when it was written
Case ID - UUID format
Evidence ID - 4 byte integer
State - {INITIAL, CHECKEDIN, CHECKEDOUT, DISPOSED, DESTROYED, RELEASED}
Data Length - 4 byte integer
Data - Free form of text
```
It is important to understant that most of the commands write a new block into a blockchain file with the current state of the block. The program always searches for the environment variable ```BCHOC_FILE_PATH``` when looking for this blockchain file. 

# Commands
The program runs the following commands. Note that [ ] represents optional 
```Commands
bchoc add -c case_id -i item_id [-i item_id ...]
bchoc checkout -i item_id
bchoc checkin -i item_id
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
bchoc remove -i item_id -y reason [-o owner]
bchoc init
bchoc verify
```
