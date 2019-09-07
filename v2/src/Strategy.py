import random


def __init__():
    pass


class Strategy:
    """
    This class implements the strategies described in the article.
    """

    def __init__(self, max_t):
        """
        Constructor of the strategy. It generates a random strategy.

        Args:
            max_t: Maximum half-life time to be considered by the strategy.
        """
        self.alpha = round(random.uniform(0, 1), 2)
        self.beta = round(1 - self.alpha, 2)
        self.tm = random.randint(1, max_t)
        self.td = random.randint(1, max_t)
        self.pos = 0.0
        self.cash = 0.0

    def reset(self):
        """
        This method reset the virtual profits (i.e. the position and cash account) of the strategy.
        """
        self.pos = 0.0
        self.cash = 0

    def get_virtual_profit(self, price):
        """
        Args:
            price: Price at which the virtual profit of the strategy is computed.

        Returns: The virtual profit (computed as pos * price + cash) of the strategy.
        """
        return self.pos * price + self.cash

    def get_param_list(self):
        """
        Returns: The strategy as a list of 4 numbers, representing each of the internal parameters of the strategy.
        """
        return self.alpha, self.beta, self.tm, self.td

    def set_param(self, index, value):
        """
        Auxiliary method to modify the internal parameters of the strategy.

        Args:
            index: Index (0 to 8) of the parameter to be modified.
            value: New value of the parameter.
        """
        if index in (0, 1):
            if index == 0:
                self.alpha = value
                self.beta = round(1 - self.alpha, 2)
            elif index == 1:
                self.beta = value
                self.alpha = round(1 - self.beta, 2)
        elif index == 2:
            self.tm = value
        elif index == 3:
            self.td = value

    def __str__(self):
        """
        Returns: String representation of the strategy.
        """

        s = """alpha = {:.2f} beta = {:.2f} """.format(self.alpha, self.beta)
        s = s + """Tm = {:d} Td = {:d}\n""".format(self.tm, self.td)
        s = s + "Position = {:f}\n".format(self.pos)
        s = s + "Cash = {:.2f}\n".format(self.cash)
        return s

    def __repr__(self):
        return self.__str__()


def create_from_list(params):

    """
    Args:
        params: List representing the internals parameters of the strategy.

    Returns: A strategy created specifically with the parameters passed in.
    """

    s = Strategy(20)

    s.alpha = params[0]
    s.beta = params[1]
    s.tm = params[2]
    s.td = params[3]
    s.pos = 0
    s.cash = 0

    return s


def copy_strategy(strategy):
    """
    This method is written to deal with Python pass-as-reference.

    Args:
        strategy: A strategy.

    Returns: A copy of the strategy.
    """
    params = strategy.get_param_list()
    return create_from_list(params)
