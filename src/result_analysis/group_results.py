""" For each scenario, groups the results.
"""

import os
import click
import pandas as pd

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

ALLOC_COST = _initialize_alloc_cost()

@click.command()
@click.argument('results_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option(
    '--process',
    type=click.Choice(['allocations', 'demand', 'all'], case_sensitive=False),
    default='all',
    help='Specify which part of the data to process. Defaults to "all".'
)
def main(results_dir, output_dir, process):
    if process in ['allocations', 'all']:
        group_allocations(results_dir, output_dir)

    if process in ['demand', 'all']:
        group_demand(results_dir, output_dir)


def group_allocations(results_dir, output_dir):
    allocations_dir = os.path.join(results_dir, 'allocations')

    for scenario in os.listdir(allocations_dir):
        scenario_dir = os.path.join(allocations_dir, scenario)
        iterate(scenario_dir)
        write_output(output_dir, scenario)
        clear_alloc_cost()

def iterate(scenario_dir):
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

def group_demand(results_dir, output_dir):
    demand_dir = os.path.join(results_dir, 'forecasts')

    for scenario in os.listdir(demand_dir):
        scenario_demand_path = os.path.join(demand_dir, scenario)
        scenario_demand = pd.read_csv(scenario_demand_path)
        scenario_demand['num_instances'] = scenario_demand.iloc[:, 1:].sum(axis=1)
        scenario_demand[['timestamp', 'num_instances']].to_csv(os.path.join(output_dir, f'{scenario}.csv'), index=False)

if __name__ == '__main__':
    main()