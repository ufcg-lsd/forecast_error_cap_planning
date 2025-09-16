""" Summarize results of an execution.

    Creates a CSV file with the results of each scenario. Contains the costs for all markets,
    on-demand, savings plans used and savings plans idle, both absolute and relative to the 
    base scenario.
"""

import click
import os
import pandas as pd
from util.aux import read_prices

def _initialize_results_summary():
    return pd.DataFrame({
        'bias_level': [],
        'sd_level': [],
        'total_cost': [],
        'od_cost': [],
        'sp_cost': [],
        'sp_used': [],
        'sp_idle': []
    })

@click.command()
@click.argument('results_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.argument('prices_path', type=click.Path(exists=False))
def main(results_dir, output_dir, prices_path,):
    prices = read_prices(prices_path)
    results_df = _initialize_results_summary()

    results_dir = f'{results_dir}/allocations'
    
    for scenario in os.listdir(results_dir):
        scenario_path = f'{results_dir}/{scenario}'
        results_df = get_scenario_info(scenario_path, 8760, prices, results_df)

    results_df.to_csv(f'{output_dir}/summary_results.csv', index=False)

def get_scenario_info(scenario_path, res_duration, prices, results_df):
    all_markets_cost = 0
    od_cost = 0
    sp_cost = 0
    sp_used = 0
    sp_idle = 0

    for family in os.listdir(scenario_path):
        family_path = f'{scenario_path}/{family}'
        family_od_cost, family_sp_cost, family_sp_used, family_sp_idle = process_family_costs(family_path, res_duration, prices)
        od_cost += family_od_cost
        sp_cost += family_sp_cost
        sp_used += family_sp_used
        sp_idle += family_sp_idle

    all_markets_cost = od_cost + sp_cost

    results_df.loc[len(results_df)] = [
        scenario_path.split('/')[-1].split('_')[1],
        scenario_path.split('/')[-1].split('_')[3],
        all_markets_cost,
        od_cost,
        sp_cost,
        sp_used,
        sp_idle
    ]

    return results_df

def process_family_costs(family_path, res_duration, prices):
    cost_allocation = pd.read_csv(f'{family_path}/alloc_cost.csv')
    total_purchases_sp = pd.read_csv(f'{family_path}/total_purchases_sp.csv')
    alloc_instance_family = pd.read_csv(f'{family_path}/alloc_instance.csv')

    on_demand_cost = sum(cost_allocation['OnDemand'])
    savings_plans_cost = sum(total_purchases_sp['value_reserves']) * res_duration

    alloc_instance_sp = alloc_instance_family[alloc_instance_family['market'] == 'r_no'].reset_index(drop=True)
    cols_inst_types = alloc_instance_sp.columns[2:]
    
    sp_used = 0
    for col in cols_inst_types:
        sp_used += sum(alloc_instance_sp[col]) * prices[col].hr_no_upfront

    sp_idle = savings_plans_cost - sp_used

    return on_demand_cost, savings_plans_cost, sp_used, sp_idle

# total_cost, od_cost, sp_cost 
# sp_used, sp_idle

if __name__ == '__main__':
    main()