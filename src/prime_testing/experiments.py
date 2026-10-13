import random
import time

import matplotlib.pyplot as plt
import numpy as np

from prime_testing.arithmetic import my_expo_mod, my_gcd, my_gcd_etendu, my_inverse, my_inverse_bezout
from prime_testing.plotting import Drawer, drawConfusionMatrix, save_path
from prime_testing.primality import (first_test, gen_carmichael, gen_carmichael3, gen_carmichael_3_list,
                                     isCarmichael, test_miller_rabin)
from prime_testing.rsa import RSA, decode, encode, gen_rsa

def timeit(method, *args):
    """
    function->int
    return runtime in seconds
    """
    start_time = time.time()
    method(*args)
    return time.time() - start_time

"""
Question 1.c
"""
def experience_gcd_inverse(n, step=1, n_exp=10, inverse=True):

    drawer = Drawer(title="Temps en fonction de N")
    
    for i in range(3, n, step):

        mean_exec = 0
        gcd_time = 0
        gcd_etendu_time = 0
        inverse_bezout_time = 0

        for exp in range(n_exp):
            a = random.getrandbits(i+1)
            N = random.getrandbits(i)

            if inverse:
                mean_exec += timeit(my_inverse, a, N)


            gcd_time += timeit(my_gcd, a, N)

            gcd_etendu_time += timeit(my_gcd_etendu, a, N)

            inverse_bezout_time += timeit(my_inverse_bezout, a, N)


        drawer.add(name="my_gcd", time=gcd_time/n_exp, size=i)
        drawer.add(name="my_gcd_etendu", time=gcd_etendu_time/n_exp, size=i)

        if inverse:
            drawer.add(name="my_inverse", time=mean_exec/n_exp, size=i)

        drawer.add(name="my_inverse_bezout", time=inverse_bezout_time/n_exp, size=i)

    drawer.draw()


def experience_exp_mod(n, step=1, n_exp=10, naiive=False):

    drawer = Drawer(title="Temps en fonction de nombre de bits de la puissance")
    
    puissance_classique = lambda x, y, z: z % (x**y) 
    mean_exec = 0
    for i in range(3, n, step):

        mean_exec1 = 0
        mean_exec2 = 0
        for exp in range(n_exp):
            a = random.getrandbits(1024)
            b = random.getrandbits(i)
            N = random.getrandbits(1024)

            mean_exec1 += timeit(my_expo_mod, a, b, N)
            if naiive:
                mean_exec2 += timeit(puissance_classique, a, b, N)

        drawer.add(name="my_expo_mod", time=mean_exec1/n_exp, size=i)

        if naiive:
            drawer.add(name="puissance_classique", time=mean_exec2/n_exp, size=i)

    drawer.draw()


def experience_first_test(n, step=1, n_exp=10):

    drawer = Drawer(title="Temps en fonction de N")

    for i in range(3, n, step):

        mean_exec = 0

        print(i)
        for exp in range(n_exp):

            n = random.getrandbits(i)

            mean_exec += timeit(first_test, n)


        drawer.add(name="first_test", time=mean_exec/n_exp, size=i)

    drawer.draw()


def experience_comptage_premier_naiif(N=1e5):
    """
    int->int
    nombre de nombre premier inferieur à N
    """
    cpt = 0
    for i in range(2, int(N)):
        if first_test(i):
            cpt += 1
    return cpt


def experience_carmichael(N=1e5):
    """
    int
    """
    cpt = 0
    for i in range(int(N)):
        if isCarmichael(i):
            print(i)
            cpt += 1
    return cpt
    
def experience_carmichael_t(tmax=5*60):
    start_time = time.time()
    i = 1

    while time.time() - start_time < tmax:
        # +2 pour éviter de tester les paire
        i += 2
        if isCarmichael(i):
            print(i)


def experience_carmichael3_t(tmax=5*60):
    """
    int -> int
    """
    start_time = time.time()
    best = 0
    N = int(1e4)

    while time.time() - start_time < tmax:

        print("N:", N)

        for i in range(4):

            if time.time() - start_time >= tmax:
                break

            carm = gen_carmichael3(N=N)

            if carm > best:
                best = carm

            print(carm)

        N *= 2

    print("Plus grand nombre de carmicheal trouvé: ", best)


