from src import Agent as Agent
import numpy as np


class Algorithm:
    """
    This class implements the algorithm. Consists of two methods: the constructor method and the run method which
    executes and returns the result of the algorithm.
    """

    def __init__(self, prices, Mt, Dt, Yt, n, s, ga, gm, gp, pmax, ncycles, init_idx, cut_idx, final_idx, max_t):
        """
        Price at which each of the agents' wealth will be computed.

        Args:

            prices: Temporal series of the prices.
            Mt: Temporal series of the filtered-to-bits price changes.
            Dt: Temporal series of the filtered-to-bits volume changes.
            Yt: Temporal series of the filtered-to-bits volatility.
            n: Number of agents.
            s: Number of strategies.
            ga: DGA-period length.
            gm: Mutation rate.
            gp: Communication pool size.
            pmax: Maximum position held by the agents.
            ncycles: Number of optimization cycles.
            init_idx: Initial index of the optimization period in the temporal series.
            cut_idx: Last index of the optimization period in the temporal series.
            final_idx: Last index of the test period in the temporal series.
            max_t: Maximum half-life time considered by strategies of the agents.

        """

        self.prices = prices
        self.mt = Mt
        self.dt = Dt
        self.yt = Yt
        self.n = n
        self.s = s
        self.ga = ga
        self.gm = gm
        self.gp = gp
        self.pmax = pmax
        self.ncycles = ncycles
        self.init_idx = init_idx
        self.cut_idx = cut_idx
        self.final_idx = final_idx
        self.max_t = max_t

    def run(self):

        """
        This method runs the algorithm.

        Returns: Population of the agent and sets of statistics of the optimization and test period.
        """

        # Create the pool with the number of agents given
        pool = [Agent.Agent(i, self.pmax, self.s, self.max_t) for i in range(0, self.n)]

        # Initialize the dictionary to store the mean and std per optimization cycle.
        statistics_optimization_per_cycle = {}
        last_price = self.prices[self.cut_idx]                                                            # Last price of the optimization cycle.

        wealth_end_cycle = []                                                               # Auxilary array to compute the max and min statistics.

        print('Running optimization period...')
        # Optimization period
        for j in range(0, self.ncycles):  # First loop over number of cycles

            print("Cycle " + str(j))

            if j > 0:                                                                       # Reset the agents and the strategies at the end of each opt cycle.
                for a in pool:
                    a.reset()
                    a.reset_strategies()

            for i in range(self.init_idx, self.cut_idx+1):                                  # Second loop over the time steps

                for agent in pool:                                                          # Third loop over the agents
                    agent.evaluate_strategies(self.prices, self.mt, self.dt, self.yt, i)

                # If it is the end of a DGA-period, evolve the strategies and reset them.
                if (i - self.init_idx) != 0 and (i - self.init_idx) % self.ga == 0:
                    for agent in pool:
                        agent.evolve_strategies(self.gm, self.gp, pool, self.prices[i])
                    for agent in pool:
                        agent.make_evolution()

            # Append the statistics.
            wealth_end_cycle = [a.get_wealth(last_price) for a in pool]
            cycle_stats = (round(np.mean(wealth_end_cycle), 2), round(np.std(wealth_end_cycle), 2))
            statistics_optimization_per_cycle[j] = cycle_stats

        max_opt = np.max(wealth_end_cycle)
        min_opt = np.min(wealth_end_cycle)

        # Reset the agents' wealth and strategies before starting the test period.
        for agent in pool:
            agent.reset()
            #agent.reset_strategies()

        avg_wealth_t_test = []
        avg_position_t_test = []

        print('Running test period...')
        # Test period
        for i in range(self.cut_idx, self.final_idx+1):

            wealths = []
            positions = []

            for agent in pool:  # Third loop over the agents

                agent.evaluate_strategies(self.prices, self.mt, self.dt, self.yt, i)
                wealths.append(agent.get_wealth(self.prices[i]))
                positions.append(agent.get_position())

            if (i - self.init_idx) != 0 and (i - self.init_idx) % self.ga == 0:

                for a in pool:
                    a.evolve_strategies(self.gm, self.gp, pool, self.prices[i])

                for a in pool:
                    a.make_evolution()

            avg_wealth_t_test.append(round(np.mean(wealths), 2))
            avg_position_t_test.append(round(np.mean(positions), 2))

        return pool, wealth_end_cycle, statistics_optimization_per_cycle, avg_wealth_t_test, avg_position_t_test, max_opt, min_opt


    def run2(self):


        # Create the pool with the number of agents given
        pool = [Agent.Agent(i, self.pmax, self.s, self.max_t) for i in range(0, self.n)]

        # Initialize the dictionary to store the mean and std per optimization cycle.
        statistics_optimization_per_cycle = {}
        last_price = self.cut_idx  # Last price of the optimization cycle.

        wealth_end_cycle = []  # Auxilary array to compute the max and min statistics.

        dga_count = 0

        # Optimization period
        for j in range(0, self.ncycles):  # First loop over number of cycles

            print("Cycle " + str(j))

            if j != 0:                       # Reset the agents and the strategies at the end of each opt cycle.
                for a in pool:
                    a.reset()
                    # a.reset_strategies()

            for i in range(self.init_idx, self.cut_idx+1):                              # Second loop over the time steps

                for agent in pool:  # Third loop over the agents
                    agent.evaluate_strategies(self.prices, self.mt, self.dt, self.yt, i)

                # If it is the end of a DGA-period, evolve the strategies and reset them.
                if dga_count is self.ga:
                    dga_count = 0
                    for agent in pool:
                        agent.evolve_strategies(self.gm, self.gp, pool, self.prices[i])
                    for agent in pool:
                        agent.make_evolution()

                dga_count += 1

            # Append the statistics.
            wealth_end_cycle = [a.get_wealth(last_price) for a in pool]
            cycle_stats = (round(np.mean(wealth_end_cycle), 2), round(np.std(wealth_end_cycle), 2))
            statistics_optimization_per_cycle[j] = cycle_stats

        max_opt = np.max(wealth_end_cycle)
        min_opt = np.min(wealth_end_cycle)

        # Reset the agents' wealth and strategies before starting the test period.
        for agent in pool:
            agent.reset()
            agent.reset_strategies()

        avg_wealth_t_test = []
        avg_position_t_test = []

        dga_count = 0

        # Test period
        for i in range(self.cut_idx, self.final_idx+1):

            wealths = []
            positions = []

            for agent in pool:  # Third loop over the agents
                agent.evaluate_strategies(self.prices, self.mt, self.dt, self.yt, i)
                wealths.append(agent.get_wealth(self.prices[i]))
                positions.append(agent.get_position())

            if dga_count is self.ga:
                dga_count = 0
                for agent in pool:
                    agent.evolve_strategies(self.gm, self.gp, pool, self.prices[i])
                for agent in pool:
                    agent.make_evolution()

            dga_count += 1

            avg_wealth_t_test.append(round(np.mean(wealths), 2))
            avg_position_t_test.append(round(np.mean(positions), 2))

        return pool, wealth_end_cycle, statistics_optimization_per_cycle, avg_wealth_t_test, avg_position_t_test, max_opt, min_opt
