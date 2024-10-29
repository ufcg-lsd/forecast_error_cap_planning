from ortools.algorithms.python import knapsack_solver

def alloc(demand, prices, available_sp, market_option):
    instance_allocation = initiate_instance_allocation(demand)

    for t in range(available_sp):
        demand_sel = {key: value[t] for key, value in demand.items()}
        packed_items = knapsack(demand_sel, prices, market_option, available_sp[t])

        for instance_type in packed_items:
            instance_allocation[market_option][instance_type][t] += 1

        for instance_type in demand:
            num_sp = instance_allocation[market_option][instance_type][t]
            num_od = demand[instance_type][t] - num_sp
            instance_allocation['OnDemand'][instance_type][t] = num_od
    
    return instance_allocation

def knapsack(demand, prices, market_option, available_sp):
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER
    )

    # each instance as a string, if there is more than one instance of the same type, 
    # it appears more than once in the list
    instance_types = []
    for instance_type in demand:
        quantity = demand[instance_type]
        for i in range(quantity):
            instance_types.append(instance_type)
    
    values = [] #on-demand prices
    weights = [[]] #savings plans prices
    for instance_type in instance_types:
        values.append(prices[instance_type]['OnDemand'])
        weights[0].append(prices[instance_type][market_option])

    capacities = [available_sp] #savings plans active value

    solver.init(values, weights, capacities)
    computed_value = solver.solve()

    packed_items = []
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(instance_types[i])

    return packed_items

def initiate_instance_allocation(demand):
    instance_allocation = {'OnDemand': {}, 'RAll': {}, 'RPartial': {}, 'RNo': {}}
    for instance_type in demand:
        instance_demand = demand[instance_type]
        
        instance_allocation['RAll'][instance_type] = [0 for _ in range(len(instance_demand))]
        instance_allocation['RPartial'][instance_type] = [0 for _ in range(len(instance_demand))]
        instance_allocation['RNo'][instance_type] = [0 for _ in range(len(instance_demand))]
        instance_allocation['OnDemand'][instance_type] = [0 for _ in range(len(instance_demand))]

    return instance_allocation
