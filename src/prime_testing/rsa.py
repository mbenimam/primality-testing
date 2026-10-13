"""RSA scolaire : génération de clés, encodage et décodage caractère par caractère."""
import random

from prime_testing.arithmetic import my_expo_mod, my_inverse_bezout
from prime_testing.primality import test_miller_rabin


def gen_rsa(t):
    """
    int: longeur en bits (doit être supérieur a 2)
    return: p, q, n avec p et q premiers distincts de t bits
    """

    inf = 1 << (t-1)

    while True:
        p = inf + random.getrandbits(t-1)
        if test_miller_rabin(p):
            break
    while True:
        q = inf + random.getrandbits(t-1)
        if test_miller_rabin(q) and q != p:
            break

    return p, q, p*q


def RSA(t):
    """
    return public_key, private_key
    """
    p, q, n = gen_rsa(t)

    # phi (nombre de nombres premier avec n, < n)
    phi = (p-1)*(q-1)

    while True:
        e = 2 + random.getrandbits(phi.bit_length()) % (phi-3)
        d = my_inverse_bezout(e, phi)
        if d is not None:
            break

    return (e, n), (d, n)


def encode(m, public_key):
    """
    (e, n)
    """

    return [my_expo_mod(ord(c), *public_key) for c in m]


def decode(m, private_key):
    """
    (d, n)
    """
    return ''.join([chr(my_expo_mod(c, *private_key)) for c in m])
