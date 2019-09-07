import matplotlib.pyplot as plt
import numpy as np

# This module includes wrappers functions for the plotting functions used to present the results (using matplotlib).


def draw_neural_network_predictions(x, prediction, real_values, ylab, title, dst_full_path):

    plt.figure()
    plt.xlabel('Day')
    plt.ylabel(ylab)
    plt.plot(x, real_values, color='black')
    plt.plot(x, prediction, color='green')
    plt.title(title)
    plt.savefig(dst_full_path)


def save_histogram(data, title, bins, dst_full_path):

    """
    Args:
        data: An array of numerical data.
        title: Title of the histogram.
        bins: Number of bins in the histogram.
        dst_full_path: Full path where the histogram will be saved.
    """

    plt.figure()
    plt.xlabel('Wealth')
    plt.ylabel('Count')
    plt.hist(data, bins=bins, rwidth=0.9, color="red")
    plt.title(title)
    plt.savefig(dst_full_path)


def out_report(file, alg, statistics_opt, max_opt, min_opt, test_results, stock):

    """
    This method generates a summary report of the execution in the `file` given in as parameter.

    Args:
        file: File where the report will be generated.
        alg: Algorithm instance run.
        statistics_opt: Optimization statistics.
        max_opt: Maximum wealth after optimization.
        min_opt: Minimum wealth after optimization.
        test_results: Test results.
        stock: Stock name.
    """

    file.write('SUMMARY OF THE SIMULATION - STOCK: ' + str(stock)+ '\n')
    file.write('---------------------------------------------' + '\n')
    file.write('Length of the optimization period = ' + str(alg.cut_idx - alg.end_nn_train) + '\n')
    file.write('Length of the test period = ' + str(alg.final_idx - alg.cut_idx) + '\n')
    file.write('Number of agents = ' + str(alg.n) + '\n')
    file.write('Number of optimization cycles = ' + str(alg.ncycles) + '\n')
    file.write('Mutation rate (g_m)= ' + str(alg.gm) + '\n')
    file.write('Length of DGA round (g_a) = ' + str(alg.ga) + '\n')
    file.write('Number of strategies per agent = ' + str(alg.s) + '\n')
    file.write('T_max for strategies = ' + str(alg.max_t) + '\n')
    file.write('P_max per agent (Max position held) = ' + str(alg.pmax) + '\n\n')
    file.write('---------------------------------------------' + '\n')
    file.write('RESULTS:\n\n')
    file.write('Optimization PERIOD' + '\n')
    file.write("Stats OPT \ \n")

    for i in range(0, alg.ncycles):
        file.write("Cycle = " + str(i+1) + " Mean wealth = " + str(round(statistics_opt[i][0], 2)) +
                   " Std of wealth= " + str(statistics_opt[i][1]) + "\n")

    file.write('\n')
    file.write('Min wealth at end of OPT='+str(min_opt) +'\n')
    file.write('Max wealth at end of OPT='+str(max_opt) +'\n')
    file.write('Test PERIOD\n')
    file.write("Mean wealth test period = " + str(round(np.mean(test_results),2))+ '\n')
    file.write("Std of wealth test period = " + str(round(np.std(test_results), 2)) + '\n')
    file.close()

