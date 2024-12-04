import unittest
from unittest.mock import patch
from src.experiment.main import experiment
import numpy as np
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
    def test_original_dem_one_type(self):
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
    def test_original_dem_two_types(self):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10],
                  'a.medium': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large', 'a.medium'],
                  'OnDemand': [2, 1.5],
                  'RAllUpfront1Y': [0, 0],
                  'RPartialUpfront1YUP': [0, 0],
                  'RPartialUpfront1YM': [0, 0],
                  'RNoUpfront1YM': [1, 0.5]}
    
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
        self.assertEqual(od_cost, 80)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 100)

    #more than one family
    # def test_original_dem_two_families(self):
    #     demand = {'timestamp': [0, 1, 2, 3],
    #               'a.large': [10, 10, 10, 10],
    #               'a.medium': [10, 10, 10, 10],
    #               'b.large': [1, 1, 1, 1],
    #               'b.medium': [2, 2, 2, 2]}

    #     prices = {'flavor': ['a.large', 'a.medium', 'b.large', 'b.medium'],
    #               'OnDemand': [2, 1.5, 2, 1.5],
    #               'RAllUpfront1Y': [0, 0, 0, 0],
    #               'RPartialUpfront1YUP': [0, 0, 0, 0],
    #               'RPartialUpfront1YM': [0, 0, 0, 0],
    #               'RNoUpfront1YM': [1, 0.5, 2, 1.5]}
    
    #     error_configs = {'bias_level': [0],
    #                      'sd_level': [0]}

    #     sp_purchases = {'timestamp': [0, 1, 2, 3],
    #               'OnDemand': [0, 0, 0, 0],
    #               'RAll': [0, 0, 0, 0],
    #               'RPartialUp': [0, 0, 0, 0],
    #               'RPartialHr': [0, 0, 0, 0],
    #               'RNo': [5, 5, 5, 5],
    #               'AllMarkets': [0, 0, 0, 0]}
        
    #     self.write_files(demand, prices, error_configs, sp_purchases)

    #     res_duration = 4

    #     out = subprocess.run(f'poetry run python3 main.py demand.csv prices.csv error_configs.csv sp_purchases.csv --reserve_duration {res_duration} output_tests', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    #     summary = pd.read_csv('output_tests/allocations/summary.csv')
    #     od_cost = sum(summary['od_cost'])
    #     sp_cost = sum(summary['sp_cost'])
    #     total_cost = sum(summary['total_cost'])
    #     self.assertEqual(od_cost, 80)
    #     self.assertEqual(sp_cost, 20)        
    #     self.assertEqual(total_cost, 100)

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
    @patch('src.forecast_generation.main.np.random.normal')
    def test_only_sd(self, mock):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0],
                         'sd_level': [0.1]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        mock.return_value = np.array([-0.3,  0.4,  0.5,  0.6], dtype=np.float64)

        # [0.97, 1.04, 1.05, 1.06]
        # new demand: [10, 11, 11, 11]

        experiment('demand.csv', 'prices.csv', 'error_configs.csv', 'sp_purchases.csv', res_duration, 'output_tests')
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 46)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 66)

    # change in both
    @patch('src.forecast_generation.main.np.random.normal')
    def test_sd_bias(self, mock):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0.1],
                         'sd_level': [0.1]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        mock.return_value = np.array([-0.3,  0.4,  0.5,  0.6], dtype=np.float64)

        # [1.07, 1.14, 1.15, 1.16]
        # new demand: [11, 12, 12, 12]

        experiment('demand.csv', 'prices.csv', 'error_configs.csv', 'sp_purchases.csv', res_duration, 'output_tests')
        summary = pd.read_csv('output_tests/allocations/summary.csv')
        od_cost = sum(summary['od_cost'])
        sp_cost = sum(summary['sp_cost'])
        total_cost = sum(summary['total_cost'])
        self.assertEqual(od_cost, 54)
        self.assertEqual(sp_cost, 20)        
        self.assertEqual(total_cost, 74)

    @patch('src.forecast_generation.main.np.random.normal')
    def test_sd_bias_2(self, mock):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0.1],
                         'sd_level': [0.2]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        mock.return_value = np.array([-0.3,  0.4,  0.5,  0.6], dtype=np.float64)     

        # [1.04, 1.18, 1.20, 1.22]
        # new demand: [11, 12, 12, 13]

        experiment('demand.csv', 'prices.csv', 'error_configs.csv', 'sp_purchases.csv', res_duration, 'output_tests')
        summary = pd.read_csv('output_tests/allocations/summary.csv')

        config_3_od = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.2), 'od_cost'].values[0]
        config_3_sp = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.2), 'sp_cost'].values[0]
        config_3_total = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.2), 'total_cost'].values[0]
        self.assertEqual(config_3_od, 56)
        self.assertEqual(config_3_sp, 20)        
        self.assertEqual(config_3_total, 76)

    ##############

    # more than one config
    @patch('src.forecast_generation.main.np.random.normal')
    def test_multiple_configs(self, mock):
        demand = {'timestamp': [0, 1, 2, 3],
                  'a.large': [10, 10, 10, 10]}

        prices = {'flavor': ['a.large'],
                  'OnDemand': [2],
                  'RAllUpfront1Y': [0],
                  'RPartialUpfront1YUP': [0],
                  'RPartialUpfront1YM': [0],
                  'RNoUpfront1YM': [1]}
    
        error_configs = {'bias_level': [0.1, -0.1, 0.1],
                         'sd_level': [0.1, 0.1, 0.2]}

        sp_purchases = {'timestamp': [0, 1, 2, 3],
                  'OnDemand': [0, 0, 0, 0],
                  'RAll': [0, 0, 0, 0],
                  'RPartialUp': [0, 0, 0, 0],
                  'RPartialHr': [0, 0, 0, 0],
                  'RNo': [5, 5, 5, 5],
                  'AllMarkets': [0, 0, 0, 0]}
        
        self.write_files(demand, prices, error_configs, sp_purchases)

        res_duration = 4

        mock.return_value = np.array([-0.3,  0.4,  0.5,  0.6], dtype=np.float64)

        # config 1:
        # [1.07, 1.14, 1.15, 1.16]
        # new demand: [11, 12, 12, 12]

        # config 2:
        # [0.87, 0.94, 0.95, 0.96]
        # new demand: [9, 10, 10, 10]        

        # config 3:
        # [1.04, 1.18, 1.20, 1.22]
        # new demand: [11, 12, 12, 13]

        experiment('demand.csv', 'prices.csv', 'error_configs.csv', 'sp_purchases.csv', res_duration, 'output_tests')
        summary = pd.read_csv('output_tests/allocations/summary.csv')

        
        config_1_od = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.1), 'od_cost'].values[0]
        config_1_sp = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.1), 'sp_cost'].values[0]
        config_1_total = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.1), 'total_cost'].values[0]
        self.assertEqual(config_1_od, 54)
        self.assertEqual(config_1_sp, 20)        
        self.assertEqual(config_1_total, 74)

        config_2_od = summary.loc[(summary['bias_level'] == -0.1) & (summary['sd_level'] == 0.1), 'od_cost'].values[0]
        config_2_sp = summary.loc[(summary['bias_level'] == -0.1) & (summary['sd_level'] == 0.1), 'sp_cost'].values[0]
        config_2_total = summary.loc[(summary['bias_level'] == -0.1) & (summary['sd_level'] == 0.1), 'total_cost'].values[0]
        self.assertEqual(config_2_od, 38)
        self.assertEqual(config_2_sp, 20)        
        self.assertEqual(config_2_total, 58)

        config_3_od = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.2), 'od_cost'].values[0]
        config_3_sp = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.2), 'sp_cost'].values[0]
        config_3_total = summary.loc[(summary['bias_level'] == 0.1) & (summary['sd_level'] == 0.2), 'total_cost'].values[0]
        self.assertEqual(config_3_od, 56)
        self.assertEqual(config_3_sp, 20)        
        self.assertEqual(config_3_total, 76)
