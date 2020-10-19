import time
import random

pow2bits = 30  # bit range for generating key

# secp256k1
A_curve = 0
B_curve = 7
modulo = 115792089237316195423570985008687907853269984665640564039457584007908834671663
order = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


Gp = Point(Gx, Gy)
Zp = Point(0, 0)


# inverting
def invert(b, p=modulo):
    u, v = b % p, p
    x1, x2 = 1, 0
    while u != 1:
        # q = v//u
        # r = v-q*u
        q, r = divmod(v, u)
        x = x2 - q * x1
        v = u
        u = r
        x2 = x1
        x1 = x
    return x1 % p


# Addition for public key
def addition_key(A, B, p=modulo):
    R = Point()
    dx = B.x - A.x
    dy = B.y - A.y
    c = dy * invert(dx, p) % p
    R.x = (c * c - A.x - B.x) % p
    R.y = (c * (A.x - R.x) - A.y) % p
    return R


# Doubling for public key
def doubling_key(A, p=modulo):
    R = Point()
    c1 = A.x * A.x * invert(A.y + A.y, p)
    c = (c1 + c1 + c1) % p
    R.x = (c * c - A.x - A.x) % p
    R.y = (c * (A.x - R.x) - A.y) % p
    return R


# Multiplication for public key
def multiplication_key(k, A=Gp, p=modulo):
    if k == 0:
        return Zp
    elif k == 1:
        return A
    elif k % 2 == 0:
        return multiplication_key(k // 2, doubling_key(A, p), p)
    else:
        return addition_key(A, multiplication_key((k - 1) // 2, doubling_key(A, p), p), p)


# calculation Y from X if pubkey is compressed
def getX2Y(X, y_parity, p=modulo):
    Y = 3
    tmp = 1
    while Y:
        if Y & 1:
            tmp = tmp * X % p
        Y >>= 1
        X = X * X % p

    X = (tmp + 7) % p

    Y = (p + 1) // 4
    tmp = 1
    while Y:
        if Y & 1:
            tmp = tmp * X % p
        Y >>= 1
        X = X * X % p

    Y = tmp

    if Y % 2 != y_parity:
        Y = -Y % p

    return Y


# get hex pubkey from int prvkey
def getPubkey(new_prvkey, flag_compress):
    Ptmp = multiplication_key(new_prvkey)
    Xcoord = Ptmp.x
    Ycoord = Ptmp.y

    if flag_compress:
        if (Ycoord % 2) == 0:
            new_pubkey = '02%064x' % int(hex(Xcoord)[2:66], 16)
        else:
            new_pubkey = '03%064x' % int(hex(Xcoord)[2:66], 16)
    else:
        new_pubkey = '04%064x%064x' % (int(hex(Xcoord)[2:66], 16), int(hex(Ycoord)[2:66], 16))

    return new_pubkey


# get pow2Jmax
def getPow2Jmax(optimalmeanjumpsize):
    sumjumpsize = 0

    for i in range(1, 256):

        sumjumpsize += 2 ** (i - 1)

        now_meanjumpsize = int(round(1.0 * (sumjumpsize + 0) / i))
        next_meanjumpsize = int(round(1.0 * (sumjumpsize + 2 ** i) / i))

        # if meanjumpsize >= optimalmeanjumpsize:
        if optimalmeanjumpsize - now_meanjumpsize <= next_meanjumpsize - optimalmeanjumpsize:
            return i


# Checks whether the given point lies on the elliptic curve
def is_on_curve(Xcoord, Ycoord, p=modulo):
    return ((Ycoord * Ycoord) - (Xcoord * Xcoord * Xcoord) - (A_curve * Xcoord) - B_curve) % p == 0


# Kangaroo algorithm
def Kangaroo():
    # mean jumpsize
    # by Pollard ".. The best choice of m (mean jump size) is w^(1/2)/2 .."
    # midJsize = (Wsqrt//2)+1
    midJsize = int(round(1.0 * Wsqrt / 2))

    pow2Jmax = getPow2Jmax(midJsize)
    sizeJmax = 2 ** pow2Jmax

    # discriminator for filter added new distinguished points (ram economy)
    pow2dp = (pow2W // 2) - 2  #
    DPmodule = 2 ** pow2dp

    # generate random start points

    # Tame
    # dT = (3<<(pow2bits-2)) + random.randint(1,(2**(pow2bits-1)))
    dT = M  # by Pollard

    if not (dT % 2):
        dT += 1  # T odd recommended

    Tp = multiplication_key(dT)

    # Wild
    # dW = random.randint(1, (1<<(pow2bits-1)))
    dW = 1  # by Pollard

    Wp = addition_key(wildRoot, multiplication_key(dW))

    # DTp/DWp - points, distinguished of Tp/Wp
    DTp, DWp = dict(), dict()  # dict is hashtable of python, provides uniqueness distinguished points

    t0 = time.time()
    n_jump = 0
    prvkey = False

    # main loop
    while True:

        # Tame
        n_jump += 1

        # Xcoord
        Xcoord = Tp.x

        pw = Xcoord % pow2Jmax
        pw = int(pw)
        nowjumpsize = 1 << pw

        # check, is it distinguished point?
        if Xcoord % DPmodule == 0:

            # add new distinguished point
            DTp[Xcoord] = dT

            # compare distinguished points, Tame & Wild
            compare = list(set(DTp) & set(DWp))
            if len(compare) > 0:
                dDT = DTp[compare[0]]
                dDW = DWp[compare[0]]
                if dDT > dDW:
                    prvkey = dDT - dDW
                elif dDW > dDT:
                    prvkey = dDW - dDT
                else:
                    print("\rError dDW == dDT !!! (0x%x)" % dDW)
                    exit(-1)

        if prvkey:
            break

        dT += nowjumpsize

        Tp = addition_key(Tp, Sp[pw])

        if prvkey:
            break

        # Wild
        n_jump += 1

        # Xcoord
        Xcoord = Wp.x

        pw = Xcoord % pow2Jmax
        pw = int(pw)
        nowjumpsize = 1 << pw

        # add new distinguished point
        if Xcoord % DPmodule == 0:

            # add new distinguished point
            DWp[Xcoord] = dW

            # compare distinguished points, Tame & Wild
            compare = list(set(DTp) & set(DWp))
            if len(compare) > 0:
                dDT = DTp[compare[0]]
                dDW = DWp[compare[0]]
                if dDT > dDW:
                    prvkey = dDT - dDW
                elif dDW > dDT:
                    prvkey = dDW - dDT
                else:
                    print("\rError dDW == dDT !!! (0x%x)" % dDW)
                    exit(-1)

        if prvkey:
            break

        dW += nowjumpsize

        Wp = addition_key(Wp, Sp[pw])

        if prvkey:
            break

    return prvkey, n_jump, (time.time() - t0), len(DTp), len(DWp)


if __name__ == '__main__':

    prvkey0 = False
    pubkey0 = False

    bitMin = 8
    bitMax = 120

    L = 2 ** (pow2bits - 1)
    U = 2 ** pow2bits

    W = U - L
    Wsqrt = W ** 0.5
    Wsqrt = int(Wsqrt)

    M = L + (W // 2)

    pow2L = pow2bits - 1
    pow2U = pow2bits
    pow2W = pow2bits - 1

    Sp = [Gp]
    for k in range(255):
        Sp.append(doubling_key(Sp[k]))

    prvkey0 = random.randint(L, U)
    pubkey0 = getPubkey(prvkey0, True)  # compressed
    print('Public key randomly generated in range 2^%s..2^%s' % (pow2L, pow2U))

    # check format pubkey
    X = 0
    Y = 0
    if len(pubkey0) == 130:
        X = int(pubkey0[2:66], 16)
        Y = int(pubkey0[66:], 16)
        flag_compress = False
    elif len(pubkey0) == 66:
        X = int(pubkey0[2:66], 16)
        Y = getX2Y(X, int(pubkey0[:2]) - 2)
        flag_compress = True
    else:
        print("Public key is invalid!")

    if not is_on_curve(X, Y):
        print("The given point not lies on the elliptic curve!")

    # wild root
    wildRoot = Point(X, Y)

    # call KANGAROOS()
    prvkey, runjump, runtime, lenT, lenW = Kangaroo()

    print('')
    print('Private key :  0x%064x' % prvkey)
