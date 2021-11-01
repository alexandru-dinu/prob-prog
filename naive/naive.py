"""
Based on "A Personal Viewpoint on Probabilistic Programming"
https://simons.berkeley.edu/talks/daniel-roy-10-06-2016

Inferring the bias (p) of a coin, given a list observations (tosses).
"""


from argparse import ArgumentParser
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tqdm import trange


def infer(
    prior: Callable[[], float],
    likelihood: Callable[[float, int], np.ndarray],
    obs: np.ndarray,
    num_samples: int,
) -> np.ndarray:
    """Sample from the posterior distribution by answering the following question:

        What values from the prior are more likely to generate the observed data?

    Args:
        prior: A function that returns a single random value from the prior.
        likelihood: A function that returns n samples from the likelihood distribution
            given the fixed value of p.
        obs: An array of observed values.
        num_samples: The number of samples to draw from the posterior.

    Returns:
        A list of `num_samples` samples from the posterior.
    """
    posterior = [0] * num_samples
    accept = False

    for i in trange(num_samples):
        while not accept:
            p = prior()
            accept = (obs == likelihood(p, len(obs))).all()
        posterior[i] = p
        accept = False

    return np.array(posterior)


def main():
    obs = np.array([*[1] * args.s, *[0] * args.f])
    np.random.shuffle(obs)

    prior = lambda: np.random.uniform(0, 1)
    likelihood = lambda p, n: np.random.binomial(n=1, p=p, size=n)
    posterior = infer(prior, likelihood, obs, args.num_samples)

    sns.histplot(posterior, stat="probability")
    plt.xlim([0, 1])
    plt.show()


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
