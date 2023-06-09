#! /usr/bin/env python3

import argparse
import re

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", help="The path to the plan.")
    return parser.parse_args()


def check_plan(args):
    with open(args.plan, 'r') as f:
        x = ""
        y = ""
        current = 0
        for line in f:
            match = re.search(r'consume-(\S+)', line)
            if match:
                word = str(match.group(1))
                if word == 'hashtag':
                    current = current + 1
                else:
                    if current == 0:
                        # We are still reading x
                        x += str(word)
                    else:
                        y += str(word)

        z = int(x, 2)*int(y, 2)
        binary_z = '{0:b}'.format(z)
        print(f"In binary:\n\t x = {x} ({len(x)} digits),\n\t y = {y} ({len(y)} digits).")
        print(f"In decimal:\n\t x = {int(x, 2)},\n\t y = {int(y, 2)}.")
        print(f"Product of x and y:\n\t xy = {z}")
        print(f"\t in binary: {binary_z} ({len(binary_z)} digits)")


if __name__ == '__main__':
    args = parse_input()
    check_plan(args)