def generateRandomCompositeImp(maxSize=100000):

    notPrime = random.randrange(4, maxSize)

    while first_test(notPrime) or (notPrime % 2) == 0:
        notPrime = random.randrange(4, maxSize)

    return notPrime


def estimate_proba_test_primality(n, testFunction, maxSize=10000, mode=0):
    """
    Entrées:
        n : Nombre de test
        maxSize : Taille maximum des valeurs testés
        mode:
            0 = Nombre généré par gen_carmichael
            1 = Nombre composé
            2 = Aléatoire

        Ne retourne rien mais print la probabilité de succes estimé.
    """
    titles = ["carmichael", "aleatoire composé", "aleatoire"]
    print("Estimating proba fermat mode = ", titles[mode])

    if mode == 0:
        carmichael_list = gen_carmichael(maxSize)

    confusion = np.zeros((2,2))

    for i in range(n):

        if mode == 0:
            prime = random.choice(carmichael_list)

        elif mode == 1:
            prime = generateRandomCompositeImp(maxSize)
            #Si celle là, que faire dans le cas de prime = 4 ?
        elif mode == 2:
            #n impair et supérieur a 2
            prime = random.randrange(3, maxSize, 2)

        mayPrime = testFunction(prime)
        isPrime  = first_test(prime)

        confusion[1-mayPrime, 1-isPrime] += 1

    confusion = confusion/confusion.sum()
    drawConfusionMatrix(confusion, "confusion_"+testFunction.__name__+"_"+titles[mode])


def estimate_proba_test_rabin(n, maxSize=100000):
    """
    Entrées:
        n : Nombre de test
        maxSize : Taille maximum des valeurs testés
        mode:
            0 = Nombre généré par gen_carmichael
            1 = Nombre composé
            2 = Aléatoire

        Ne retourne rien mais print la probabilité de succes estimé.
    """

    modeLabel = ["Carmichael", "Composé", "Aléatoire"]
    
    plt.figure("miller_rabin")
    plt.xlabel("T")
    plt.ylabel("probabilité d'erreur (entre 0 et 1)")
    plt.title("probabilité d'erreur en fonction de T du test de Miller Rabin")

    carmichael_list = gen_carmichael_3_list(3e3, 50)

    for mode in range(3):
        
        x = []
        y = []
        
        for T in range(1, 10):
            print("T = ", T)
            error_counter = 0

            for i in range(n):

                if mode == 0:
                    prime = random.choice(carmichael_list)

                elif mode == 1:
                    prime = generateRandomCompositeImp(maxSize)
                    #Si celle là, que faire dans le cas de prime = 4 ?
                elif mode == 2:
                    #n impair et supérieur a 2
                    prime = random.randrange(3, maxSize, 2)

                mayPrime = test_miller_rabin(prime, T)

                isPrime  = first_test(prime)

                if mayPrime != isPrime:
                    error_counter += 1

            error_pourcent = error_counter/n

            x.append(T)
            y.append(error_pourcent)

        plt.plot(x, y, label=modeLabel[mode])

    plt.legend(loc='best')
    plt.savefig(save_path("miller_rabin_test_T"))
    plt.show()


def experiment_gen_rsa(nb_bits_max=128, step_size=2, n_exp=10):
    drawer = Drawer()
    
    # pour chaque taille de nombre
    for i in range(3, nb_bits_max, step_size):
        # faire la moyenne des n_exp lancé

        mean_exec = 0
        for exp in range(n_exp):
            mean_exec += timeit(gen_rsa, i)

        drawer.add(name="gen_rsa", time=mean_exec/n_exp, size=i)
    drawer.draw()


def experiment_RSA():

    public_key,  private_key = RSA(1024)

    m = "Bonjour"
    t = time.time()
    s = encode(m, public_key)
    d = decode(s, private_key)
    print(f"message envoyé: {m}, message décodé: {d}, temps encodage_decodage : {time.time() - t}")
