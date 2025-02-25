import click
import os
import pandas as pd

@click.command()
@click.argument('allocations_dir', type=click.Path(exists=False))
@click.option('--base_scenario',
              type=str,
              default='bias_0.0_sd_0.0')
@click.argument('results_path', type=click.Path(exists=False))
def main(allocations_dir, base_scenario, results_path):

    base_scenario_path = f'{allocations_dir}/{base_scenario}'
    base_scenario_cost = get_scenario_cost(base_scenario_path)

    results = {'bias_level': [base_scenario.split('_')[1]],
               'sd_level': [base_scenario.split('_')[3]],
               'cost': [base_scenario_cost],
               'relative_cost': [1]}

    for scenario in os.listdir(allocations_dir):
        if scenario == base_scenario: continue
        
        scenario_path = f'{allocations_dir}/{scenario}'
        scenario_cost = get_scenario_cost(scenario_path)

        results['bias_level'].append(scenario.split('_')[1])
        results['sd_level'].append(scenario.split('_')[3])
        results['cost'].append(scenario_cost)
        results['relative_cost'].append(scenario_cost/base_scenario_cost)
    
    results_df = pd.DataFrame(results)
    results_df.sort_values(by=['bias_level', 'sd_level'])
    results_df.to_csv(results_path, index=False)
        
def get_scenario_cost(scenario_path):
    scenario_cost = 0
    for family in os.listdir(scenario_path):
        family_path = f'{scenario_path}/{family}'
        cost_allocation = pd.read_csv(f'{family_path}/alloc_cost.csv')

        family_cost = sum(cost_allocation['AllMarkets'])
        scenario_cost += family_cost
    
    return scenario_cost

if __name__ == '__main__':
    main()
