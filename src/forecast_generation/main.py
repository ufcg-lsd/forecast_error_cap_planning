import click
import math
import pandas as pd
import numpy as np

class ErrorConfig:
    def __init__(self, bias_level, sd_level):
        self.bias_level = bias_level
        self.sd_level = sd_level
    
    def to_string(self):
        return f'bias_{self.bias_level}_sd_{self.sd_level}'

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('error_configs_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, error_configs_path, output_dir):
    demand = pd.read_csv(demand_path)
    error_configs = read_error_configs(error_configs_path)
    generate_error_forecasts(demand, error_configs, output_dir)

def generate_error_forecasts(demand, error_configs, output_dir):
    """
    Create the demands with errors and saves them as csv files, given a list of error configs. 
    """

    for error_config in error_configs:
        new_demand = add_error(demand, error_config.bias_level, error_config.sd_level)
        new_demand.to_csv(f'{output_dir}/demand_{error_config.to_string()}.csv', index=False)

def add_error(demand, bias_level, sd_level):
    """
    Adds error to a demand, given one level of bias and one level of deviation.
    """

    new_demand = pd.DataFrame()
    for instance_type in demand:
        snormal = np.random.normal(loc=0, scale=1, size=len(demand[instance_type]))
        new_demand[instance_type] = demand[instance_type] * (1 + bias_level + sd_level * snormal)

        new_demand[instance_type] = np.ceil(new_demand[instance_type].round(2)).astype(int)

        #new_demand[instance_type] = demand[instance_type] * (1 + (bias_level / 100) + sd_level * snormal)
        #new_demand[instance_type] = demand[instance_type] * (1 + (bias_level / 100)) * (1 + (sd_level * snormal))

    return new_demand    

def read_error_configs(error_configs_path):
    """
    Reads the csv file with the error configs as a list of objects of ErrorConfig.
    """

    error_configs_df = pd.read_csv(error_configs_path)
    error_configs = []

    for _, row in error_configs_df.iterrows():
        error_config = ErrorConfig(row['bias_level'], row['sd_level'])
        error_configs.append(error_config)

    return error_configs

if __name__ == '__main__':
    main()