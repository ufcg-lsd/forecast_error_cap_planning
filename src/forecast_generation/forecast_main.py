""" Creates simulated forecasts with error given a demand.

Receives the real future demand and a set of error configurations.
Those error configurations consist of a bias level and a standard
deviation level. For each configuration, creates a variation of the
real demand by adding the two error variables. Writes each forecasted
demand as csv file.
"""

import pandas as pd
import numpy as np

class ErrorConfig:
    def __init__(self, bias_level, sd_level):
        self.bias_level = bias_level
        self.sd_level = sd_level
    
    def to_string(self):
        return f'bias_{self.bias_level}_sd_{self.sd_level}'

def main(demand_path, error_configs_path, error_option, output_dir):
    demand = pd.read_csv(demand_path)
    error_configs = read_error_configs(error_configs_path)
    generate_error_forecasts(demand, error_configs, error_option, output_dir)

def generate_error_forecasts(demand, error_configs, error_option, output_dir):
    """
    Create the demands with errors and saves them as csv files, given a list of error configs. 
    """

    size = len(demand[demand.keys()[0]])
    snormal = get_snormal(size)

    for error_config in error_configs:
        new_demand = add_error(demand, error_config.bias_level, error_config.sd_level, error_option, snormal)
        new_demand.to_csv(f'{output_dir}/demand_{error_config.to_string()}.csv', index=False)

def add_error(demand, bias_level, sd_level, error_option, global_snormal):
    """
    Adds error to a demand, given one level of bias and one level of deviation.
    """

    new_demand = pd.DataFrame()
    for instance_type in demand:
        if instance_type in ['timestamp', 'hour']:
            new_demand[instance_type] = demand[instance_type]
        else:
            match error_option:
                case 1:
                    snormal = get_snormal(len(demand[instance_type]))
                    new_demand[instance_type] = round(demand[instance_type] * (1 + bias_level + sd_level * snormal))
                case 2:
                    snormal = get_snormal(len(demand[instance_type]))
                    new_demand[instance_type] = round(demand[instance_type] * (1 + bias_level) * (1 + (sd_level * snormal)))
                case 3:
                    new_demand[instance_type] = round(demand[instance_type] * (1 + bias_level + sd_level * global_snormal))
                case 4:
                    new_demand[instance_type] = round(demand[instance_type] * (1 + bias_level) * (1 + (sd_level * global_snormal)))

    return new_demand

def get_snormal(size):
    return np.random.normal(loc=0, scale=1, size=size)

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