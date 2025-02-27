import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    results_path = sys.argv[1]
    results = pd.read_csv(results_path)

    results_sd_0 = results[results['sd_level'] == 0]
    results_sd_005 = results[results['sd_level'] == 0.05]
    results_sd_01 = results[results['sd_level'] == 0.1]

    results_sd_0 = results_sd_0.sort_values(by=['bias_level'])
    results_sd_005 = results_sd_005.sort_values(by=['bias_level'])
    results_sd_01 = results_sd_01.sort_values(by=['bias_level'])

    plt.plot(results_sd_0['bias_level'], results_sd_0['relative_cost'], marker='o', linestyle='-', label=f'sd_level={0}', color='gold')
    plt.plot(results_sd_005['bias_level'], results_sd_005['relative_cost'], marker='o', linestyle='-', label=f'sd_level={0.05}', color='orange')
    plt.plot(results_sd_01['bias_level'], results_sd_01['relative_cost'], marker='o', linestyle='-', label=f'sd_level={0.1}', color='orangered')

    plt.xlabel('Bias Level')
    plt.ylabel('Relative Cost')
    plt.title('Impact of Forecast Error in Cost')
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()
