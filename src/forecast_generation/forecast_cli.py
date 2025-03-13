import click
from src.forecast_generation import forecast_main

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('error_configs_path', type=click.Path(exists=True))
@click.option('--error_option',
              type=int,
              default=1)
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, error_configs_path, error_option, output_dir):
    forecast_main.main(demand_path, error_configs_path, error_option, output_dir)
    
if __name__ == '__main__':
    main()