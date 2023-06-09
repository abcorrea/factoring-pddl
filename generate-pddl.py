#! /usr/bin/env python

from pddl import *
from utils import *

class Graph:
    def __init__(self):
        self.graph = {}
        self.initial_node = None

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node1, node2, label):
        if node1 in self.graph:
            self.graph[node1].append((node2, label))

    def set_initial_node(self, node):
        assert node in self.graph.keys()
        self.initial_node = node

    def get_initial_node_str(self):
        return str(self.initial_node)

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
    upper_bound = 2 ** (z.bit_length())
    while product <= upper_bound:
        primes.append(candidate_primes[idx])
        product = product * primes[-1]
        idx = idx + 1
    print(f"Selected %d primes: {primes}" % len(primes))
    print(f"Product of selected primes: {product}")
    return primes

def create_prime_automaton(z, p):
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

    g.set_initial_node(0)

    return g


def create_trivial_factor_automaton(z):

    print("Creating automaton to forbid factorization z = 1*z.")
    # Forbids that factors are 1 and z
    g = Graph()
    g.add_node('T')
    g.add_node('x0')
    g.add_node('x1')
    g.add_node('x2')
    g.add_node('y0')
    g.add_node('y1')
    g.add_node('y2')

    g.set_initial_node('x0')

    # In the first node, we need to consume at least
    # one '1', otherwise we are just adding trailing 0s
    g.add_edge('x0', 'x0', '0')
    g.add_edge('x0', 'x1', '1')

    # When we move to the next node, we need
    # to consume at least a 0 or an 1. In other words,
    # we cannot consume #
    g.add_edge('x1', 'x2', '0')
    g.add_edge('x1', 'x2', '1')

    # Once we reach x2, we know that x != 1. So we can
    # either consume more digits or end the word x here
    # and move to y.
    g.add_edge('x2', 'x2', '0')
    g.add_edge('x2', 'x2', '1')
    g.add_edge('x2', 'y0', 'hashtag')

    # Same idea for y
    ## First part
    g.add_edge('y0', 'y0', '0')
    g.add_edge('y0', 'y1', '1')
    ## Second part
    g.add_edge('y1', 'y2', '0')
    g.add_edge('y1', 'y2', '1')
    ## Third part, but now we go to accepting node T
    ## once we read the hashtag token
    g.add_edge('y2', 'y2', '0')
    g.add_edge('y2', 'y2', '1')
    g.add_edge('y2', 'T', 'hashtag')

    return g

def create_length_automaton(z):
    # We know that |x| + |y| = |z|
    ## TODO or should it be |z| + 1?

    g = Graph()
    g.add_node('T')
    bits = z.bit_length()+2
    for i in range(bits):
        g.add_node(i)
        if i == 0:
            g.add_edge(i, i, '0')
            g.add_edge(i, i+1, '1')
            g.add_edge(i, i, 'hashtag')
        elif i == bits-1:
            g.add_edge(i, 'T', 'hashtag')
        elif i == bits-2:
            g.add_edge(i, 'T', 'hashtag')
        else:
            g.add_edge(i, i+1, '0')
            g.add_edge(i, i+1, '1')
            g.add_edge(i, i, 'hashtag')

    g.set_initial_node(0)
    return g


def main():
    args = parse_arguments()

    z = args.z
    candidate_primes = find_primes(z)
    print(f"There are %d primes up to {z}." % len(candidate_primes))

    primes = get_primes(candidate_primes, z)

    automata = []
    for p in primes:
        automata.append(create_prime_automaton(z, p))
    automata.append(create_trivial_factor_automaton(z))
    automata.append(create_length_automaton(z))

    print_domain('domain.pddl', automata)
    print_problem('problem.pddl', automata)


if __name__ == "__main__":
    main()
