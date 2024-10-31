import unittest
from allocator_main import allocate
from allocator_aux import InstancePrices

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

    def testHeuristicTwoInstTypeRNo(self):
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

    def testHeuristicTwoInstTypeRNo(self):
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

        instance_allocation = {'OnDemand': {'a1.large': [3, 3, 3, 3, 3], 'a1.medium': [0, 0, 0, 0, 0]},
                     'RAll': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RPartial': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [0, 0, 0, 0, 0]}, 
                     'RNo': {'a1.large': [0, 0, 0, 0, 0], 'a1.medium': [5, 5, 5, 5, 5]}}
        
        cost_allocation = {'OnDemand': [18, 18, 18, 18, 18], 
                           'RAll': [0, 0, 0, 0, 0], 
                           'RPartialUp': [0, 0, 0, 0, 0], 
                           'RPartialHr': [0, 0, 0, 0, 0], 
                           'RNo': [10, 10, 10, 10, 10]}
        
        self.assertDictEqual(instance_allocation_res, instance_allocation)
        self.assertDictEqual(cost_allocation_res, cost_allocation)

