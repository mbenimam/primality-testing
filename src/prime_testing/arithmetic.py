"""Arithmétique dans Z/nZ : pgcd, Bézout, inverse et exponentiation modulaire."""


def my_gcd(a, b):
    """
    int*int -> int
    """
    a, b = max(a, b), min(a, b)
    while b != 0:
        tempo = b
        b = a % b
        a = tempo
    return a


def my_gcd_etendu(a, b):
    """
    int*int -> int*int*int
    return (pgcd, u, v) avec u*max(a, b) + v*min(a, b) == pgcd
    """
    a, b = max(a, b), min(a, b)
    u = (a, 1, 0)
    v = (b, 0, 1)

    while v[0] != 0:
        q = u[0] // v[0]
        u, v = v, (u[0] - q*v[0], u[1] - q*v[1], u[2] - q*v[2])

    return u


def my_inverse(a, N):
    """
    int*int -> int
    retourner inverse de a modulo N, None si a n'est pas inversible
    """
    # tester tout les nombres
    for b in range(N):
        if (a*b) % N == 1:
            return b
    # si on trouve pas d'inverse
    return None


def my_inverse_bezout(a, N):
    """
    int*int -> int
    inverse de a modulo N via pgcd etendu, dans [0, N-1]
    None si a n'est pas inversible
    """
    a %= N
    if a == 0:
        return 0 if N == 1 else None

    # a < N, donc le coefficient de a est le troisième
    gcd, _, v = my_gcd_etendu(N, a)
    if gcd == 1:
        return v % N

    # si on trouve pas d'inverse
    return None


def my_expo_mod(g, n, N):
    """
    int*int*int -> int
    return (g^n) % N
    """
    h = 1

    if n < 0:
        # puissance negative
        g = my_inverse_bezout(g, N)
        if g is None:
            raise ValueError(f"la base n'a pas d'inverse modulo {N}")
        n = -n

    l = n.bit_length()

    #Note: on met la range jusqu'a -1 pour que i prenne aussi la valeur 0.
    for i in range(l - 1, -1, -1):
        h = (h**2) % N

        if (n >> i) & 1 == 1:
            h = (h * g) % N

    return h % N
