import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    results_path = sys.argv[1]
    results = pd.read_csv(results_path)

    sd_levels = sorted(list(set(results['sd_level'])))
    colors = ['gold', 'orange', 'orangered']

    for i in range(len(sd_levels)):
        sd_level = sd_levels[i]
        results_sd_level = results[results['sd_level'] == sd_level]
        results_sd_level = results_sd_level.sort_values(by=['bias_level'])
        plt.plot(results_sd_level['bias_level'], results_sd_level['relative_cost'], marker='o', linestyle='-', label=f'sd_level={sd_level}', color=colors[i])

    plt.xlabel('Bias Level')
    plt.ylabel('Relative Cost')
    plt.title('Impact of Forecast Error in Cost')
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()
