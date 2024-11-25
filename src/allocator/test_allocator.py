import unittest
from src.allocator.allocator_main import allocate
from src.allocator.allocator_aux import InstancePrices

class TestAllocator(unittest.TestCase):

    def testHeuristicOneInstTypeRNo(self):
        demand = {'a1': [5, 5, 10, 5, 5]}
        prices = {'a1': InstancePrices(1, 0, 0, 0, 0.5)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [2, 2, 2, 2, 2]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1': [1, 1, 6, 1, 1]},
                     'RAll': {'a1': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1': [4, 4, 4, 4, 4]}}
        
        cost_allocation = {'OnDemand': [1, 1, 6, 1, 1], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [2, 2, 2, 2, 2]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testHeuristicOneInstTypeRAll(self):
        demand = {'a1': [5, 5, 10, 5, 5]}
        prices = {'a1': InstancePrices(1, 2.5, 0, 0, 0)} #effective hourly rate: 0.5
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [10, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0],
                           'RNo': [0, 0, 0, 0, 0]}
        res_duration = 5
        market_option = 'RAll'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1': [1, 1, 6, 1, 1]},
                     'RAll': {'a1': [4, 4, 4, 4, 4]}, 
                     'RPartial': {'a1': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1': [0, 0, 0, 0, 0]}}
        
        cost_allocation = {'OnDemand': [1, 1, 6, 1, 1], 
                           'RAll': [10, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [0, 0, 0, 0, 0]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testHeuristicOneInstTypeRPartial(self):
        demand = {'a1': [5, 5, 10, 5, 5]}
        prices = {'a1': InstancePrices(1, 0, 1.25, 0.25, 0)} #effective hourly rate: 0.5
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [5, 0, 0, 0, 0],
                           'RPartialHr': [1, 1, 1, 1, 1],
                           'RNo': [0, 0, 0, 0, 0]}
        res_duration = 5
        market_option = 'RPartial'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1': [1, 1, 6, 1, 1]},
                     'RAll': {'a1': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1': [4, 4, 4, 4, 4]}, 
                     'RNo': {'a1': [0, 0, 0, 0, 0]}}
        
        cost_allocation = {'OnDemand': [1, 1, 6, 1, 1], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [5, 0, 0, 0, 0], 
                           'RPartialHr': [1, 1, 1, 1, 1], 
                           'RNo': [0, 0, 0, 0, 0]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

#############################################################################

    def testHeuristicTwoInstTypeRNo1(self):
        demand = {'a1.large': [2, 2, 3, 1, 1],
                  'a1.medium': [1, 1, 1, 1, 3]}
        prices = {'a1.large': InstancePrices(2, 0, 0, 0, 1),
                  'a1.medium': InstancePrices(1, 0, 0, 0, 0.5)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [2, 2, 2, 2, 2]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1.large': [0, 0, 1, 0, 0], 'a1.medium': [1, 1, 1, 0, 1]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [2, 2, 2, 1, 1], 'a1.medium': [0, 0, 0, 1, 2]}}
        
        cost_allocation = {'OnDemand': [1, 1, 2+1, 0, 1], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [2, 2, 2, 2, 2]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testHeuristicTwoInstTypeRNo2(self):
        demand = {'a1.large': [3, 3, 3, 3, 3],
                  'a1.medium': [5, 5, 5, 5, 5]}
        prices = {'a1.large': InstancePrices(6, 0, 0, 0, 3),
                  'a1.medium': InstancePrices(4, 0, 0, 0, 2)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [10, 10, 10, 10, 10]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [5, 5, 5, 5, 5]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [3, 3, 3, 3, 3], 'a1.medium': [0, 0, 0, 0, 0]}}
        
        cost_allocation = {'OnDemand': [20, 20, 20, 20, 20], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [10, 10, 10, 10, 10]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testHeuristicMultInstType(self):
        demand = {'a1.large': [3, 3, 3, 3, 3],
                  'a1.medium': [3, 3, 3, 3, 3],
                  'a1.small': [3, 3, 3, 3, 3],
                  'a1.xlarge': [3, 3, 3, 3, 3]}
        prices = {'a1.large': InstancePrices(6, 0, 0, 0, 3),
                  'a1.medium': InstancePrices(4, 0, 0, 0, 2),
                  'a1.small': InstancePrices(2, 0, 0, 0, 1),
                  'a1.xlarge': InstancePrices(12, 0, 0, 0, 6)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [10.5, 10.5, 10.5, 15, 15]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1.large': [2, 2, 2, 2, 2], 'a1.medium': [3, 3, 3, 3, 3], 'a1.small': [2, 2, 2, 3, 3], 'a1.xlarge': [2, 2, 2, 1, 1]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0], 'a1.small': [0, 0, 0, 0, 0], 'a1.xlarge': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0], 'a1.small': [0, 0, 0, 0, 0], 'a1.xlarge': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [1, 1, 1, 1, 1], 'a1.medium': [0, 0, 0, 0, 0], 'a1.small': [1, 1, 1, 0, 0], 'a1.xlarge': [1, 1, 1, 2, 2]}}
        
        cost_allocation = {'OnDemand': [2*6+3*4+2*2+2*12, 2*6+3*4+2*2+2*12, 2*6+3*4+2*2+2*12, 2*6+3*4+3*2+1*12, 2*6+3*4+3*2+1*12], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [10.5, 10.5, 10.5, 15, 15]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testHeuristicDifferentDiscounts(self):
        demand = {'a1.large': [2, 2, 2, 2, 2],
                  'a1.medium': [5, 5, 5, 5, 5]}
        prices = {'a1.large': InstancePrices(5, 0, 0, 0, 3),
                  'a1.medium': InstancePrices(4, 0, 0, 0, 2)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [10, 10, 10, 10, 10]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 1

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [3, 3, 3, 3, 3]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [2, 2, 2, 2, 2], 'a1.medium': [2, 2, 2, 2, 2]}}
        
        cost_allocation = {'OnDemand': [12, 12, 12, 12, 12], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [10, 10, 10, 10, 10]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

#############################################################################

    def testKnapsackTwoInstTypeRNo(self):
        demand = {'a1.large': [3, 3, 3, 3, 3],
                  'a1.medium': [5, 5, 5, 5, 5]}
        prices = {'a1.large': InstancePrices(6, 0, 0, 0, 3),
                  'a1.medium': InstancePrices(4, 0, 0, 0, 2)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [10, 10, 10, 10, 10]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 2

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation_1 = {'OnDemand': {'a1.large': [3, 3, 3, 3, 3], 'a1.medium': [0, 0, 0, 0, 0]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [5, 5, 5, 5, 5]}}

        instance_allocation_2 = {'OnDemand': {'a1.large': [1, 1, 1, 1, 1], 'a1.medium': [3, 3, 3, 3, 3]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [2, 2, 2, 2, 2], 'a1.medium': [2, 2, 2, 2, 2]}}

        possible_instance_allocations = [
            instance_allocation_1,
            instance_allocation_2
        ]
        
        cost_allocation = {'OnDemand': [18, 18, 18, 18, 18], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [10, 10, 10, 10, 10]}
        
        self.assertIn(instance_allocation_res, possible_instance_allocations)
        self.assertDictEqual(cost_allocation_res, cost_allocation)
    
    def testKnapsackDifferentDiscounts(self):
        demand = {'a1.large': [2, 2, 2, 2, 2],
                  'a1.medium': [5, 5, 5, 5, 5]}
        prices = {'a1.large': InstancePrices(5, 0, 0, 0, 3),
                  'a1.medium': InstancePrices(4, 0, 0, 0, 2)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [10, 10, 10, 10, 10]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 2

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1.large': [2, 2, 2, 2, 2], 'a1.medium': [0, 0, 0, 0, 0]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [5, 5, 5, 5, 5]}}
        
        cost_allocation = {'OnDemand': [10, 10, 10, 10, 10], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [10, 10, 10, 10, 10]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testKnapsackRealPricesRNo(self):
        demand = {'d3en.12xlarge': [3 for _ in range(8760)]}
        prices = {'d3en.12xlarge': InstancePrices(6.30864, 32495, 16579, 1.89259, 3.97444)}
        cost_allocation = {'OnDemand': [0 for _ in range(8760)], 
                           'RAll': [0 for _ in range(8760)], 
                           'RPartialUp': [0 for _ in range(8760)],
                           'RPartialHr': [0 for _ in range(8760)] ,
                           'RNo': [7.72612 for _ in range(8760)]}
        res_duration = 8760
        market_option = 'RNo'
        alloc_method = 2

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'d3en.12xlarge': [2 for _ in range(8760)]},
                     'RAll': {'d3en.12xlarge': [0 for _ in range(8760)]}, 
                     'RPartial': {'d3en.12xlarge': [0 for _ in range(8760)]}, 
                     'RNo': {'d3en.12xlarge': [1 for _ in range(8760)]}}
        
        cost_allocation = {'OnDemand': [12.61728 for _ in range(8760)], 
                           'RAll': [0 for _ in range(8760)], 
                           'RPartialUp': [0 for _ in range(8760)], 
                           'RPartialHr': [0 for _ in range(8760)], 
                           'RNo': [7.72612 for _ in range(8760)]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testKnapsackRealPricesRAll(self):
        demand = {'d3en.12xlarge': [3 for _ in range(8760)]}
        prices = {'d3en.12xlarge': InstancePrices(6.30864, 32495, 16579, 1.89259, 3.97444)}
        cost_allocation = {'OnDemand': [0 for _ in range(8760)], 
                           'RAll': [32495] + [0 for _ in range(8759)], 
                           'RPartialUp': [0 for _ in range(8760)],
                           'RPartialHr': [0 for _ in range(8760)] ,
                           'RNo': [0 for _ in range(8760)]}
        res_duration = 8760
        market_option = 'RAll'
        alloc_method = 2

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'d3en.12xlarge': [2 for _ in range(8760)]},
                     'RAll': {'d3en.12xlarge': [1 for _ in range(8760)]}, 
                     'RPartial': {'d3en.12xlarge': [0 for _ in range(8760)]}, 
                     'RNo': {'d3en.12xlarge': [0 for _ in range(8760)]}}
        
        cost_allocation = {'OnDemand': [12.61728 for _ in range(8760)], 
                           'RAll': [32495] + [0 for _ in range(8759)], 
                           'RPartialUp': [0 for _ in range(8760)], 
                           'RPartialHr': [0 for _ in range(8760)], 
                           'RNo': [0 for _ in range(8760)]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testKnapsackRealPricesRPartial(self):
        demand = {'d3en.12xlarge': [3 for _ in range(8760)]}
        prices = {'d3en.12xlarge': InstancePrices(6.30864, 32495, 16579, 1.89259, 3.97444)}
        cost_allocation = {'OnDemand': [0 for _ in range(8760)], 
                           'RAll': [0 for _ in range(8760)], 
                           'RPartialUp': [16579] + [0 for _ in range(8759)],
                           'RPartialHr': [1.89259 for _ in range(8760)],
                           'RNo': [0 for _ in range(8760)]}
        res_duration = 8760
        market_option = 'RPartial'
        alloc_method = 2

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'d3en.12xlarge': [2 for _ in range(8760)]},
                     'RAll': {'d3en.12xlarge': [0 for _ in range(8760)]}, 
                     'RPartial': {'d3en.12xlarge': [1 for _ in range(8760)]}, 
                     'RNo': {'d3en.12xlarge': [0 for _ in range(8760)]}}
        
        cost_allocation = {'OnDemand': [12.61728 for _ in range(8760)], 
                           'RAll': [0 for _ in range(8760)], 
                           'RPartialUp': [16579] + [0 for _ in range(8759)], 
                           'RPartialHr': [1.89259 for _ in range(8760)], 
                           'RNo': [0 for _ in range(8760)]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

    def testKnapsackMultInstType(self):
        demand = {'a1.large': [3, 3, 3, 3, 3],
                  'a1.medium': [3, 3, 3, 3, 3],
                  'a1.small': [3, 3, 3, 3, 3],
                  'a1.xlarge': [3, 3, 3, 3, 3]}
        prices = {'a1.large': InstancePrices(6, 0, 0, 0, 3),
                  'a1.medium': InstancePrices(3, 0, 0, 0, 2),
                  'a1.small': InstancePrices(2, 0, 0, 0, 1),
                  'a1.xlarge': InstancePrices(14, 0, 0, 0, 6)}
        cost_allocation = {'OnDemand': [0, 0, 0, 0, 0], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0],
                           'RPartialHr': [0, 0, 0, 0, 0] ,
                           'RNo': [5.5, 5.5, 5.5, 10, 10]}
        res_duration = 5
        market_option = 'RNo'
        alloc_method = 2

        instance_allocation_res, cost_allocation_res = allocate(demand, prices, cost_allocation, res_duration, market_option, alloc_method)

        instance_allocation = {'OnDemand': {'a1.large': [2, 2, 2, 2, 2], 'a1.medium': [3, 3, 3, 3, 3], 'a1.small': [1, 1, 1, 2, 2], 'a1.xlarge': [3, 3, 3, 2, 2]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0], 'a1.small': [0, 0, 0, 0, 0], 'a1.xlarge': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0], 'a1.small': [0, 0, 0, 0, 0], 'a1.xlarge': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [1, 1, 1, 1, 1], 'a1.medium': [0, 0, 0, 0, 0], 'a1.small': [2, 2, 2, 1, 1], 'a1.xlarge': [0, 0, 0, 1, 1]}}
        
        cost_allocation = {'OnDemand': [12+9+2+42, 12+9+2+42, 12+9+2+42, 12+9+4+28, 12+9+4+28], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [5.5, 5.5, 5.5, 10, 10]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)