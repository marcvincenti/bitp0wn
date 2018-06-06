#!/usr/bin/env python

import bitcoin

N = bitcoin.N

################################################################################
##############################   Initialization   ##############################
################################################################################

# Generate a pair of keys for Alice
a_sk = bitcoin.random_key()
a_pk = bitcoin.privtopub(a_sk)

# Generate a pair of keys for Bob
b_sk = bitcoin.random_key()
b_pk = bitcoin.privtopub(b_sk)

################################################################################
#################################   Signature   ################################
################################################################################

def ecdsa_raw_sign_one_to_one(msghash, sender_priv, receiver_pub):
    z = bitcoin.hash_to_int(msghash)
    k = bitcoin.deterministic_generate_k(msghash, sender_priv)
    r, y = bitcoin.fast_multiply(bitcoin.decode_pubkey(receiver_pub), k)
    s = bitcoin.inv(k, N) * (z + r*bitcoin.decode_privkey(sender_priv)) % N
    v, r, s = 27+((y % 2) ^ (0 if s * 2 < N else 1)), r, s if s * 2 < N else N - s
    return v, r, s

# Bob write a message
msg = "Hello Alice"
msg_hash = bitcoin.electrum_sig_hash(msg)

# Then, Bob sign the message for Alice
signature_for_alice = ecdsa_raw_sign_one_to_one(msg_hash, b_sk, a_pk)

################################################################################
###############################   Verification   ###############################
################################################################################

def ecdsa_raw_verify_one_to_one(msghash, vrs, sender_pub, receiver_priv):
    v, r, s = vrs
    w = bitcoin.inv(s, N)
    z = bitcoin.hash_to_int(msghash)
    u1, u2D = z*w % N, r*w*bitcoin.decode_privkey(receiver_priv) % N
    receiver_pub = bitcoin.privtopub(receiver_priv)
    u1Qr = bitcoin.fast_multiply(bitcoin.decode_pubkey(receiver_pub), u1)
    u2DQs = bitcoin.fast_multiply(bitcoin.decode_pubkey(sender_pub), u2D)
    x, y = bitcoin.fast_add(u1Qr, u2DQs)
    return bool(r == x and (r % N) and (s % N))

# Alice verify the signature provided by Bob works with her own private key
assert ecdsa_raw_verify_one_to_one(msg_hash, signature_for_alice, b_pk, a_sk)
