from src import Data as Data
from src import Algorithm as Alg
import matplotlib.pyplot as plt
import datetime
import os
from timeit import default_timer as timer
from src import Plotting as p
import pickle


n = 1000                         # n: Numero de agentes
s = 8                            # s: Numero de estrategias por agente
g_a = 60                         # g_a: periodo de DGA
g_m = 0.5                        # g_m: ratio de mutacion
g_p = 8                          # g_p: tamao de la 'communication pool'
p_max = 10                       # p_max: pos max de cada agente
ncycles = 100                     # ncycles: Numero de ciclos en los que el algoritmo recorre el periodo de optimizacion
max_t = 20                        # Max value

stock = 'NKY 225'
df = Data.get_pandas_dataframe(r'datasets/NKY225.csv', 'Close').drop(columns=['index'])
title = 'NKY 225'

prices = list(df.Price.values)
dates = list(df.Date.values)
Mt = list(df.Mt.values)
Dt = list(df.Dt.values)
Yt = list(df.Yt.values)

initial_date = '1993-03-17'
cut_date = '2005-05-12'
end_date = '2012-05-17'

initial_idx = dates.index(initial_date)
cut_idx = dates.index(cut_date)
end_idx = dates.index(end_date)

print('Initial date (index in series) is ' + initial_date + '()' + str(initial_idx)+')')
print('Cut date (index in series) is ' + cut_date + '()' + str(cut_idx)+')')
print('End date (index in series) is ' + end_date + '(' + str(end_idx)+')')

print('Lenght in timesteps of the optimization period: ' + str(cut_idx - initial_idx) )

alg = Alg.Algorithm(prices, Mt, Dt, Yt, n, s, g_a, g_m, g_p, p_max, ncycles, initial_idx, cut_idx, end_idx, max_t)

start = timer()

print('Starting the simulation...')

pool, all_agents, statistics_opt, avg_wealth_t_test, avg_position_t_test, max_opt, min_opt = alg.run2()

end = timer() - start

print('Duration of the execution: ' + str(end))

tmp = str(datetime.datetime.now())

directory = 'results/'+stock+' '+tmp

os.mkdir(directory)

last_price_opt = prices[cut_idx]
last_price_test = prices[end_idx]

# Histograms OPT and TEST

p.save_histogram(all_agents, 'Number of agents by wealth - Histogram - Optimization', 25, directory+'/histogram-optimization-period.png')

p.save_histogram([a.get_wealth(last_price_test) for a in pool], 'Number of agents by wealth - Histogram - Test', 25, directory+'/histogram-test-period.png')

# Position + Price chart

fig, ax1 = plt.subplots()
color = 'black'
ax1.set_xlabel('Day')
ax1.set_ylabel('NKY Index')
ax1.plot(prices[cut_idx:end_idx], color=color)

ax2 = ax1.twinx()

color = 'orange'
ax2.set_ylabel('Average Position', color=color)
ax2.plot(avg_position_t_test, color=color, linewidth=0.8, alpha=0.7)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()
plt.savefig(directory+'/position-price-test-chart.png')

# Wealth + Price chart
fig, ax1 = plt.subplots()
color = 'black'
ax1.set_xlabel('Day')
ax1.set_ylabel('NKY Index')
ax1.plot(prices[cut_idx:end_idx], color=color)

ax2 = ax1.twinx()

color = 'red'
ax2.set_ylabel('Mean Wealth', color=color)
ax2.plot(avg_wealth_t_test, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()
plt.savefig(directory+'/wealth-price-test-chart.png')

test_result = [agent.get_wealth(last_price_test) for agent in pool]

file = open(directory+'/report.txt', 'w')

p.out_report(file, alg, statistics_opt, max_opt, min_opt, test_result, stock)
