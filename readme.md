# Bitp0wn

```
This repo is a showcase of algorithms to get some fun with cryptography.
The scripts are not optimised and are only proof-of-concepts.  
```

### hacks

+ __[hacks/brute_force.py](https://github.com/mvrcrypto/bitp0wn/blob/master/hacks/brute_force.py)__ : You will find a simple bruteforce algorithm wich test every possibilities to retrieve a private key from the public key.

+ __[hacks/bsgs.py](https://github.com/mvrcrypto/bitp0wn/blob/master/hacks/bsgs.py)__ : The Baby-step Giant-step algorithm, it has order of 2^(n/2) time complexity and space complexity.

### miscellaneous

+ __[miscellaneous/double.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/double.py)__ : This file is more about finding an arithmetic relationship between 2 public keys on the curve. Most of formulaes are specific to _secp256k1_.

+ __[miscellaneous/forgery.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/forgery.py)__ : In this file, we try to establish the relation between a generated signature (see __fake_sig.py__) and a new one with the same r value.

+ __[miscellaneous/playground.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/playground.py)__ : This file contains relations between values of differents signatures for an identical address.

+ __[miscellaneous/tiny-curve.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/tiny-curve.py)__ : This script let you generate your own elliptic curves (not secure, never use the curves in production). This will be useful to test some of our algorithms on smaller curves.

### networks

+ __[networks/shared-secret.py](https://github.com/mvrcrypto/bitp0wn/blob/master/networks/shared-secret.py)__ : Here you will find an algorithm to anonymously contact a node by constructing a route and a global shared secret key that only the initial sender and final receiver will share. The receiver won't know who is the sender and will send a signature to ensure the global key isn't compromised. Also, the encryption key is computed with a global shared key between all participants, but only the 2 communicating nodes have the key.

### signatures

+ __[signatures/fake_sig.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/fake_sig.py)__ : In this script, we show why hashing the message in ecdsa is important. Because without it, you can generate plenty of signatures that can be verified with Satoshi signature.

+ __[signatures/r_exploit_ecdsa.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/r_exploit_ecdsa.py)__ : This algorithm exploit a failure in signatures generation. If the same address use the same k in 2 differents signatures (_i.e_ same r-value), then you can recalculate the private key instantly.

+ __[signatures/r_exploit_schnorr.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/r_exploit_schnorr.py)__ : Same as precedent exploit but for schnorr signatures instead of ecdsa signatures.

+ __[signatures/secret-sign.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/secret-sign.py)__ : A proof-of-concept to build a signature for a particular public key. Only the owner of this public key will be able to assert that the signature is correct.
