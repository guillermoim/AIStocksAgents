from src import Strategy as st
from src import Functions as ut
from src import DGA as dga
import operator


class Agent:

    """
    This class represent the Agents in the model.
    """

    def __init__(self, id, pmax, sn, max_t):
        """
        Constructor of Agent.

        Args:
            id: This parameter identifies the agent in a unique way.
            pmax: This parameter indicates the maximum position to be held by an agent.
            sn: This parameter indicates the number of strategies the agent owns.
            max_t: Maximum half-life time of the strategies created for the agent.
        """

        # When an agent is created only Pmax, ga, s and max t are needed.
        # Wealth is set to 0 and strategies are generated randomly.

        self.id = id  # Id para identificar al agente. Dos
        self.pmax = pmax
        self.max_t = max_t

        self.strategies = [st.Strategy(max_t) for _ in range(0, sn)]
        self.cash = 0
        self.position = 0
        self.next_strategies = []

    def get_strategies_by_profit(self, price):
        """
        This method sort and returns the agent's strategies on the virtual profits at the given price.

        Args:
            price: Value of the price on which the virtual profit will be computed.

        Returns: List of strategies sorted on their virtual profit

        """

        x = [(s, s.pos * price + s.cash) for s in self.strategies]
        ls = sorted(x, key=operator.itemgetter(1), reverse=True)
        res = [e[0] for e in ls]
        return res

    def get_top_strategy(self, price):
        """
        This method returns the agent's top strategy at the given price.

        Args:
            price: Value of the price on which the virtual profit will be computed.

        Returns: The best performing strategy of the agent at the given price.

        """

        return self.get_strategies_by_profit(price)[0]

    def get_wealth(self, price):
        """

        Args:
            price: Value of the price on which the wealth will be computed.

        Returns: The wealth of the agent.

        """

        return round(self.cash + self.position * price, 2)

    def get_position(self):
        """

        Returns: The position held by the agent.

        """
        return self.position

    def get_cash(self):
        """

        Returns: The cash account of the agent.

        """

        return self.cash

    def evaluate_strategies(self, prices, Mt, Dt, nn_m, nn_d, t):  # Evaluate the strategies for Mt, Dt, Yt at time step t
        """
        This method is called on each timestep and it evaluates each of the agent's strategies according to the
        description in the article.

        Args:
            prices: Temporal series of the prices.
            Mt: Temporal series of the filtered-to-bits price changes.
            Dt: Temporal series of the filtered-to-bits volume changes.
            Yt: Temporal series of the filtered-to-bits volatility.
            t: Time-step on which the strategies will be evaluated.

        """

        # First thing: Evaluate profit of the agent

        # Max benefit of applying a determined strategy
        price = prices[t]

        new_pos = 0
        maxProfit = None

        for s in self.strategies:

            # Compute the impact factors
            i_m = ut.impact_factor(Mt, s.tm, t)
            i_d = ut.impact_factor(Dt, s.td, t)

            current_position = s.pos
            current_cash = s.cash

            # Compute the strategy position-change level
            # l_t = s.alpha * s.em * i_m * nn_m + s.beta * s.ed * i_d * nn_d
            l_t = s.alpha * i_m * nn_m + s.beta * i_d * nn_d

            # Compute position at time t
            p_t = round(l_t * self.pmax)

            virtual_profit = s.pos * price + s.cash

            # Compute virtual profit from the position at time t
            s.cash = current_cash - (p_t - current_position) * round(price, 2)
            s.pos = p_t

            if maxProfit is None or virtual_profit > maxProfit:
                new_pos = p_t
                maxProfit = virtual_profit

        # Add the max_profit obtained from a strategy at time-step t to the agent's wealth
        cash_flow = (new_pos - self.position) * round(price, 2)
        self.cash = self.cash - cash_flow
        self.position = new_pos

    def evolve_strategies(self, gm, price, pool, gp):
        """
        This method implement the evolution of the agent's strategies. Accordingly to the paper, it implements the
        crossover, mutation and communication steps. The results of the evolution are stored in the Agent attribute
        next_strategies`.

        Args:
            gm: Mutation rate.
            gp: Size of the communication pool.
            pool: Collections of agents conforming the pool.
            price: Price at which each of the agents' wealth will be computed.

        """
        max_t = self.max_t

        # Crossover
        strategies = self.get_strategies_by_profit(price)[:]
        a, b = dga.one_point_crossover(strategies[0], strategies[1])

        # Communication
        res1, res2 = dga.communication(gp, pool, self, price)

        # Mutation
        res3 = dga.mutation(a, gm, max_t)
        res4 = dga.mutation(b, gm, max_t)

        # Replacement
        modified_strategies = []
        modified_strategies.extend(strategies[0:4])

        modified_strategies.append(res1)
        modified_strategies.append(res2)
        modified_strategies.append(res3)
        modified_strategies.append(res4)

        self.next_strategies = modified_strategies[:]

    def make_evolution(self):
        """
        This method makes the evolution effective, this means to copy the evolved strategies (which are in the Agent
        attribute next_strategies>`) to the strategies attribute.
        """
        self.strategies = self.next_strategies[:]
        self.next_strategies = []
        self.reset_strategies()

    def reset(self):
        """
        This method set the agent's position and cash to 0.
        """
        self.cash = 0
        self.position = 0

    def reset_strategies(self):
        """
        This method resets (i.e. sets virtual profits to 0) each of the agent's strategies.
        """
        for s in self.strategies:
            s.reset()

    def __str__(self):
        """
        String representation of the Agent.
        """
        return "ID= " + str(self.id) + " / Cash= "+str(self.cash) + " Position  =" + str(self.position)

    def __repr__(self):
        return str(self)