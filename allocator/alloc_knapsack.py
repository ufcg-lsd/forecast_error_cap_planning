from ortools.algorithms.python import knapsack_solver
from .allocator_aux import initiate_instance_allocation

FLOAT_PRECISION = 10**5

def alloc(demand, prices, available_sp, market_option, res_duration):
    """ Allocates the demand in the on-demand and savings plans markets
    """
    
    instance_allocation = initiate_instance_allocation(demand)

    for t in range(len(available_sp)):
        demand_sel = {key: value[t] for key, value in demand.items()}
        packed_items = knapsack(demand_sel, prices, market_option, available_sp[t], res_duration)

        for instance_type in packed_items:
            instance_allocation[market_option][instance_type][t] += 1

        for instance_type in demand:
            num_sp = instance_allocation[market_option][instance_type][t]
            num_od = demand[instance_type][t] - num_sp
            instance_allocation['OnDemand'][instance_type][t] = num_od
        
    return instance_allocation

def knapsack(demand, prices, market_option, available_sp, res_duration):
    """ Solves the knapsack problem for savings plans

    For one hour, chooses which instances should be allocated in the savings plans market.
    The savings plans available value is the knapsack capacity and the instances are the items.
    For each instance, its weight is the savings plans price and its value is the on-demand price.
    The objective is to maximize the value inside the knapsack, given its capacity. 
    """

    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    # each instance as a string, if there is more than one instance of the same type, 
    # it appears more than once in the list
    instance_types = []
    for instance_type, quantity in demand.items():
        for i in range(quantity):
            instance_types.append(instance_type)
    
    values = [] #on-demand prices
    weights = [[]] #savings plans prices
    for instance_type in instance_types:
        on_demand_price = prices[instance_type].on_demand
        sp_price = prices[instance_type].get_effective_hourly_rate(market_option, res_duration)
        values.append(int(round(on_demand_price * FLOAT_PRECISION, 0)))
        weights[0].append(int(round(sp_price * FLOAT_PRECISION, 0)))

    capacities = [int(round(available_sp * FLOAT_PRECISION, 0))] #savings plans active value

    solver.init(values, weights, capacities)
    computed_value = solver.solve()

    packed_items = []
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(instance_types[i])

    return packed_items