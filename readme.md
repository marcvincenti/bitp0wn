# Bitp0wn

```
This repo is a showcase of algorithms to get some fun with bitcoin cryptography.
The scripts are not optimised and are only proof-of-concepts (not suited for production).
```

### keys

+ __[keys/brute_force.py](https://github.com/mvrcrypto/bitp0wn/blob/master/keys/brute_force.py)__ : You will find a simple bruteforce algorithm wich test every possibilities to retrieve a private key from the public key.

+ __[keys/bsgs.py](https://github.com/mvrcrypto/bitp0wn/blob/master/keys/bsgs.py)__ : The Baby-step Giant-step algorithm, it has order of 2^(n/2) time complexity and space complexity.

+ __[keys/pollard_rho.py](https://github.com/mvrcrypto/bitp0wn/blob/master/keys/pollard_rho.py)__ : The Pollard Rho algorithm, it has order of 2^(n/2) time complexity but is slower than bsgs in practice. However, this algorithm has a constant space complexity.

### miscellaneous

+ __[miscellaneous/double.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/double.py)__ : This file is more about finding an arithmetic relationship between 2 public keys on the curve. Most of formulaes are specific to _secp256k1_.

+ __[miscellaneous/playground.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/playground.py)__ : This file contains relations between values of differents signatures for an identical address.

+ __[miscellaneous/secret-sign.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/secret-sign.py)__ : A proof-of-concept to build a signature for a particular public key. Only the owner of this public key will be able to assert that the signature is correct.

+ __[miscellaneous/shamir-shared-secret.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/shamir-shared-secret.py)__ : Shamir Shared Secret Scheme to distribute a secret to n entities wich can be recovered with k < n shares.

+ __[miscellaneous/tiny-curve.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/tiny-curve.py)__ : This script let you generate your own elliptic curves (not secure, never use the curves in production). This will be useful to test some of our algorithms on smaller curves.

### signatures

+ __[signatures/fake_sig.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/fake_sig.py)__ : In this script, we show why hashing the message in ecdsa is important. Because without it, you can generate plenty of signatures that can be verified with the public key of your choice.

+ __[signatures/r_exploit_ecdsa.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/r_exploit_ecdsa.py)__ : This algorithm exploit a failure in signatures generation. If the same address use the same k in 2 differents signatures (_i.e_ same r-value), then you can recalculate the private key instantly.

+ __[signatures/r_exploit_schnorr.py](https://github.com/mvrcrypto/bitp0wn/blob/master/signatures/r_exploit_schnorr.py)__ : Same as precedent exploit but for schnorr signatures instead of ecdsa signatures.
