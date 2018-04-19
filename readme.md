# Bitp0wn

```
This repo is a showcase of alogrithms to get a private key from a public key on ecdsa.
The scripts are not optimised and are only proof-of-concepts.  
```

You can find a little desription of each files below :

+ __[brute_force.py](https://github.com/mvrcrypto/bitp0wn/blob/master/brute_force.py)__ : You will find a simple brute algorithm wich test every possibilities.

+ __[birthday.py](https://github.com/mvrcrypto/bitp0wn/blob/master/birthday.py)__ : This algorithm try to generate new signatures from a prechosen address. This is based on [birthday attack](https://en.wikipedia.org/wiki/Birthday_attack).

+ __[local_maximum.py](https://github.com/mvrcrypto/bitp0wn/blob/master/local_maximum.py)__ : Worst heuristic, try to find a local maximum with a bad fitness function.

+ __[genetic.py](https://github.com/mvrcrypto/bitp0wn/blob/master/genetic.py)__ : Here we try to crack private key using a metaheuristic (also with a bad fitness function): [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm). This is much better than __local_maximum.py__.

+ __[r_exploit.py](https://github.com/mvrcrypto/bitp0wn/blob/master/r_exploit.py)__ : This algorithm exploit a failure in signatures generation. If the same address use the same k in 2 differents signatures (_i.e_ same r-value), then you can retrieve the private key instantly.

+ __[substract_optim.py](https://github.com/mvrcrypto/bitp0wn/blob/master/substract_optim.py)__ : My best algorithm wich work in O(2^(n/2)) or O(sqrt(2^n)) with n the number of bits of the private key. The idea is to generate once for all every public keys with with the private key being inferior to n/2. Then, we multiply them by (n/2) and we substract the public key. We found the private key when we found a key present in the pre-generated base.

Then you can find 2 other files :

+ __[playground.py](https://github.com/mvrcrypto/bitp0wn/blob/master/others/playground.py)__ : This file contains relations between values of differents signatures for an identical address.

+ __[double.py](https://github.com/mvrcrypto/bitp0wn/blob/master/others/double.py)__ : This file is more about finding relationship between 2 public keys on the curve. Most of formulaes are specific to _secp256k1_.
