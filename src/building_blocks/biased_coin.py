"""
Based on "A Personal Viewpoint on Probabilistic Programming"
https://simons.berkeley.edu/talks/daniel-roy-10-06-2016
"""


from argparse import ArgumentParser

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import trange

# Inferring the bias (p) of a coin, given a list observations (tosses)

# one experiment: bernoulli(p)
def bernoulli(p):
    return np.random.uniform(0, 1) <= p


# prior
def guesser():
    p = np.random.uniform(0, 1)
    return p


# P(checker is true) == likelihood
# P(obs == generated | model p)
def checker(p, obs):
    return obs == [bernoulli(p) for _ in range(len(obs))]


# posterior: distribution on the return value (g)
def infer(guesser, checker, obs):
    accept = False

    while not accept:
        g = guesser()
        accept = checker(g, obs)

    return g


def main():
    obs = [*[1] * args.s, *[0] * args.f]
    samples = [infer(guesser, checker, obs) for _ in trange(args.num_samples)]

    sns.histplot(samples)
    plt.savefig('./a.png')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--num_samples", type=int, help="Number of samples to draw from posterior."
    )
    parser.add_argument(
        "--s", type=int, help="Number of successes in the observed data."
    )
    parser.add_argument(
        "--f", type=int, help="Number of failures in the observed data."
    )
    args = parser.parse_args()

    main()
