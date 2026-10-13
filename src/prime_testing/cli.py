import os

from prime_testing.arithmetic import my_expo_mod, my_gcd, my_inverse_bezout
from prime_testing.experiments import (estimate_proba_test_primality, estimate_proba_test_rabin,
                                       experience_carmichael, experience_carmichael3_t, experience_carmichael_t,
                                       experience_comptage_premier_naiif, experience_exp_mod, experience_first_test,
                                       experience_gcd_inverse, experiment_gen_rsa, experiment_RSA)
from prime_testing.primality import first_test, gen_carmichael3, test_fermat, test_miller_rabin


def calcul_gcd():
	print("**********Calcul de PGCD(a, b)*********")
	a = int(input("Entrez a: "))
	b = int(input("Entrez b: "))
	print("pgcd = ", my_gcd(a, b))

def calcul_inverse():
	print("**********Calcul de inverse modulaire (a^-1 [N])*********")
	a = int(input("Entrez a: "))
	N = int(input("Entrez N: "))
	inv = my_inverse_bezout(a, N)
	if inv is None:
		print(f"{a} n'a pas d'inverse modulo {N}")
	else:
		print(f"{a}*{inv} = {(a*inv) % N} [{N}]")
##Question 1.c
def q1c():
	experience_gcd_inverse(30, 3)
	experience_gcd_inverse(3000, 300, inverse=False)

def calcul_expo_mod():
	print("**********Calcul de exponentiation rapide(g^n [N])*********")
	g = int(input("Entrez g: "))
	n = int(input("Entrez n: "))
	N = int(input("Entrez N: "))
	res = my_expo_mod(g, n, N)
	print(f"{g}^{n} = {res} [{N}]")
	
##Question 1.d
def q1d():
	experience_exp_mod(10000, 500, n_exp=10)


def calcul_first_test():
	p = ["n'est pas premier", "est premier"]
	print("********** teste deterministe naiif *********")
	N = int(input("Entrez N à tester : "))
	prime = first_test(N)
	print(f"{N} {p[prime]}")
##Question 2.a / b
def q2ab():
	experience_first_test(60, 8, n_exp=5)


##Question 2.c
def q2c():
	print("Nombre de nombres premier jusqu'a 1e5 compté via first_test:", experience_comptage_premier_naiif())

##Question 2.d
def q2d():
	experience_carmichael(500000)

##Question 2.e
def q2e():
	print(gen_carmichael3(1e4))

##Question 2.f
def q2f():
	experience_carmichael_t()

##Question 2.f avec 3
def q2f2():
	experience_carmichael3_t()


def calcul_fermat_test():
	p = ["est composé", "est peut-être premier"]
	print("********** teste de Fermat *********")
	N = int(input("Entrez N à tester : "))
	print(f"{N} {p[test_fermat(N)]}")
##Question 3.b / c
def q3bc():
	for i in range(3):
		estimate_proba_test_primality(50000, test_fermat, mode=i)

def calcul_miller_rabin():
	p = ["est composé", "est peut-être premier"]
	print("********** teste de Miller-Rabin *********")
	N = int(input("Entrez N à tester : "))
	print(f"{N} {p[test_miller_rabin(N)]}")

def q4b():
	estimate_proba_test_rabin(50, maxSize=1000000)

def q4c():
	for i in range(3):
		estimate_proba_test_primality(50000, test_miller_rabin, mode=i)

def q4d():
	experiment_gen_rsa(nb_bits_max=1024, step_size=64, n_exp=10)

def bonus():
	experiment_RSA()


menu = [("Question 1.a (calcul pgcd)", calcul_gcd),
		("Question 1.b (calcul inverse)", calcul_inverse),
		("Question 1.c (complexité pgcd, et inverse)", q1c),
		("Question 1.d (calcul expo modulaire)", calcul_expo_mod),
		("Question 1.d2 (complexite expo modulaire)", q1d),
		("Question 2.a (test primalité first_test)", calcul_first_test),
		("Question 2.a / 2.b (complexité first_test)", q2ab),
		("Question 2.c (comptage des premiers inferieurs 1e5)", q2c),
		("Question 2.d (liste des carmichael inferieurs 1e5)", q2d),
		("Question 2.e (carmichael random)", q2e),
		("Question 2.f (max carmichael en 5 minutes incremental)", q2f),
		("Question 2.f (max carmichael en 5 minutes avec carmichael3 aleatoire)", q2f2),
		("Question 3.a (test primalité fermat_test)", calcul_fermat_test),
		("Question 3.b / 3.c (probabilité success fermat)", q3bc),
		("Question 4.a (test primalité miller rabin)", calcul_miller_rabin),
		("Question 4.b (probabilité success miller_rabin)", q4b),
		("Question 4.c (probabilité success miller_rabin)", q4c),
		("Question 4.d (gen_rsa)", q4d),
		("Question BONUS ;)", bonus),]


###Menu
def main():
	while True:

		os.system('cls' if os.name=='nt' else 'clear')

		print("-1: Stop")

		for i, (name, _) in enumerate(menu):
			print(f"{i}: {name}")

		selected = input("Please enter your choice: ")

		try:
			selected = int(selected)

		except ValueError:
			print(f"{selected} is not a number.")
			continue

		if selected == -1:
			break

		else:

			if selected < 0 or selected >= len(menu):
				print(f"{selected} is an invalid choice.")
				continue
		
			os.system('cls' if os.name=='nt' else 'clear')
			menu[selected][1]()
			input("press any key to continue ....")


if __name__ == "__main__":
	main()
