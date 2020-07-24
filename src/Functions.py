import math
import collections

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

    return round(numerator/denominator, 2)

def normalize_seconds(seconds: int) -> tuple:
    (days, remainder) = divmod(seconds, 86400)
    (hours, remainder) = divmod(remainder, 3600)
    (minutes, seconds) = divmod(remainder, 60)

    return collections.namedtuple("_", ("days", "hours", "minutes", "seconds"))(days, hours, minutes, seconds)


