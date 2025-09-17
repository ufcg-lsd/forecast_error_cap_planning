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
        'sp_idle': [],
        'total_used': []
    })

@click.command()
@click.argument('results_dir', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(exists=False))
@click.argument('prices_path', type=click.Path(exists=False))
@click.option('--res_duration',
              type=int,
              default=8760)
@click.option('--base_scenario',
              type=str,
              default='bias_0.0_sd_0.0')
@click.option(
    '--process',
    type=click.Choice(['abs_costs', 'relative_costs', 'all'], case_sensitive=False),
    default='all',
    help='Specify which data should be processed. Defaults to "all".'
)
def main(results_dir, output_file, prices_path, res_duration, base_scenario, process):
    prices = read_prices(prices_path)
    results_df = _initialize_results_summary()

    results_dir = os.path.join(results_dir, 'allocations')
    
    for scenario in os.listdir(results_dir):
        scenario_path = os.path.join(results_dir, scenario)
        results_df = get_scenario_info(scenario_path, res_duration, prices, results_df)
    
    if process in ['relative_costs', 'all']:
        results_df = get_relative_costs(results_df, base_scenario)
        if process == 'relative_costs':
            results_df = results_df.drop(columns=['total_cost', 'od_cost', 'sp_cost', 'sp_used', 'sp_idle', 'total_used'])

    results_df = results_df.sort_values(by=['bias_level', 'sd_level'])
    results_df.to_csv(output_file, index=False)

def get_scenario_info(scenario_path, res_duration, prices, results_df):
    od_cost, sp_cost, sp_used, sp_idle = 0, 0, 0, 0

    for family in os.listdir(scenario_path):
        family_path = os.path.join(scenario_path, family)
        family_od_cost, family_sp_cost, family_sp_used, family_sp_idle = process_family_costs(family_path, res_duration, prices)
        od_cost += family_od_cost
        sp_cost += family_sp_cost
        sp_used += family_sp_used
        sp_idle += family_sp_idle

    total_cost = od_cost + sp_cost
    total_used = sp_used + od_cost

    results_df.loc[len(results_df)] = [
        scenario_path.split('/')[-1].split('_')[1],
        scenario_path.split('/')[-1].split('_')[3],
        total_cost,
        od_cost,
        sp_cost,
        sp_used,
        sp_idle,
        total_used
    ]

    return results_df

def process_family_costs(family_path, res_duration, prices):
    cost_allocation = pd.read_csv(os.path.join(family_path, 'alloc_cost.csv'))
    total_purchases_sp = pd.read_csv(os.path.join(family_path, 'total_purchases_sp.csv'))
    alloc_instance_family = pd.read_csv(os.path.join(family_path, 'alloc_instance.csv'))

    on_demand_cost = cost_allocation['OnDemand'].sum()
    savings_plans_cost = total_purchases_sp['value_reserves'].sum() * res_duration

    alloc_instance_sp = alloc_instance_family[alloc_instance_family['market'] == 'r_no']

    if not alloc_instance_sp.empty:
        inst_cols = alloc_instance_sp.columns[2:]
        sp_used = (alloc_instance_sp[inst_cols] * [prices[c].hr_no_upfront for c in inst_cols]).to_numpy().sum()
    else:
        sp_used = 0

    sp_idle = savings_plans_cost - sp_used

    return on_demand_cost, savings_plans_cost, sp_used, sp_idle

def get_relative_costs(results_df, base_scenario):
    base_scenario_row = results_df[(results_df['bias_level'] == base_scenario.split('_')[1]) & (results_df['sd_level'] == base_scenario.split('_')[3])]
    if base_scenario_row.empty:
        raise ValueError(f"Base scenario '{base_scenario}' not found in the results.")
    
    base_sp_idle = base_scenario_row['sp_idle'].values[0]
    base_total_used = base_scenario_row['total_used'].values[0]
    base_total_cost = base_scenario_row['total_cost'].values[0]

    results_df['diff_sp_idle'] = results_df['sp_idle'] - base_sp_idle
    results_df['diff_total_used'] = results_df['total_used'] - base_total_used
    results_df['diff_total_cost'] = results_df['total_cost'] - base_total_cost

    results_df['rel_sp_idle'] = round((results_df['diff_sp_idle'] / base_sp_idle) * 100, 2) if base_sp_idle != 0 else float('nan')
    results_df['rel_total_used'] = round((results_df['diff_total_used'] / base_total_used) * 100, 2) if base_total_used != 0 else float('nan')

    results_df['rel_tc_sp_idle'] = round((results_df['diff_sp_idle'] / base_sp_idle) * 100, 2) if base_sp_idle != 0 else float('nan')
    results_df['rel_tc_total_used'] = round((results_df['diff_total_used'] / base_total_used) * 100, 2) if base_total_used != 0 else float('nan')
    results_df['rel_total_cost'] = round((results_df['diff_total_cost'] / base_total_cost) * 100, 2) if base_total_cost != 0 else float('nan')

    return results_df

if __name__ == '__main__':
    main()