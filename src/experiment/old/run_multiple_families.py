import os
import click
import pandas as pd
from src.experiment.main import experiment

RES_DURATION = 8760

@click.command()
@click.argument('families_path', type=click.Path(exists=False))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('error_configs_path', type=click.Path(exists=True))
def main(families_path, prices_path, error_configs_path):
    summary = pd.DataFrame(columns=['family','bias_level','sd_level','od_cost','sp_cost','total_cost'])
    
    for family in os.listdir(families_path):
        if os.path.isdir( f'{families_path}/{family}'):
            demand_path = f'{families_path}/{family}/input/demand.csv'
            cost_allocation_path = f'{families_path}/{family}/input/cost_allocation.csv'
            output_dir = f'{families_path}/{family}/output'
            experiment(demand_path, prices_path, error_configs_path, cost_allocation_path, RES_DURATION, output_dir)
            
            family_summary = pd.read_csv(f'{families_path}/{family}/output/allocations/summary.csv')
            
            family_summary['family'] = family
            summary = pd.concat([summary, family_summary], ignore_index=True)
            
    summary.to_csv(f'{families_path}/detailed_summary.csv', index=False)
    
    summary = summary.drop(['family'], axis=1)
    summary = summary.groupby(['bias_level','sd_level']).sum()
    
    summary = summary.sort_values(by='total_cost')
    
    summary.to_csv(f'{families_path}/summary.csv', index=False)

if __name__ == '__main__':
    main()