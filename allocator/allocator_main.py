import click
import pandas as pd
from allocator_aux import InstancePrices

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('cost_allocation_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option('--res_duration',
              type=int,
              default=8760)
def main(demand_path, prices_path, cost_allocation_path, output_dir, res_duration):
    demand = read_demand(demand_path)
    prices = read_prices(prices_path)
    available_savings_plans = read_savings_plans(cost_allocation_path, res_duration)

    instance_allocation, cost_allocation = allocate(demand, prices, available_savings_plans, res_duration)
    
    write_allocation(instance_allocation, cost_allocation, output_dir)

def allocate(demand, prices, available_savings_plans):
    instance_allocation = 

    update_cost_allocation()
    return 

def read_demand(demand_path):
    demand = {}
    with open(demand_path, mode='r') as file:
            header = file.readline().split(',')

            # put the instance types in a dictionary
            for i in range(0, len(header)):
                instance_type = header[i].strip('\n').strip('"')
                demand[instance_type] = []
            
            # iterates over the file to create the datasets of each type
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.split(',')

                for i in range(0, len(line)):
                    instance_type = header[i].strip('\n').strip('"')
                    demand[instance_type].append(int(line[i]))

    timestamp = {'timestamp': demand['timestamp']}
    demand.pop('timestamp')

    return demand, timestamp

def read_prices(self, prices_path):
    prices = {}
    with open(prices_path, mode='r') as file:
            header = file.readline().split(',')
            
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.split(',')
                
                instance_type = line[0]
                on_demand_hour = float(line[1])
                up_all_upfront = float(line[2])
                up_partial_upfront = float(line[3])
                hr_partial_upfront = float(line[4])
                hr_no_upfront = float(line[5])

                prices[instance_type] = InstancePrices(on_demand_hour, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront)
    return prices

def read_savings_plans(cost_allocation_path, res_duration):
    available_savings_plans = []
    with open(cost_allocation_path, mode='r') as file:
        header = file.readline().split(',')
        current_t = 0

        while True:
            line = file.readline()
            if not line:
                break
            line = line.split(',')

            up_all_upfront = float(line[2])
            up_partial_upfront = float(line[3])
            hr_partial_upfront = float(line[4])
            hr_no_upfront = float(line[5])

            available_savings_plans[current_t] += hr_no_upfront + hr_partial_upfront

            for t in range(current_t, current_t + res_duration):
                available_savings_plans[t] += (up_all_upfront + up_partial_upfront) / res_duration

            current_t += 1

    return available_savings_plans

def write_allocation(instance_alloc, cost_alloc, output_path):
    final_t = len(cost_alloc['OnDemand'])

    #instance allocation
    instance_alloc_df = {'timestamp': [t for t in range(final_t)],
                        'market': ['on_demand', 'r_all', 'r_partial', 'r_no'] * final_t,
                        }

    instance_types = list(instance_alloc['OnDemand'].keys())

    for instance_type in instance_types:
        instance_alloc_df[instance_type] = []
        for t in range(final_t):
            od = instance_alloc['OnDemand'][instance_type][t]
            r_all = instance_alloc['RAll'][instance_type][t]
            r_partial = instance_alloc['RPartial'][instance_type][t]
            r_no = instance_alloc['RNo'][instance_type][t]
            
            instance_alloc_df[instance_type] += [od, r_all, r_partial, r_no]

    instance_alloc_df.to_csv(f'{output_path}/alloc_instance.csv', index=False)

    #cost allocation
    cost_alloc_df = pd.DataFrame(cost_alloc)
    cost_alloc_df.insert(0, 'timestamp', [t for t in range(final_t)])
    cost_alloc_df.to_csv(f'{output_path}/alloc_cost.csv', index=False)

if __name__ == '__main__':
    main()