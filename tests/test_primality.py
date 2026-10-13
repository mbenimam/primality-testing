import random
from math import isqrt

import pytest

from prime_testing import primality
from prime_testing.primality import first_test, gen_carmichael, gen_carmichael3, isCarmichael, isCarmichael_facteurs

# les 16 nombres de Carmichael inferieurs à 10^5
CARMICHAEL_1E5 = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841,
                  29341, 41041, 46657, 52633, 62745, 63973, 75361]


def is_prime(n):
    """Oracle indépendant du code testé."""
    return n >= 2 and all(n % i for i in range(2, isqrt(n) + 1))


@pytest.fixture(autouse=True)
def seed():
    random.seed(2020)


def test_first_test_matches_oracle():
    for n in range(-5, 5000):
        assert first_test(n) == is_prime(n), n


def test_first_test_counts_primes_below_1e5():
    assert sum(first_test(n) for n in range(10**5)) == 9592


def test_korselt_criterion():
    assert isCarmichael_facteurs(561, [3, 11, 17])
    assert not isCarmichael_facteurs(231, [3, 7, 11])
    assert isCarmichael_facteurs(216821881, [331, 661, 991])
    # 45 = 3^2 * 5 : 44 est divisible par 2 et par 4, seul le facteur carré l'écarte
    assert not isCarmichael_facteurs(45, [3, 5])


def test_isCarmichael():
    assert isCarmichael(561)
    assert not isCarmichael(231)
    # un nombre premier n'est pas de Carmichael
    assert not isCarmichael(563)


def test_gen_carmichael_lists_the_known_ones():
    assert gen_carmichael(3000) == [561, 1105, 1729, 2465, 2821]


def test_gen_carmichael3_returns_a_carmichael_number():
    for _ in range(5):
        n = gen_carmichael3(200)
        assert not is_prime(n)
        assert isCarmichael(n)


def test_fermat_agrees_with_trial_division_on_the_original_cases():
    # 377791 = 17 * 71 * 313 : composé, et la base 253432 le voit
    assert not primality.test_fermat(377791, 253432)
    # 377789 est premier : aucune base ne peut le rejeter
    assert primality.test_fermat(377789, 253432)


def test_fermat_base_sharing_a_factor_exposes_561():
    # 561 = 3 * 11 * 17 et 3 divise 3
    assert not primality.test_fermat(561, 3)


def test_fermat_is_fooled_by_carmichael_numbers():
    # toute base première avec 561 ment : 319 bases sur les 559 de [2, 560]
    liars = sum(primality.test_fermat(561, a) for a in range(2, 561))
    assert liars == 319
    assert primality.test_fermat(561, 2)


def test_fermat_never_rejects_a_prime():
    for p in [3, 5, 7, 101, 7919]:
        for a in range(2, min(p, 50)):
            assert primality.test_fermat(p, a)


def test_miller_rabin_small_and_even_inputs():
    assert [primality.test_miller_rabin(n) for n in range(-1, 10)] == \
        [False, False, False, True, True, False, True, False, True, False, False]


def test_miller_rabin_matches_oracle_on_odd_numbers():
    for n in range(5, 20000, 2):
        assert primality.test_miller_rabin(n, 10) == is_prime(n), n


def test_miller_rabin_never_rejects_a_prime_with_one_round():
    for n in range(3, 5000):
        if is_prime(n):
            assert primality.test_miller_rabin(n, 1), n


def test_miller_rabin_rejects_carmichael_numbers():
    for n in CARMICHAEL_1E5:
        assert not primality.test_miller_rabin(n, 10), n


def test_miller_rabin_squares_at_most_h_minus_1_times(monkeypatch):
    # n - 1 = 2^h * m : un tour coûte une exponentiation puis au plus h-1 carrés
    calls = []
    real = primality.my_expo_mod

    def counting(g, e, N):
        calls.append(e)
        return real(g, e, N)

    monkeypatch.setattr(primality, "my_expo_mod", counting)
    T = 3
    for h in (16, 20, 24):
        n = (1 << h) + 1
        calls.clear()
        primality.test_miller_rabin(n, T)
        assert len(calls) <= T * h, (h, len(calls))


def test_miller_rabin_on_large_known_values():
    assert primality.test_miller_rabin(2**127 - 1)        # premier de Mersenne
    assert not primality.test_miller_rabin(2**128 + 1)    # nombre de Fermat composé
    assert not primality.test_miller_rabin((2**61 - 1) * (2**89 - 1))
