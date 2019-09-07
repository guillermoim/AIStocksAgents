import math


def __init__():
    pass


def impact_factor(series, halftime, t):

    """
    Compute the impact factor as described in the paper.

    Args:

        series: Temporal series.
        halftime: Half-life time of the strategy.
        t: Reference time step.

    Returns: Impact factor in the range (-1, +1).
    """

    numerator = 0.0
    denominator = 0.0

    for tau in range(1, halftime + 1):
        aux = math.exp(- (tau - 1) / halftime)
        numerator += series[t - tau] * aux
        denominator += aux

    if denominator == 0:
        print(t, halftime)

    return round(numerator/denominator, 2)


def sign2(value):
    if value >= 0:
        return 1
    else:
        return -1

