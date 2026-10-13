"""Tests de primalité (naïf, Fermat, Miller-Rabin) et nombres de Carmichael."""
import random
from math import isqrt

from prime_testing.arithmetic import my_expo_mod, my_gcd


def first_test(N):
    """
    int -> boolean
    test naiif de primalité
    complexité en O(sqrt(n))
    """
    if N < 2:
        return False
    for i in range(2, isqrt(N)+1):
        if N % i == 0:
            return False
    return True


#critére korselt
def isCarmichael_facteurs(n, facteurs):
    """
    int*list->boolean
    tester si n est un nombre de carmichael, etant donné ses facteurs
    """
    for facteur in facteurs:
        # pas facteur premier carré
        if n % (facteur**2) == 0:
            return False
        if (n-1) % (facteur-1) != 0:
            return False
    # pass le test
    return True


def isCarmichael(n):
    """
    int->boolean
    tester si n est un nombre de carmichael, sans connaitre ses facteurs
    """
    n_divisors = 0
    for i in range(2, n):
        # (i premier avec n => i**(n-1) = 1[n])
        gcd = my_gcd(i, n)
        if (gcd == 1) and (my_expo_mod(i, n-1, n) != 1):
            return False

        if n % i == 0:
            n_divisors += 1

    if n_divisors == 0:
        # n est premier
        return False

    return True


def gen_carmichael(N=1e5):
    """
    int->list
    liste des nombres de carmichael inferieurs à N
    """
    acc = []
    for i in range(int(N)):
        if isCarmichael(i):
            acc.append(i)

    return acc


def gen_carmichael3(N=1e5):
    """
    int->int
    un nombre de carmichael, produit de 3 premiers distincts inferieurs à N
    """
    premiers = [i for i in range(3, int(N), 2) if first_test(i)]
    nb_facteur = 3

    while True:
        acc = random.sample(premiers, nb_facteur)
        n = 1
        for a in acc:
            n *= a
        if isCarmichael_facteurs(n, acc):
            return n


def gen_carmichael_3_list(N=1e5, n_elements=10):
    """
    int*int->list
    """
    premiers = [i for i in range(3, int(N), 2) if first_test(i)]
    nb_facteur = 3
    T = []
    while len(T) < n_elements:
        acc = random.sample(premiers, nb_facteur)

        n = 1
        for a in acc:
            n *= a
        if isCarmichael_facteurs(n, acc):
            T.append(n)

    return T


def test_fermat(n, a=None):
    """
    n un entier impair

    Retourne vrai si premier possible
    faux si composé

    """
    if n < 2:
        return False
    if n == 2:
        return True

    if a is None:
        a = random.randrange(2, n)

    return my_expo_mod(a, n-1, n) == 1


def test_miller_rabin(n, T=10):
    """
    int*int->boolean
    n = 1 + 2**h * m
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    h = 0
    m = n-1
    while m % 2 == 0:
        m = m // 2
        h += 1

    for i in range(T):
        a = random.randrange(2, n-1)
        b = my_expo_mod(a, m, n)

        if b == 1 or b == (n-1):
            continue

        # au plus h-1 carrés : b parcourt a^(2m), a^(4m), ..., a^((n-1)/2)
        for j in range(1, h):
            b = my_expo_mod(b, 2, n)
            if b == (n-1):
                break
            if b == 1:
                # racine carrée de 1 autre que 1 et -1
                return False
        else:
            return False

    return True
