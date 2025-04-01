import click
import os
import pandas as pd

RES_DURATION = 8760

@click.command()
@click.argument('allocations_dir', type=click.Path(exists=False))
@click.option('--base_scenario',
              type=str,
              default='bias_0.0_sd_0.0')
@click.argument('results_path', type=click.Path(exists=False))
def main(allocations_dir, base_scenario, results_path):
    group_results(allocations_dir, base_scenario, RES_DURATION, results_path)

def group_results(allocations_dir, base_scenario, res_duration, results_path):
    base_scenario_path = f'{allocations_dir}/{base_scenario}'
    base_scenario_cost = get_scenario_cost(base_scenario_path, res_duration)

    results = {'bias_level': [base_scenario.split('_')[1]],
               'sd_level': [base_scenario.split('_')[3]],
               'cost': [base_scenario_cost],
               'relative_cost': [1]}

    for scenario in os.listdir(allocations_dir):
        if scenario == base_scenario: continue
        
        scenario_path = f'{allocations_dir}/{scenario}'
        scenario_cost = get_scenario_cost(scenario_path, res_duration)

        results['bias_level'].append(scenario.split('_')[1])
        results['sd_level'].append(scenario.split('_')[3])
        results['cost'].append(scenario_cost)
        results['relative_cost'].append(scenario_cost/base_scenario_cost)
    
    results_df = pd.DataFrame(results)
    results_df.sort_values(by=['sd_level', 'bias_level'])
    results_df.to_csv(results_path, index=False)
        
def get_scenario_cost(scenario_path, res_duration):
    scenario_cost = 0
    for family in os.listdir(scenario_path):
        family_path = f'{scenario_path}/{family}'
        cost_allocation = pd.read_csv(f'{family_path}/alloc_cost.csv')
        total_purchases_sp = pd.read_csv(f'{family_path}/total_purchases_sp.csv')

        on_demand_cost = sum(cost_allocation['OnDemand'])
        savings_plans_cost = sum(total_purchases_sp['value_reserves']) * res_duration
        family_cost = on_demand_cost + savings_plans_cost
        
        scenario_cost += family_cost
    
    return scenario_cost

if __name__ == '__main__':
    main()
