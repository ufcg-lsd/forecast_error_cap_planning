import click
from allocator_aux import read_demand, read_prices, read_cost_allocation, write_allocation
import alloc_heuristic
import alloc_knapsack

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('cost_allocation_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option('--res_duration',
              type=int,
              default=8760)
@click.option('--alloc_method',
              type=int,
              default=1)
def main(demand_path, prices_path, cost_allocation_path, output_dir, res_duration, alloc_method):
    demand = read_demand(demand_path)
    prices = read_prices(prices_path)
    cost_allocation = read_cost_allocation(cost_allocation_path)

    instance_allocation, cost_allocation = allocate(demand, prices, cost_allocation, res_duration, alloc_method)
    
    write_allocation(instance_allocation, cost_allocation, output_dir)

def allocate(demand, prices, cost_allocation, res_duration, alloc_method):
    available_sp = get_available_savings_plans(cost_allocation, res_duration)

    match alloc_method:
        case 1:
            instance_allocation = alloc_heuristic.alloc(demand, prices, available_sp, res_duration)
        case 2:
            instance_allocation = alloc_knapsack.alloc(demand, prices, available_sp, res_duration)

    cost_allocation = update_cost_alloc(cost_allocation, instance_allocation, prices)
    
    return instance_allocation, cost_allocation

def get_available_savings_plans(cost_allocation, res_duration):
    final_t = len(cost_allocation['OnDemand'])
    available_savings_plans = [0 for _ in range(final_t)]
    for curr_t in range(final_t):
        up_all_upfront = cost_allocation['RAll'][curr_t]
        up_partial_upfront = cost_allocation['RPartialUp'][curr_t]
        hr_partial_upfront = cost_allocation['RPartialHr'][curr_t]
        hr_no_upfront = cost_allocation['RNo'][curr_t]
    
        available_savings_plans[curr_t] += hr_no_upfront + hr_partial_upfront

        for t in range(curr_t, curr_t + res_duration):
            available_savings_plans[t] += (up_all_upfront + up_partial_upfront) / res_duration

        curr_t += 1

    return available_savings_plans

def update_cost_alloc(cost_allocation, instance_allocation, prices):
    final_t = len(cost_allocation['OnDemand']) 
    
    for t in range(final_t):
        cost_allocation['OnDemand'][t] = 0

        for instance_type in instance_allocation['OnDemand']:
            demand = instance_allocation['OnDemand'][instance_type][t]
            price = prices[instance_type].on_demand
            cost_allocation['OnDemand'][t] += demand * price
    
    return cost_allocation

if __name__ == '__main__':
    main()