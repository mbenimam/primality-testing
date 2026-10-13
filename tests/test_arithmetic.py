import math
import random

import pytest

from prime_testing.arithmetic import my_expo_mod, my_gcd, my_gcd_etendu, my_inverse, my_inverse_bezout


def test_gcd_known_value_in_both_orders():
    assert my_gcd(987, 345) == 3
    assert my_gcd(345, 987) == 3


def test_gcd_matches_math_gcd():
    rng = random.Random(1)
    for _ in range(500):
        a, b = rng.getrandbits(64), rng.getrandbits(64)
        assert my_gcd(a, b) == math.gcd(a, b)


def test_gcd_etendu_returns_bezout_coefficients():
    for a, b in [(987, 345), (345, 987)]:
        gcd, u, v = my_gcd_etendu(a, b)
        assert gcd == 3
        assert u*max(a, b) + v*min(a, b) == gcd


def test_gcd_etendu_on_numbers_wider_than_64_bits():
    rng = random.Random(2)
    for _ in range(200):
        a, b = rng.getrandbits(300), rng.getrandbits(200)
        gcd, u, v = my_gcd_etendu(a, b)
        assert all(type(x) is int for x in (gcd, u, v))
        assert gcd == math.gcd(a, b)
        assert u*max(a, b) + v*min(a, b) == gcd


def test_inverse_brute_force():
    assert my_inverse(14, 11) == 4
    assert my_inverse(4, 8) is None


def test_inverse_bezout_is_normalised():
    assert my_inverse_bezout(3, 7) == 5
    assert my_inverse_bezout(14, 11) == 4


def test_inverse_bezout_matches_pow():
    rng = random.Random(3)
    for _ in range(500):
        N = rng.randrange(2, 10**9)
        a = rng.randrange(1, 10**12)
        if math.gcd(a, N) == 1:
            assert my_inverse_bezout(a, N) == pow(a, -1, N)
        else:
            assert my_inverse_bezout(a, N) is None


def test_expo_mod_known_values():
    assert my_expo_mod(2, 10, 67) == pow(2, 10, 67)
    assert my_expo_mod(7892, 678, 79) == pow(7892, 678, 79)
    assert my_expo_mod(5, 23, 77) == pow(5, 23, 77)


def test_expo_mod_matches_pow():
    rng = random.Random(4)
    for _ in range(300):
        g, n, N = rng.getrandbits(256), rng.getrandbits(128), rng.getrandbits(256) + 1
        assert my_expo_mod(g, n, N) == pow(g, n, N)


def test_expo_mod_negative_exponent():
    assert my_expo_mod(3, -1, 7) == 5
    assert my_expo_mod(3, -5, 1000003) == pow(3, -5, 1000003)
    with pytest.raises(ValueError):
        my_expo_mod(4, -1, 8)
