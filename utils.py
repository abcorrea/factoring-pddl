import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("z", help="Number to be factored", type=int)
    args = parser.parse_args()
    return args


def print_table(table):
    print("| x | 2x mod n | 2x+1 mod n |")
    print("|---|----------|------------|")

    for x, row in enumerate(table):
        print(f"| {x} | {row[0]}        | {row[1]}          |")


def find_primes(n):
    # Sieve of Eratosthenes
    # This is inneficient and I got it from ChatGPT no shame :-)
    sieve = [True] * (n + 1)
    p = 2
    while p * p <= n:
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
        p += 1

    primes = [p for p in range(2, n+1) if sieve[p]]
    return primes
