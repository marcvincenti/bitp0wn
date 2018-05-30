#!/usr/bin/env python

import bitcoin

N = 8193
# If you want fewer values, you can use 2 and you will get every powers of 2
MIN = 3

def lenY(p):
    y_set = set()
    for x in range(p):
        y = pow(int(x*x*x+7), int((p+1)//4), int(p))
        y_set.add(y)
    return len(y_set)

best_p = 0
best_len = N
cpt = 0
for p in range(N):
    _len = lenY(p)
    if _len <= best_len and _len >= MIN:
        if _len < best_len:
            best_len = _len
            cpt = 1
        else:
            cpt += 1
        best_p = p

print "We have {0} values using p = {1}\n(Occurences: {2})".format(best_len, best_p, cpt)
