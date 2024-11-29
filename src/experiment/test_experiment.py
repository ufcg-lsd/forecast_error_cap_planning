import unittest
import pandas as pd
import os
import subprocess

class TestVtexAllocation(unittest.TestCase):

    def setUp(self):
        os.mkdir('output_tests')

    def safe_remove(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    # def tearDown(self):
    #     self.safe_remove('demand.csv')
    #     self.safe_remove('prices.csv')
    #     self.safe_remove('error_configs.csv')
    #     self.safe_remove('sp_purchases.csv')

    #     #out = subprocess.run('rm -r output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    ##############  ##############
    
    def test_only_original_dem(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}

        prices_df = pd.DataFrame(prices)
        prices_df.to_csv('prices.csv', index=False)

        error_configs = {'bias': [0],
                         'sd': [0]}

        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)
    
        error_configs = {'bias_level': [0],
                         'sd_level': [0]}

        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}

        sp_purchases_df = pd.DataFrame(sp_purchases)
        sp_purchases_df.to_csv('sp_purchases.csv', index=False)

        out = subprocess.run('poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        summary = pd.read_csv('output_tests/allocations/bias_0.0_sd_0.0.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 50)
        self.assertEqual(sp_cost, 25)        
        self.assertEqual(total_cost, 75)