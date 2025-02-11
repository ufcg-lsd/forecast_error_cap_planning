import click
import pandas as pd
import os
from src.forecast_generation.main import read_error_configs, generate_error_forecasts
from src.experiment.set_opt_file_structure import set_up_multiple_scenarios

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('error_configs_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, prices_path, error_configs_path, output_dir):

    forecasts_dir = f'{output_dir}/forecasts'
    if not os.path.exists(forecasts_dir):
        os.mkdir(forecasts_dir)

    demand = pd.read_csv(demand_path)
    error_configs = read_error_configs(error_configs_path)
    generate_error_forecasts(demand, error_configs, forecasts_dir)

    optimizations_dir = f'{output_dir}/optimizations'
    if not os.path.exists(optimizations_dir):
        os.mkdir(optimizations_dir)
    set_up_multiple_scenarios(forecasts_dir, prices_path, optimizations_dir)

    print('Path for optimizations:', optimizations_dir)

if __name__ == '__main__':
    main()