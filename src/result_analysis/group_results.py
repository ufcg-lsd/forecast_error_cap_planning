""" For each scenario, groups the results.

    Each scenario has dozens of different instance families, each one with
    different optimization results. This scripts groups the results in each
    instance family, in order to have only one file of each type for each
    different scenario, helping to analyse the results.
"""

import os
import click
import pandas as pd
from util.aux import read_prices

DURATION = 8760

def _initialize_alloc_cost():
    return pd.DataFrame({
        'timestamp': [i for i in range(DURATION)],
        'OnDemand': [0] * DURATION,
        'RAll': [0] * DURATION,
        'RPartialUp': [0] * DURATION,
        'RPartialHr': [0] * DURATION,
        'RNo': [0] * DURATION,
        'AllMarkets': [0] * DURATION
    })

def _initialize_sp_usage():
    return pd.DataFrame({
        'timestamp': [i for i in range(DURATION)],
        'value_used': [0] * DURATION
    })

ALLOC_COST = _initialize_alloc_cost()

SP_USAGE = _initialize_sp_usage()

@click.command()
@click.argument('results_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option(
    '--prices_path',
    type=click.Path(exists=True),
    help='Path to the prices data file. This is required if processing "sp_usage" or "all".'
)
@click.option(
    '--process',
    type=click.Choice(['allocations', 'demand', 'sp_usage', 'all'], case_sensitive=False),
    default='all',
    help='Specify which part of the data to process. Defaults to "all".'
)
def main(results_dir, output_dir, prices_path, process):
    """
    Group the results from each scenario.

    RESULTS_DIR: The directory containing the results to be grouped.
    OUTPUT_DIR: The directory where the grouped results will be stored.
    """
    if process in ['allocations', 'all']:
        group_allocations(results_dir, output_dir)

    if process in ['demand', 'all']:
        group_demand(results_dir, output_dir)
    
    if process in ['sp_usage', 'all']:
        if not prices_path:
            raise click.UsageError("The --prices_path option is required when processing 'sp_usage' or 'all'.")
        group_sp_usage(results_dir, output_dir, prices_path)

# Allocation

def group_allocations(results_dir, output_dir):
    allocations_dir = os.path.join(results_dir, 'allocations')

    for scenario in os.listdir(allocations_dir):
        scenario_dir = os.path.join(allocations_dir, scenario)
        iterate_allocations(scenario_dir)
        write_output(output_dir, scenario)
        clear_alloc_cost()

def iterate_allocations(scenario_dir):
    global ALLOC_COST
    for family in os.listdir(scenario_dir):
        family_dir = os.path.join(scenario_dir, family)
        alloc_cost_path = os.path.join(family_dir, 'alloc_cost.csv')
        alloc_cost_family = pd.read_csv(alloc_cost_path)
        
        for col in ALLOC_COST.columns:
            if col != 'timestamp':
                ALLOC_COST[col] += alloc_cost_family[col]
    
def write_output(output_dir, scenario):
    ALLOC_COST.to_csv(os.path.join(output_dir, f'alloc_cost_{scenario}.csv'), index=False)

def clear_alloc_cost():
    global ALLOC_COST
    ALLOC_COST = _initialize_alloc_cost()

# Savings Plans Usage

def group_sp_usage(results_dir, output_dir, prices_path):
    prices = read_prices(prices_path)
    allocations_dir = os.path.join(results_dir, 'allocations')

    for scenario in os.listdir(allocations_dir):
        scenario_dir = os.path.join(allocations_dir, scenario)
        iterate_sp_usage(scenario_dir, prices)
        write_output(output_dir, scenario)
        clear_alloc_cost()

def iterate_sp_usage(scenario_dir, prices):
    global SP_USAGE
    for family in os.listdir(scenario_dir):
        family_dir = os.path.join(scenario_dir, family)
        alloc_instance_path = os.path.join(family_dir, 'alloc_instance.csv')
        alloc_instance_family = pd.read_csv(alloc_instance_path)

        alloc_instance_sp = alloc_instance_family[alloc_instance_family['market'] == 'r_no']
        alloc_instance_sp = alloc_instance_sp.reset_index(drop=True)

        #sp_prices = {key: obj.hr_no_upfront for key, obj in prices.items()}

        cols_inst_types = alloc_instance_sp.columns[2:]
        for col in cols_inst_types:
            SP_USAGE['value_used'] += alloc_instance_sp[col] * prices[col].hr_no_upfront


        #alloc_values_sp = alloc_instance_sp[cols_inst_types] * sp_prices
        #alloc_values_sp['value_used'] = alloc_values_sp.iloc[:, 1:].sum(axis=1)
        #SP_USAGE['value_used'] += alloc_values_sp['value_used']

def write_output(output_dir, scenario):
    SP_USAGE.to_csv(os.path.join(output_dir, f'sp_usage_{scenario}.csv'), index=False)

def clear_sp_usage():
    global SP_USAGE
    SP_USAGE = _initialize_sp_usage()

# Demand (or forecasts)

def group_demand(results_dir, output_dir):
    demand_dir = os.path.join(results_dir, 'forecasts')

    for scenario in os.listdir(demand_dir):
        scenario_demand_path = os.path.join(demand_dir, scenario)
        scenario_demand = pd.read_csv(scenario_demand_path)
        scenario_demand['num_instances'] = scenario_demand.iloc[:, 1:].sum(axis=1)
        scenario_demand[['timestamp', 'num_instances']].to_csv(os.path.join(output_dir, f'{scenario}.csv'), index=False)

if __name__ == '__main__':
    main()