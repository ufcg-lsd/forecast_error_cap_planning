import click
import os
from src.forecast_generation import forecast_main
from src.experiment.aux.set_opt_file_structure import set_up_multiple_scenarios

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('error_configs_path', type=click.Path(exists=True))
@click.option('--res_duration',
              type=int,
              default=8760)
@click.option('--error_option',
              type=int,
              default=1)
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, prices_path, error_configs_path, res_duration, error_option, output_dir):

    forecasts_dir = f'{output_dir}/forecasts'
    if not os.path.exists(forecasts_dir):
        os.mkdir(forecasts_dir)

    forecast_main.main(demand_path, error_configs_path, error_option, forecasts_dir)

    optimizations_dir = f'{output_dir}/optimizations'
    if not os.path.exists(optimizations_dir):
        os.mkdir(optimizations_dir)
    set_up_multiple_scenarios(forecasts_dir, prices_path, res_duration, optimizations_dir)

    print('Path for optimizations:', optimizations_dir)

if __name__ == '__main__':
    main()
