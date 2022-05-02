#!/usr/bin/env   python3

import click
import random
import sys


@click.command()
@click.argument(
        "alphabet_f",
        type=click.File('r'))
@click.option(
        "--space",
        "space_weight",
        type=int,
        default=88,
        show_default=True,
        help="White space weight")
def generate(alphabet_f, space_weight: int):
    """
    Using the alphabet from `alphabet_f`, generates random sentences.
    """
    alphabet = list(map(str.strip, alphabet_f))
    weights  = [ random.randrange(10, 50) for _ in alphabet ]

    alphabet.append(" ")
    weights.append(space_weight)
    assert len(alphabet) == len(weights)

    print(alphabet, weights, sep="\n", file=sys.stderr)
    for _ in range(10_000):
        print(''.join(random.choices(alphabet, weights, k=random.randrange(20, 60))), ".", sep="")





if __name__ == "__main__":
    generate()
