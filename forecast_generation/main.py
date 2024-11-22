import click
import pandas as pd
import numpy as np

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
def main(demand_path, output_dir):
    demand = pd.read_csv(demand_path)

    generate_error_forecasts(demand, error_configs, output_dir)

def generate_error_forecasts(demand, error_configs, output_dir):
    for error_config in error_configs:
        new_demand = add_error(demand, error_config.bias_level, error_config.sd_level)
        new_demand.to_csv(f'{output_dir}/demand_{error_config.to_string()}.csv', index=False)

def add_error(demand, bias_level, sd_level):
    snormal = np.random.normal(loc=0, scale=1)
    #nesse caso, o desvio é exatamente igual para todas horas
    new_demand = demand * (1 + (bias_level / 100) + sd_level * snormal)
    new_demand = demand * (1 + (bias_level / 100)) * (1 + (sd_level * snormal))

    return new_demand    

if __name__ == '__main__':
    main()

class ErrorConfig:
    def __init__(self, bias_level, sd_level):
        self.bias_level = bias_level
        self.sd_level = sd_level
    
    def to_string(self):
        return f'bias_{self.bias_level}_sd_{self.sd_level}'