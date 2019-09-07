from src import NeuralNetwork as nn
from src import Agent as Agent
from src import Functions as ft
import numpy as np


class Algorithm:
    """
    This class implements the algorithm. Consists of two methods: the constructor method and the run method which
    executes and returns the result of the algorithm.
    """

    def __init__(self, prices, volumes, memory, Mt, Dt, n, s, ga, gm, gp, pmax, iterations, ncycles, init_nn_train, end_nn_train, cut_idx, final_idx, max_t):
        self.prices = prices
        self.volumes = volumes
        self.memory = memory
        self.mt = Mt
        self.dt = Dt
        self.n = n
        self.s = s
        self.ga = ga
        self.gm = gm
        self.gp = gp
        self.iterations = iterations
        self.pmax = pmax
        self.ncycles = ncycles
        self.init_nn_train = init_nn_train
        self.end_nn_train = end_nn_train
        self.cut_idx = cut_idx
        self.final_idx = final_idx
        self.max_t = max_t

    def run(self):

        mem_size = self.memory

        input_prices = self.prices[self.init_nn_train:self.end_nn_train]
        input_volumes = self.volumes[self.init_nn_train:self.end_nn_train]

        test_prices = self.prices[self.end_nn_train:self.final_idx]
        test_volumes = self.volumes[self.end_nn_train:self.final_idx]

        # Primero: Construir y entrenar redes neuronales.

        scl1, train_prices, labels_prices, features_set_prices, model_prices = nn.build_and_train(input_prices, mem_size)
        scl2, train_volumes, labels_volumes, features_set_volumes, model_volumes = nn.build_and_train(input_volumes, mem_size)

        predictions_prices = nn.train(scl1, train_prices, labels_prices, features_set_prices, model_prices, test_prices, mem_size, self.iterations)
        predictions_volumes = nn.train(scl2, train_volumes, labels_volumes, features_set_volumes, model_volumes, test_volumes, mem_size, self.iterations)

        # Segundo: Entrenar GA + red neuronal

        pool = [Agent.Agent(i, self.pmax, self.s, self.max_t) for i in range(0, self.n)]

        last_price_opt = self.prices[self.cut_idx]
        opt_stats = None

        statistics_optimization_per_cycle = {}
        last_price = self.prices[self.cut_idx]  # Last price of the optimization cycle.


        for j in range(0, self.ncycles):

            print("Cycle ", j)

            if j > 0:  # Reset the agents and the strategies at the end of each opt cycle.
                for a in pool:
                    a.reset()
                    a.reset_strategies()

            for i in range(self.end_nn_train, self.cut_idx + 1):  # Second loop over the time steps

                hip = i - self.end_nn_train
                nn_m = ft.sign2(predictions_prices[hip+1] - predictions_prices[hip])
                nn_d = ft.sign2(predictions_volumes[hip+1] - predictions_prices[hip])

                for agent in pool:  # Third loop over the agents
                    agent.evaluate_strategies(self.prices, self.mt, self.dt, nn_m, nn_d, i)

                # If it is the end of a DGA-period, evolve the strategies and reset them.
                if (i - self.end_nn_train) != 0 and (i - self.end_nn_train) % self.ga == 0:
                    for agent in pool:
                        agent.evolve_strategies(self.gm, self.prices[i], pool, self.gp)
                    for agent in pool:
                        agent.make_evolution()

            wealth_end_cycle = [a.get_wealth(last_price) for a in pool]
            cycle_stats = (round(np.mean(wealth_end_cycle), 2), round(np.std(wealth_end_cycle), 2))
            statistics_optimization_per_cycle[j] = cycle_stats

        max_opt = np.max(wealth_end_cycle)
        min_opt = np.min(wealth_end_cycle)

        all_agents = []

        for a in pool:
            all_agents.append(a.get_wealth(self.prices[self.cut_idx]))
            a.reset()
            a.reset_strategies()

        avg_wealth_t_test = []
        avg_position_t_test = []

        for i in range(self.cut_idx, self.final_idx):  # Second loop over the time steps

            wealths = []
            positions = []


            nn_m = 1
            nn_d = 1

            for agent in pool:  # Third loop over the agents
                agent.evaluate_strategies(self.prices, self.mt, self.dt, nn_m, nn_d, i)
                wealths.append(agent.get_wealth(self.prices[i]))
                positions.append(agent.get_position())

            # If it is the end of a DGA-period, evolve the strategies and reset them.
            if (i - self.end_nn_train) != 0 and (i - self.end_nn_train) % self.ga == 0:
                for agent in pool:
                    agent.evolve_strategies(self.gm, self.prices[i], pool, self.gp)
                for agent in pool:
                    agent.make_evolution()

            avg_wealth_t_test.append(round(np.mean(wealths), 2))
            avg_position_t_test.append(round(np.mean(positions), 2))

        return pool, all_agents, wealth_end_cycle, statistics_optimization_per_cycle, avg_wealth_t_test, avg_position_t_test, max_opt, min_opt
