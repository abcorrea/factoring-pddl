#! /usr/bin/env python

from pddl import *
from utils import *

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node1, node2, label):
        if node1 in self.graph:
            self.graph[node1].append((node2, label))

def compute_remainder_table(n):
    table = [None]*n
    for x in range(n):
        row = ((2 * x) % n, (2 * x + 1) % n)
        table[x] = row

    return table

def get_primes(candidate_primes, z):
    primes = []
    product = 1
    idx = 0
    upper_bound = 2 ** (z.bit_length() + 1)
    while product < upper_bound:
        primes.append(candidate_primes[idx])
        product = product * primes[-1]
        idx = idx + 1
    print(f"Selected %d primes: {primes}" % len(primes))
    print(f"Product of selected primes: {product}")
    return primes

def create_automaton(z, p):
    z_remainder = z % p
    table = compute_remainder_table(p)
    g = Graph()
    g.add_node('T')

    # create "base" automaton, where the number x is consumed.
    for x, row in enumerate(table):
        g.add_node((x))
        even = row[0] # 2*x
        odd = row[1] # 2*x + 1
        g.add_edge((x), (even), '0')
        g.add_edge((x), (odd), '1')

    # for each node of the "base", we have a transition reading "#"
    # to a component that will consume y.
    for i in range(len(table)):
        g.add_edge((i), (0, i), 'hashtag')
        for x, row in enumerate(table):
            g.add_node((x, i))
            even = row[0] # 2*x
            odd = row[1] # 2*x + 1
            g.add_edge((x, i), (even, i), '0')
            g.add_edge((x, i), (odd, i), '1')
        for j in range(len(table)):
            if ((i * j) % p) == z_remainder:
                g.add_edge((j, i), 'T', 'hashtag')

    return g

def main():
    args = parse_arguments()

    z = args.z
    candidate_primes = find_primes(2*z)
    print(f"There are %d primes up to {z}: {candidate_primes}" % len(candidate_primes))

    primes = get_primes(candidate_primes, z)

    automata = []
    for p in primes:
        automata.append(create_automaton(z, p))

    print_domain('domain.pddl', primes)
    print_problem('problem.pddl', automata)


if __name__ == "__main__":
    main()
