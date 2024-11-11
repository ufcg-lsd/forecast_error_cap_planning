import pandas as pd

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

def read_prices(prices_path):
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

                prices[instance_type] = InstancePrices(on_demand_hour, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront)
    return prices

def read_cost_allocation(cost_allocation_path):
    cost_allocation = {'OnDemand': [], 'RAll': [], 'RPartialUp': [], 'RPartialHr': [], 'RNo': []}
    with open(cost_allocation_path, mode='r') as file:
            header = file.readline().split(',')
            
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.split(',')

                cost_allocation['OnDemand'].append(line[1])
                cost_allocation['RAll'].append(line[2])
                cost_allocation['RPartialUp'].append(line[3])
                cost_allocation['RPartialHr'].append(line[4])
                cost_allocation['RNo'].append(line[5])

    return cost_allocation

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

def initiate_instance_allocation(demand):
    instance_allocation = {'OnDemand': {}, 'RAll': {}, 'RPartial': {}, 'RNo': {}}
    for instance_type in demand:
        instance_demand = demand[instance_type]
        
        instance_allocation['RAll'][instance_type] = [0 for _ in range(len(instance_demand))]
        instance_allocation['RPartial'][instance_type] = [0 for _ in range(len(instance_demand))]
        instance_allocation['RNo'][instance_type] = [0 for _ in range(len(instance_demand))]
        instance_allocation['OnDemand'][instance_type] = [0 for _ in range(len(instance_demand))]

    return instance_allocation

class InstancePrices:
    def __init__(self, on_demand, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront):
        self.on_demand = on_demand
        self.up_all_upfront = up_all_upfront
        self.up_partial_upfront = up_partial_upfront
        self.hr_partial_upfront = hr_partial_upfront
        self.hr_no_upfront = hr_no_upfront
    
    def get_effective_hourly_rate(self, market, res_duration):
        match market:
            case 'OnDemand':
                return self.on_demand
            case 'RAll':
                return self.up_all_upfront / res_duration
            case 'RPartial':
                return (self.up_partial_upfront / res_duration) + self.hr_partial_upfront
            case 'RNo':
                return self.hr_no_upfront