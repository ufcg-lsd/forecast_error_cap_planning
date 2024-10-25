def alloc(demand, prices, available_sp, market_option, res_duration):
    ordered_instance_types = sorted(prices, key=lambda x: prices[x].get_effective_hourly_rate(market_option, res_duration), reverse=True)

    od_cost = 0

    for instance_type in ordered_instance_types:
        if instance_type in list(demand.keys()):
            instance_demand = demand[instance_type]

            hourly_price = prices[instance_type].get_effective_hourly_rate(market_option, res_duration)
            
            for t in range(len(instance_demand)):
                num_sp_instances = min(available_sp[t] // hourly_price, instance_demand[t])
                available_sp[t] = available_sp[t] - (num_sp_instances * hourly_price)

                remaining_instances = instance_demand[t] - num_sp_instances
                od_cost += remaining_instances * prices[instance_type].on_demand
    
    return od_cost