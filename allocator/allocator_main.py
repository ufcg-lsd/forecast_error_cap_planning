import click
from allocator_aux import InstancePrices

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('cost_allocation_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(exists=False))
@click.option('--res_duration',
              type=int,
              default=8760)
def main(demand_path, prices_path, cost_allocation_path, output_path, res_duration):
    demand = read_demand(demand_path)
    prices = read_prices(prices_path)
    available_savings_plans = read_savings_plans(cost_allocation_path, res_duration)

    allocation = allocate(demand, prices, available_savings_plans, res_duration)
    
    write_allocation(allocation, output_path)

def allocate(demand, prices, available_savings_plans):
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

def write_allocation(output_path):
     #TODO

if __name__ == '__main__':
    main()