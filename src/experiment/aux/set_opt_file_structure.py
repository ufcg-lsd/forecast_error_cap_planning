import os
import sys
import pandas as pd
from src.allocator.allocator_aux import read_prices, read_demand

RES_DURATION = 8760
MARKET_OPTION = 'RNo'

def main():
    output_path = sys.argv[1]
    demand_dir = sys.argv[2]
    prices_path = sys.argv[3]

    set_up_multiple_scenarios(demand_dir, prices_path, output_path)
    
def set_up_multiple_scenarios(demand_dir, prices_path, output_path):
    prices = read_prices(prices_path)

    for demand_path in os.listdir(demand_dir):
        if demand_path[-4:] == '.csv':
            scenario_name = demand_path[7:-4]
            scenario_path = f'{output_path}/{scenario_name}'
            set_up_scenario(prices, f'{demand_dir}/{demand_path}', scenario_path)

def set_up_scenario(prices, demand_path, scenario_path):
    os.mkdir(scenario_path)
    demand, timestamp = read_demand(demand_path)
    families = get_families(demand)
    families = select_types(families, prices)

    for family in families:
        instance_types = families[family]

        os.mkdir(f'{scenario_path}/{family}')
        os.mkdir(f'{scenario_path}/{family}/output')

        od_config = {'instance': [], 'hourly_price': []}
        sp_config = {'instance': [], 'hourly_price': [], 'duration': []}

        for instance_type in instance_types:
            od_config['instance'].append(instance_type)
            od_config['hourly_price'].append(prices[instance_type].on_demand)

            sp_config['instance'].append(instance_type)
            sp_config['hourly_price'].append(get_effective_hourly_rate(prices[instance_type], MARKET_OPTION, RES_DURATION))
            sp_config['duration'].append(RES_DURATION)
        
        
        od_config_df = pd.DataFrame(od_config)
        od_config_df.to_csv(f'{scenario_path}/{family}/on_demand_config.csv', index=False)

        sp_config_df = pd.DataFrame(sp_config)
        sp_config_df.to_csv(f'{scenario_path}/{family}/savings_plan_config.csv', index=False)

        sel_demand = {key: demand[key] for key in instance_types}
        sel_demand_df = pd.DataFrame(sel_demand)
        sel_demand_df.insert(0, 'hour', timestamp['timestamp'])
        sel_demand_df.to_csv(f'{scenario_path}/{family}/total_demand.csv', index=False)

def get_families(demand):
    families = {}
    for instance_type in demand:
        if len(instance_type.split('.')) == 1:
            family = instance_type
        else: 
            family, type = instance_type.split('.')
        if family in families:
            families[family].append(instance_type)
        else:
            families[family] = [instance_type]
    return families

def select_types(families, prices):
    new_families = {}
    for family in families:
        instance_types = families[family]
        for instance_type in instance_types:
            if instance_type in prices.keys():
                if family in new_families: 
                    new_families[family].append(instance_type)
                else:
                    new_families[family] = [instance_type]
    
    return new_families

def get_effective_hourly_rate(instance_price, market, res_duration):
    match market:
        case 'OnDemand':
            return instance_price.on_demand
        case 'RAll':
            return instance_price.up_all_upfront / res_duration
        case 'RPartial':
            return (instance_price.up_partial_upfront / res_duration) + instance_price.hr_partial_upfront
        case 'RNo':
            return instance_price.hr_no_upfront


if __name__ == '__main__':
    main()