""" Calculates the results with the relative cost compared to the optimization cost
"""

import click
import os
import pandas as pd

@click.command()
@click.argument('results_file_path', type=click.Path(exists=True))
@click.argument('optimizations_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=True))
@click.option('--base_scenario',
              type=str,
              default='bias_0.0_sd_0.0')
def main(results_file_path, optimizations_dir, output_dir, base_scenario):

    base_scenario_opt_path = os.path.join(optimizations_dir, base_scenario)
    total_opt_cost = 0

    for family in os.listdir(base_scenario_opt_path):
        family_opt_cost = get_opt_cost(family, base_scenario_opt_path)
        total_opt_cost += family_opt_cost
    
    results_df = pd.read_csv(results_file_path)
    results_df["relative_cost"] = results_df["cost"] / total_opt_cost

    new_row = pd.DataFrame([{'bias_level': 0, 'sd_level': 0, 'cost': total_opt_cost, 'relative_cost': 1}])
    results_df = pd.concat([new_row, results_df], ignore_index=True)

    results_df.to_csv(os.path.join(output_dir, 'resuts_comp_opt.csv'), index=False)
    
def get_opt_cost(family, base_scenario_opt_path):
    results_opt_dir = os.path.join(base_scenario_opt_path, family)
    results_opt_path = os.path.join(results_opt_dir, 'output/result_cost.csv')
    results_opt = pd.read_csv(results_opt_path)
    total_opt_cost = results_opt.loc[0, 'total_cost']

    return total_opt_cost

if __name__ == '__main__':
    main()
