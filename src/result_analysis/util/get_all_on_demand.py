import sys
import pandas as pd
from aux import read_demand, read_prices, get_families, select_types

def main():
    demand_path = sys.argv[1]
    prices_path = sys.argv[2]

    total_demand, timestamp = read_demand(demand_path)
    prices = read_prices(prices_path)

    total_duration = len(timestamp['timestamp'])

    families = get_families(total_demand)
    families = select_types(families, prices)

    total_sum = 0
    for family in families:
        instance_types = families[family]
        demand = {key: total_demand[key] for key in instance_types}
        family_sum = sum_demand(demand, prices, total_duration)
        total_sum += family_sum
        print(family, family_sum)

    print('total', total_sum)

def sum_demand(demand, prices, duration):
    total_sum = 0
    for instance_type in demand:
        instance_demand = demand[instance_type]
        
        hourly_price = prices[instance_type].on_demand

        for i in range(len(instance_demand)):
            total_sum += instance_demand[i] * hourly_price
    
    return total_sum

if __name__ == '__main__':
    main()