import click
from src.allocator import allocator_main

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('cost_allocation_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option('--res_duration',
              type=int,
              default=8760)
@click.option('--market_option',
              type=str,
              default='RNo')
@click.option('--alloc_method',
              type=int,
              default=1)
def main(demand_path, prices_path, cost_allocation_path, output_dir, res_duration, market_option, alloc_method):
    allocator_main.main(demand_path, prices_path, cost_allocation_path, output_dir, res_duration, market_option, alloc_method)

if __name__ == '__main__':
    main()