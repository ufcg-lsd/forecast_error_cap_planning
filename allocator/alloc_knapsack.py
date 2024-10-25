from ortools.algorithms.python import knapsack_solver

def main(demand, prices, available_savings_plans):
    for t in range(available_savings_plans):
        demand_sel = {key: value[t] for key, value in demand.items()}
        allocate_hour(demand_sel, prices, available_savings_plans[t])

def allocate_hour(demand, prices, available_savings_plans):
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER
    )

    # each instance as a string, if there is more than one instance of the same type, 
    # it appears more than once in the list
    instance_types = []
    for instance_type in list(demand.keys()):
        quantity = demand[instance_type]
        for i in range(quantity):
            instance_types.append(instance_type)

    #values: on-demand prices
    values = []
    #weights: savings plans prices
    weights = [[]]

    for instance_type in instance_types:
        values.append[prices[instance_type]]
        weights[0].append[prices[instance_type]]

    #capacities: savings plans active value
    capacities = [available_savings_plans]

    solver.init(values, weights, capacities)
    computed_value = solver.solve()

    packed_items = []
    packed_weights = []
    instances_savings_plans = []
    total_weight = 0
    print("Total value =", computed_value)
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print("Total weight:", total_weight)
    print("Packed items:", packed_items)
    print("Packed_weights:", packed_weights)
