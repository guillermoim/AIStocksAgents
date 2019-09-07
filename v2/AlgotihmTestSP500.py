from src import Data as Data
from src import Algorithm as Alg
from src import Plotting as p
import matplotlib.pyplot as plt
import datetime
import os
from timeit import default_timer as timer

memory = 40
n = 100
s = 8
ga = 50
gm = 0.5
gp = 8
pmax = 10
itera = 10
ncycles = 2

max_t = 20

stock = 'S&P 500'
df = Data.get_pandas_dataframe(r'datasets/sp500.csv', 'Open').drop(columns=['index'])
title = 'S&P 500'


prices = list(df.Price.values)
dates = list(df.Date.values)
volumes = list(df.Volume.values)

Mt = list(df.Mt.values)
Dt = list(df.Dt.values)

init_nn_date = '1990-01-02'
end_nn_date = '2000-01-10'
cut_date = '2005-05-12'
end_date = '2012-02-10'

init_nn_train_idx = dates.index(init_nn_date)
end_nn_train_idx = dates.index(end_nn_date)
cut_idx = dates.index(cut_date)
final_idx = dates.index(end_date)

print('Initial date training neural network (index in series) is', init_nn_date, '(', init_nn_train_idx, ')')
print('End date training neural network (index in series) is ', end_nn_date, '(', end_nn_train_idx, ')')
print('Cut date (index in series) is ', cut_date ,'(', cut_idx ,')')
print('Final date (index in series) is ', end_date ,'(', final_idx ,')')


print('Lenght in timesteps of the optimization period: ' + str(cut_idx - end_nn_train_idx))

alg = Alg.Algorithm(prices, volumes, memory, Mt, Dt, n, s, ga, gm, gp, pmax, itera, ncycles, init_nn_train_idx, end_nn_train_idx, cut_idx, final_idx, max_t)

start = timer()

print('Starting the simulation...')

pool, all_agents, wealth_end_cycle, statistics_opt, avg_wealth_t_test, avg_position_t_test, max_opt, min_opt = alg.run()

end = timer() - start

print('Duration of the execution: ' + str(end))

tmp = str(datetime.datetime.now())

directory = 'results/'+stock+' '+tmp

os.mkdir(directory)

last_price_opt = prices[cut_idx]
last_price_test = prices[final_idx]

p.save_histogram(all_agents, 'Number of agents by wealth - Histogram - Optimization', 25, directory+'/histogram-optimization-period.png')

p.save_histogram([a.get_wealth(last_price_test) for a in pool], 'Number of agents by wealth - Histogram - Test', 25, directory+'/histogram-test-period.png')


# Position + Price chart

fig, ax1 = plt.subplots()
color = 'black'
ax1.set_xlabel('Day')
ax1.set_ylabel('NKY Index')
ax1.plot(prices[cut_idx:final_idx], color=color)

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
ax1.plot(prices[cut_idx:final_idx], color=color)

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
