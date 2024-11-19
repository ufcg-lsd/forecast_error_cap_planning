from .allocator_aux import initiate_instance_allocation

def alloc(demand, prices, available_sp, market_option, res_duration):
    """ Allocates the demand in the on-demand and savings plans markets
    """
    
    instance_allocation = initiate_instance_allocation(demand)
    ordered_instance_types = sorted(prices, key=lambda x: prices[x].get_effective_hourly_rate(market_option, res_duration), reverse=True)

    for instance_type in ordered_instance_types:
        if instance_type in demand:
            instance_demand = demand[instance_type]
            hourly_price = prices[instance_type].get_effective_hourly_rate(market_option, res_duration)
            
            for t in range(len(instance_demand)):
                num_sp_instances = min(available_sp[t] // hourly_price, instance_demand[t])
                remaining_instances = instance_demand[t] - num_sp_instances

                instance_allocation[market_option][instance_type][t] = num_sp_instances
                instance_allocation['OnDemand'][instance_type][t] = remaining_instances

                available_sp[t] = available_sp[t] - (num_sp_instances * hourly_price)
    
    return instance_allocation