class InstancePrices:
    def __init__(self, on_demand, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront, sp_up_all_upfront, sp_up_partial_upfront, sp_hr_partial_upfront, sp_hr_no_upfront):
        self.on_demand = on_demand
        self.up_all_upfront = up_all_upfront
        self.up_partial_upfront = up_partial_upfront
        self.hr_partial_upfront = hr_partial_upfront
        self.hr_no_upfront = hr_no_upfront
        self.sp_up_all_upfront = sp_up_all_upfront
        self.sp_up_partial_upfront = sp_up_partial_upfront
        self.sp_hr_partial_upfront = sp_hr_partial_upfront
        self.sp_hr_no_upfront = sp_hr_no_upfront

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

                prices[instance_type] = InstancePrices(on_demand_hour, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront)
    return prices

def select_types(families, prices):
    new_families = {}
    for family in families:
        instance_types = families[family]
        new_families[family] = []
        for instance_type in instance_types:
            if instance_type in prices.keys():
                new_families[family].append(instance_type)
    
    return new_families