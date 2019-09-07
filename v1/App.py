import src.Data as dat
import src.Algorithm as Alg
import src.Functions as f
import src.Plotting as p
import datetime
import os
import matplotlib.pyplot as plt
from timeit import default_timer as timer

def main():

    print("================================")
    print("        AIStocksAgents-v1       ")
    print("================================")
    print("Select source .csv file (/full/path/to/file):")
    file = input().strip()
    print("Select initial date of optimization period (same format as in .csv files):")
    initial_date = input().strip()
    print("Select cut date of optimization period (same format as in .csv files):")
    cut_date = input().strip()
    print("Select end date of test period (same format as in .csv files):")
    end_date = input().strip()
    print("Select number of optimzation cycles:")
    ncycles = int(input().strip())
    print("Select foder where results will be stored (/full/path/to/folder):")
    results = input().strip()


    n = 1000                        # n: Number of agents
    s = 8                            # s: Number of strategies per agent
    g_a = 60                         # g_a: DGA rounds length
    g_m = 0.5                        # g_m: Mutation rate
    g_p = 8                          # g_p: Size of the communication pool
    p_max = 10                       # p_max: Max position held by agent
    max_t = 20

    df = dat.get_pandas_dataframe(file, 'Open').drop(columns=['index'])

    prices = list(df.Price.values)
    dates = list(df.Date.values)
    Mt = list(df.Mt.values)
    Dt = list(df.Dt.values)
    Yt = list(df.Yt.values)

    initial_idx = dates.index(initial_date)
    cut_idx = dates.index(cut_date)
    end_idx = dates.index(end_date)

    print('Initial date (index in series) is ' + initial_date + '(' + str(initial_idx)+')')
    print('Cut date (index in series) is ' + cut_date + '(' + str(cut_idx)+')')
    print('End date (index in series) is ' + end_date + '(' + str(end_idx)+')')

    print('Lenght in timesteps of the optimization period: ' + str(cut_idx - initial_idx))
    print('Lenght in timesteps of the test period: ' + str(end_idx - cut_idx))


    alg = Alg.Algorithm(prices, Mt, Dt, Yt, n, s, g_a, g_m, g_p, p_max, ncycles, initial_idx, cut_idx, end_idx, max_t)
    start = timer()

    print('Starting the simulation...')
    pool, all_agents, statistics_opt, avg_wealth_t_test, avg_position_t_test, max_opt, min_opt = alg.run()

    end = timer() - start

    print('Duration of the execution ', f.normalize_seconds(end))

    tmp = str(datetime.datetime.now())

    directory = results+'/'+tmp

    os.mkdir(directory)

    last_price_opt = prices[cut_idx]
    last_price_test = prices[end_idx]

    p.save_histogram(all_agents, 'Number of agents by wealth - Histogram - Optimization', 25, directory+'/histogram-optimization-period.png')

    p.save_histogram([a.get_wealth(last_price_test) for a in pool], 'Number of agents by wealth - Histogram - Test', 25, directory+'/histogram-test-period.png')

    # Position + Price chart

    plt.rcParams["figure.figsize"] = (12,8)


    fig, ax1 = plt.subplots()
    color = 'black'
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Stcok')
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
    ax1.set_ylabel('Stock')
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

    p.out_report(file, alg, statistics_opt, max_opt, min_opt, test_result, 'Stock')


if __name__ == '__main__':
    main()
