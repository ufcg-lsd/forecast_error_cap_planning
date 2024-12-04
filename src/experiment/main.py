import click
import os
import pandas as pd
from src.allocator.allocator_main import allocate, write_allocation, read_cost_allocation, read_demand, read_prices
from src.forecast_generation.main import generate_error_forecasts, read_error_configs

MARKET_OPTION = 'RNo'
ALLOC_METHOD = 2

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('error_configs_path', type=click.Path(exists=True))
@click.argument('cost_allocation_path', type=click.Path(exists=True))
@click.option('--reserve_duration', type=int, default=8760)
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, prices_path, error_configs_path, cost_allocation_path, reserve_duration, output_dir):
    experiment(demand_path, prices_path, error_configs_path, cost_allocation_path, reserve_duration, output_dir)

def experiment(demand_path, prices_path, error_configs_path, cost_allocation_path, reserve_duration, output_dir):
    forecasts_dir = f'{output_dir}/forecasts'
    os.mkdir(forecasts_dir)

    allocations_dir = f'{output_dir}/allocations'
    os.mkdir(allocations_dir)

    summary_df = pd.DataFrame(columns=['bias_level', 'sd_level', 'od_cost', 'sp_cost', 'total_cost'])

    error_configs = read_error_configs(error_configs_path)
    generate_error_forecasts(pd.read_csv(demand_path), error_configs, forecasts_dir)

    prices = read_prices(prices_path)
    cost_allocation = read_cost_allocation(cost_allocation_path)

    for filename in os.listdir(forecasts_dir):
        forecast_path = f'{forecasts_dir}/{filename}'
        
        config_name = '_'.join((filename.rstrip('.csv')).split('_')[1:])
        alloc_dir = f'{allocations_dir}/{config_name}'
        os.mkdir(alloc_dir)

        forecast_dem, timestamp = read_demand(forecast_path)
        
        instance_allocation, cost_allocation = allocate(forecast_dem, prices, cost_allocation, reserve_duration, MARKET_OPTION, ALLOC_METHOD)

        write_allocation(instance_allocation, cost_allocation, alloc_dir)

        config_name = config_name.split('_')
        summary_df.loc[len(summary_df)] = [config_name[1], config_name[3], sum(cost_allocation['OnDemand']), sum(cost_allocation[MARKET_OPTION]),
                                        (sum(cost_allocation['OnDemand']) + sum(cost_allocation[MARKET_OPTION]))]

    summary_df.to_csv(f'{allocations_dir}/summary.csv', index=False)

if __name__ == '__main__':
    main()