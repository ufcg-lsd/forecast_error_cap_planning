import unittest
import pandas as pd
import os
import subprocess

class TestExperiment(unittest.TestCase):

    def setUp(self):
        os.mkdir('output_tests')

    def safe_remove(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def tearDown(self):
        self.safe_remove('demand.csv')
        self.safe_remove('prices.csv')
        self.safe_remove('error_configs.csv')
        self.safe_remove('sp_purchases.csv')

        out = subprocess.run('rm -r output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    def write_files(self, demand, prices, error_configs, sp_purchases):
        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        prices_df = pd.DataFrame(prices)
        prices_df.to_csv('prices.csv', index=False)

        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        sp_purchases_df = pd.DataFrame(sp_purchases)
        sp_purchases_df.to_csv('sp_purchases.csv', index=False)
        

    ##############  ##############

    # only original demand#
    
    #one type
    def test_only_original_dem(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0],
                         'sd_level': [0]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        out = subprocess.run(f'poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv --reserve_duration {res_duration} output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 40)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 60)

    #more than one type

    #more than one family

    ##############

    # only one simulated forecast #

    # change only in bias
    def test_only_bias_positive(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0.1],
                         'sd_level': [0]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        out = subprocess.run(f'poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv --reserve_duration {res_duration} output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 48)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 68)

    def test_only_bias_positive_not_integer(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0.05],
                         'sd_level': [0]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        out = subprocess.run(f'poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv --reserve_duration {res_duration} output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 48)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 68)

    def test_only_bias_negative(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [-0.1],
                         'sd_level': [0]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        out = subprocess.run(f'poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv --reserve_duration {res_duration} output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 32)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 52)

    def test_only_bias_negative_not_integer(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [-0.05],
                         'sd_level': [0]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        out = subprocess.run(f'poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv --reserve_duration {res_duration} output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 40)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 60)

    # change only in sd

    # change in both

    ##############

    # more than one config
