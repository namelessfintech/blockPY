from functools import reduce
import hashlib as  hl
from collections import OrderedDict
from hash_util import *

# Initializing our (empty) blockchain list
# set the global mining reward
MINING_REWARD = 10

""" Step:  intializing my blockchain list """
# the genisis block is the founding block of my blockchain
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
# initiate my blockchain and add the genisis block
blockchain = [genesis_block]

# create a variable to serve as a queue for unmined
open_transactions = []

# establish the ownership of the blockchain
owner = 'Michael'

# create an exisiting loop for all transaction participants in the blockchain
participants = {'Michael'}

def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00' #here Is where I can get fancy with my condition to check for a valid hash. Use academic research to guide me.


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0 
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def get_balance(participant):
    """ Create a function to retrieve a users balance """
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)

    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    """ Replaced by one liner below using lambda and reduce """
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > tx_sum + 0 else 0, tx_sender ,0)


    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    
    """ Replaced by another one liner below using lambda and reduce again """
    amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_received += tx[0]

    return amount_recieved - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """ Verify that an sender has suffiecient funds """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The sender of the funds.
        :recipient: The recipient of the funds.
        :amount: The amount of funds sent with the transaction (default = 1.0)
    """
    # store the individual transction in a dictionary, update uses an orderedDict to prevent fault
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = OrderedDict([('sender', sender),("recipient", recipient),('amount', amount)])
  
    if verify_transaction(transaction):
        # add new transaction details to open transactions 
        open_transactions.append(transaction)
        # update the participants set with all exsting tranactions with existing participants
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    """ Step: Mining Code below """
    
    # grab the the last hashed block
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)  # pass in the last block to hash it and set to be passed to newly mined block
    # print(hash_block)
    
    proof = proof_of_work()

    # design a new transaction to capture the mining reward per block
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }

    reward_transaction = OrderedDict([('sender', 'MINING'),('recipient', owner), ('amount', MINING_REWARD)])

    # create a shallow copy of the open transactions
    copied_transactions = open_transactions[:]

    # append the mining reward transaction to all current open txns
    copied_transactions.append(reward_transaction)

    # create the new block
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    #append new block to the blockchain
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input




def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print( " ")
        print(block)
        print(" ")
    else:
        print('-' * 20)


def verify_chain():
    """ Verify the current blockchain and return True if it's valid, False otherwise."""
    # loop through each block and compare each available block
    for (index, block) in enumerate(blockchain): # Generate a destructured tuple with enumerate function
        if index == 0:
            continue # skip the validation of the genesis block
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False

        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print("Proof of work is invalid")
            return False

    return True # return true to continue process if all blocks are valid

def verify_transactions():
    # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     elif verify_transaction != True:
    #         print("This block is broken")
    #     else:
    #         is_valid = False
    # return is_valid
    """ One line implementation to validate that all transactions are true """
    return all([verify_transaction(tx) for tx in open_transactions])


# dont forget to add the node list: 


waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    """ Create an infite loop to run the blockchain cli """
    # print the user options
    print(" ------------------------------------- ")
    print(" ")
    print('Please choose an option number?')
    print(" ")
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    print(" ")
    print(" ------------------------------------- ")
    print(" ")


    # save user input
    user_choice = get_user_choice()

    # Create a conditions to service the user input
    if user_choice == '1':
        tx_data = get_transaction_value() 
        recipient, amount = tx_data # I can destructure or unpack a tuple as such
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount): # add transactiont to open transactions
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':  # output existing blocks
        print_blockchain_elements()
    elif user_choice == '4': # output all existing participants
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == 'h': # change the blockchain manually to test the validation methods of hash n-1 being exact copy in hash N
        # Make sure that you don't try to "hack" the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Michael', 'amount': 100.0}]
            }
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print(" ------------------------------------------------ ")
    print(" ")
    print('Current Balance of {}\'s Account:{:6.2f}'.format(owner, get_balance("Michael")))
    print(" ")
else:
    print('User left!')


print('Done!')

"""  Pretty soon I will have built and understood a full block chain"""
