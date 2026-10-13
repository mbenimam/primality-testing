import random

import pytest

from prime_testing.primality import first_test
from prime_testing.rsa import RSA, decode, encode, gen_rsa


@pytest.fixture(autouse=True)
def seed():
    random.seed(2020)


@pytest.mark.parametrize("t", [3, 4, 10, 16])
def test_gen_rsa_returns_two_distinct_primes_of_t_bits(t):
    for _ in range(20):
        p, q, n = gen_rsa(t)
        assert p != q and n == p*q
        assert p.bit_length() == t and q.bit_length() == t
        assert first_test(p) and first_test(q)


@pytest.mark.parametrize("t", [16, 64, 256])
def test_keys_are_inverse_modulo_phi(t):
    (e, n), (d, n2) = RSA(t)
    assert n == n2
    assert 0 < d
    for m in (2, 65, 12345):
        assert pow(pow(m, e, n), d, n) == m


@pytest.mark.parametrize("t", [16, 64, 256])
def test_encode_decode_round_trip(t):
    public_key, private_key = RSA(t)
    message = "Bonjour, é ç à !"
    cipher = encode(message, public_key)
    assert cipher != [ord(c) for c in message]
    assert decode(cipher, private_key) == message

