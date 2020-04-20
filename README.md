# CSE 469 - Blockchain Chain of Custody
Developers: 
  - Luis Claramunt (1212717114)
  - Jacob Babik 
  - Ben Downes

Chain of custody is the chronological documentation that records the sequence of custody, control, transfer, analysis, and disposition of physical or electronic evidence.

# Installation
In order to get the executable `bchoc` you will need the Makefile for this project. Open your terminal and simply execute the command
`make`
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
It is important to understant that most of the commands write a new block into a blockchain file with the current state of the block. The program searches for the environment variable `BCHOC_FILE_PATH` when looking for this blockchain file. 

# Commands
The program runs the following commands. Note that **[ ]** represents optional 
```Commands
bchoc add -c case_id -i item_id [-i item_id ...]
bchoc checkout -i item_id
bchoc checkin -i item_id
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
bchoc remove -i item_id -y reason [-o owner]
bchoc init
bchoc verify
```
Next, an explanation of each command will be provied

### init
Initialize the chain of custody and checks the initial block.<br>Example
```init example
$ bchoc init
Blockchain file not found. Created INITIAL block.
```
### add
Add new evidence to the chain of custody (block to the blockchain). You may add more than one. It is necessary to provide a case-id and a unique item-id for each them. It will return an error if a block with the given item-id is already in the blockchain. These new blocks will be given a state of `CHECKEDIN`. It will initialize a blockchain if it cannot find one.<br>Example: 
```Add Example
$ bchoc add -c 65cc391d-6568-4dcc-a3f1-86a2f04140f3 -i 987654321 -i 123456789
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Added item: 987654321
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:13:07.820445Z
Added item: 123456789
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:13:07.820445Z
 ```
### checkout
Add new block to the blockchain with the given item-id (`-i`) and `CHECKOUT` state. It may only be performed on evidence items that have already been added to the blockchain and currently have `CHECKEDIN` state.<br>Example:
```Checkout Example
$ bchoc checkout -i 987654321
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Checked out item: 987654321
  Status: CHECKEDOUT
  Time of action: 2019-01-22T03:22:04.220451Z
  ```
 ### Checkin
Add new block to the blockchain with the given item-id (`-i`) and `CHECKEDIN` state. Checkin actions may only be performed on evidence items that have already been added to the blockchain<br>Example:
```Checkin Example
$ bchoc checkin -i 987654321
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Checked in item: 987654321
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:24:25.729411Z
  ```
 ### log
Display the blockchain entries. The default setting is to show the oldest first, but it could be the other way around (`-r`) as in the example provided. You may also specify the number of blocks to be displayed (`-n`) and a specific block (`-i`).<br>Example:
  ```log Example
  $ bchoc log -r -n 2 -i 987654321
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Item: 987654321
Action: CHECKEDIN
Time: 2019-01-22T03:24:25.729411Z

Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Item: 987654321
Action: CHECKEDOUT
Time: 2019-01-22T03:22:04.220451Z
```
### remove
No further actions can be performed on the block with the specific id (`-i`). The block must have a state of `CHECKEDIN`. You may specify the reason why you are removing the evidence/block (`-y`). Valid reasons are: `DISPOSED`, `DESTROYED`, and `RELEASED`. If you choose `RELEASED` you must also provide owner information (`-o`) which does not have any requirements.
```remove Example
$ bchoc remove -i 987654321 -y RELEASED -o "John Doe, 123 Cherry Ln, Pleasant, AZ 84848, 480-XXX-4321"
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Removed item: 987654321
  Status: RELEASED
  Owner info: John Doe, 123 Cherry Ln, Pleasant, AZ 84848, 480-XXX-4321
  Time of action: 2019-01-22T03:24:25.729411Z
  ```
### verify
Validate Chain of Custody's content.
```verify Examplee
$ bchoc verify
Transactions in blockchain: 6
State of blockchain: CLEAN
```
