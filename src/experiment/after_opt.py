import click
import os
import pandas as pd
from src.allocator import allocator_main

RES_DURATION = 8760
MARKET_OPTION = 'RNo'
ALLOC_METHOD = 1

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, prices_path, output_dir):
    alloc_results_path = f'{output_dir}/allocations'
    if not os.path.exists(alloc_results_path):
        os.mkdir(alloc_results_path)

    opt_results_path = f'{output_dir}/optimizations'

    for scenario in os.listdir(opt_results_path):
        scenario_path = f'{opt_results_path}/{scenario}'

        scenario_alloc_results_path = f'{alloc_results_path}/{scenario}'
        os.mkdir(scenario_alloc_results_path)

        for family in os.listdir(scenario_path):
            family_alloc_results_path = f'{alloc_results_path}/{scenario}/{family}'
            os.mkdir(family_alloc_results_path)
            
            total_purchases_sp = pd.read_csv(f'{scenario_path}/{family}/output/total_purchases_savings_plan.csv')
            
            num_rows = len(total_purchases_sp)
            cost_alloc_sp = pd.DataFrame({
                "timestamp": [i for i in range(num_rows)],
                "OnDemand": [0] * num_rows,
                "RAll": [0] * num_rows,
                "RPartialUp": [0] * num_rows,
                "RPartialHr": [0] * num_rows,
                "RNo": total_purchases_sp['value_active'].tolist(),
                "AllMarkets": total_purchases_sp['value_active'].tolist()
            })

            cost_allocation_path = f'{family_alloc_results_path}/purchases_sp.csv'
            cost_alloc_sp.to_csv(cost_allocation_path, index=False)
            allocator_main.main(demand_path, prices_path, cost_allocation_path, family_alloc_results_path, RES_DURATION, MARKET_OPTION, ALLOC_METHOD)
        