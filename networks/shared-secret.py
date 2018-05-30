#!/usr/bin/env python

import bitcoin
import pyaes

NB_RELAY_NODES = 2

def AES_encrypt(msg, key):
    aes = pyaes.AESModeOfOperationCTR(key[2:34])
    return aes.encrypt(str(msg))

def AES_decrypt(msg, key):
    aes = pyaes.AESModeOfOperationCTR(key[2:34])
    return aes.decrypt(msg)

################################################################################
##############################   Initialization   ##############################
################################################################################

# Generate a pair of keys for the user
user_sk = bitcoin.random_key()
user_pk = bitcoin.privtopub(user_sk)

# Generate a pair of keys for nodes
assert NB_RELAY_NODES > 0
relayNodes = list()
for i in range(NB_RELAY_NODES):
    secret = bitcoin.random_key()
    relayNodes.append({
        'secret': secret,
        'public': bitcoin.privtopub(secret)
    })
exitNode_sk = bitcoin.random_key()
exitNode_pk = bitcoin.privtopub(exitNode_sk)

################################################################################
############################   Connecting Process   ############################
################################################################################

# The user ask for a connection to relayNode1, wich ask to next node... until exitNode
u_shared = user_pk
for i in range(NB_RELAY_NODES):
    u_shared = bitcoin.multiply(u_shared, relayNodes[i]['secret'])

# Then exitNode calculate and sign the global shared secret
global_shared = bitcoin.multiply(u_shared, exitNode_sk)
global_shared_signature = bitcoin.ecdsa_sign(global_shared, exitNode_sk)

# Then, the exitNode accept the connection by sending back the signature
# The relayNodes now calculate new shared with exitNode
e_shared = exitNode_pk
for i in range(NB_RELAY_NODES)[::-1]:
    e_shared = bitcoin.multiply(e_shared, relayNodes[i]['secret'])

# User can now calculate global shared key and test if exitNode has the same
assert exitNode_pk == bitcoin.ecdsa_recover(bitcoin.multiply(e_shared, user_sk), global_shared_signature)

################################################################################
##########################   Communication Process   ###########################
################################################################################

# The user have some data that he can encrypt with global shared key
user_msg = 'A random user message.'
encrypted_msg = AES_encrypt(user_msg, global_shared)

# The user send it to relayNodes, wich will relay it to exitNode
# Now, the exitNode can read the data without knowing the user
exit_msg = AES_decrypt(encrypted_msg, global_shared)

assert exit_msg == user_msg
