# Bitp0wn

```
This repo is a showcase of algorithms to get some fun with cryptography.
The scripts are not optimised and are only proof-of-concepts.  
```

### hacks

+ __[hacks/brute_force.py](https://github.com/mvrcrypto/bitp0wn/blob/master/hacks/brute_force.py)__ : You will find a simple bruteforce algorithm wich test every possibilities to retrieve a private key from the public key.

+ __[hacks/r_exploit.py](https://github.com/mvrcrypto/bitp0wn/blob/master/hacks/r_exploit.py)__ : This algorithm exploit a failure in signatures generation. If the same address use the same k in 2 differents signatures (_i.e_ same r-value), then you can recalculate the private key instantly.

+ __[hacks/substract_optim.py](https://github.com/mvrcrypto/bitp0wn/blob/master/hacks/substract_optim.py)__ : My best algorithm wich work in O(sqrt(2^n)) with n the number of bits of the private key. The idea is to generate once for all every public keys with with the private key being inferior to n/2. Then, we multiply them by (n/2) and we substract the public key. We found the private key when we found a key which already exist in the pre-generated base.

### miscellaneous

+ __[miscellaneous/playground.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/playground.py)__ : This file contains relations between values of differents signatures for an identical address.

+ __[miscellaneous/double.py](https://github.com/mvrcrypto/bitp0wn/blob/master/miscellaneous/double.py)__ : This file is more about finding an arithmetic relationship between 2 public keys on the curve. Most of formulaes are specific to _secp256k1_.

### networks

+ __[networks/shared-secret.py](https://github.com/mvrcrypto/bitp0wn/blob/master/networks/shared-secret.py)__ : Here you will find an algorithm to anonymously contact a node by constructing a route and a global shared secret key that only the initial sender and final receiver will share. The receiver won't know who is the sender and will send a signature to ensure the global key isn't compromised.
