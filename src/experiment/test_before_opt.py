import os
import unittest
import subprocess
import shutil
import pandas as pd

class TestBeforeOpt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir('output_tests')
        cls.create_files()
        out = subprocess.run(f'poetry run python3 before_opt.py demand.csv prices.csv error_configs.csv output_tests --error_option 1', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @classmethod
    def tearDownClass(cls):
        cls.safe_remove('demand.csv')
        cls.safe_remove('prices.csv')
        cls.safe_remove('error_configs.csv')

        shutil.rmtree('output_tests')

    def create_files():
        demand = {'timestamp': [0, 1, 2],
                  'a.large': [10, 10, 10],
                  'a.medium': [1, 1, 1],
                  'b.large': [5, 5, 5],
                  'b.medium': [3, 3, 3]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        prices = {'flavor': ['a.large', 'a.medium', 'b.large', 'b.medium'],
                  'OnDemand': [2, 1, 4, 2],
                  'RAllUpfront1Y': [0, 0, 0, 0],
                  'RPartialUpfront1YUP': [0, 0, 0, 0],
                  'RPartialUpfront1YM': [0, 0, 0, 0],
                  'RNoUpfront1YM': [1, 0.5, 2, 1]}

        prices_df = pd.DataFrame(prices)
        prices_df.to_csv('prices.csv', index=False)

        error_configs = {'bias_level': [0.0, 0.1, 0.2],
                  'sd_level': [0.0, 0.0, 0.0]}

        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

    def safe_remove(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
    
    def test_dir_structure(self):
        self.assertTrue(os.path.isdir('output_tests/forecasts'))
        self.assertTrue(os.path.isdir('output_tests/optimizations'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.0_sd_0.0'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.1_sd_0.0'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.2_sd_0.0'))

        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.0_sd_0.0/a'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.1_sd_0.0/a'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.2_sd_0.0/a'))

        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.0_sd_0.0/b'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.1_sd_0.0/b'))
        self.assertTrue(os.path.isdir('output_tests/optimizations/bias_0.2_sd_0.0/b'))
    
    def test_forecast_files(self):
        self.assertTrue(os.path.isfile('output_tests/forecasts/demand_bias_0.0_sd_0.0.csv'))
        self.assertTrue(os.path.isfile('output_tests/forecasts/demand_bias_0.1_sd_0.0.csv'))
        self.assertTrue(os.path.isfile('output_tests/forecasts/demand_bias_0.2_sd_0.0.csv'))

    def test_opt_input_a(self):
        demand_a_1 = pd.read_csv('output_tests/optimizations/bias_0.0_sd_0.0/a/total_demand.csv')
        on_demand_a_1 = pd.read_csv('output_tests/optimizations/bias_0.0_sd_0.0/a/on_demand_config.csv')
        savings_plans_a_1 = pd.read_csv('output_tests/optimizations/bias_0.0_sd_0.0/a/savings_plan_config.csv')

        self.assertListEqual(list(demand_a_1['a.large']), [10, 10, 10])
        self.assertListEqual(list(demand_a_1['a.medium']), [1, 1, 1])

        self.assertListEqual(list(on_demand_a_1['instance']), ['a.large', 'a.medium'])
        self.assertListEqual(list(on_demand_a_1['hourly_price']), [2, 1])

        self.assertListEqual(list(savings_plans_a_1['instance']), ['a.large', 'a.medium'])
        self.assertListEqual(list(savings_plans_a_1['hourly_price']), [1, 0.5])
        self.assertListEqual(list(savings_plans_a_1['duration']), [8760, 8760])

        demand_a_2 = pd.read_csv('output_tests/optimizations/bias_0.1_sd_0.0/a/total_demand.csv')
        on_demand_a_2 = pd.read_csv('output_tests/optimizations/bias_0.1_sd_0.0/a/on_demand_config.csv')
        savings_plans_a_2 = pd.read_csv('output_tests/optimizations/bias_0.1_sd_0.0/a/savings_plan_config.csv')

        self.assertListEqual(list(demand_a_2['a.large']), [11, 11, 11])
        self.assertListEqual(list(demand_a_2['a.medium']), [1, 1, 1])

        self.assertListEqual(list(on_demand_a_2['instance']), ['a.large', 'a.medium'])
        self.assertListEqual(list(on_demand_a_2['hourly_price']), [2, 1])

        self.assertListEqual(list(savings_plans_a_2['instance']), ['a.large', 'a.medium'])
        self.assertListEqual(list(savings_plans_a_2['hourly_price']), [1, 0.5])
        self.assertListEqual(list(savings_plans_a_2['duration']), [8760, 8760])
    
        demand_a_3 = pd.read_csv('output_tests/optimizations/bias_0.2_sd_0.0/a/total_demand.csv')
        on_demand_a_3 = pd.read_csv('output_tests/optimizations/bias_0.2_sd_0.0/a/on_demand_config.csv')
        savings_plans_a_3 = pd.read_csv('output_tests/optimizations/bias_0.2_sd_0.0/a/savings_plan_config.csv')

        self.assertListEqual(list(demand_a_3['a.large']), [12, 12, 12])
        self.assertListEqual(list(demand_a_3['a.medium']), [1, 1, 1])

        self.assertListEqual(list(on_demand_a_3['instance']), ['a.large', 'a.medium'])
        self.assertListEqual(list(on_demand_a_3['hourly_price']), [2, 1])

        self.assertListEqual(list(savings_plans_a_3['instance']), ['a.large', 'a.medium'])
        self.assertListEqual(list(savings_plans_a_3['hourly_price']), [1, 0.5])
        self.assertListEqual(list(savings_plans_a_3['duration']), [8760, 8760])

    def test_opt_input_b(self):
        demand_b_1 = pd.read_csv('output_tests/optimizations/bias_0.0_sd_0.0/b/total_demand.csv')
        on_demand_b_1 = pd.read_csv('output_tests/optimizations/bias_0.0_sd_0.0/b/on_demand_config.csv')
        savings_plans_b_1 = pd.read_csv('output_tests/optimizations/bias_0.0_sd_0.0/b/savings_plan_config.csv')

        self.assertListEqual(list(demand_b_1['b.large']), [5, 5, 5])
        self.assertListEqual(list(demand_b_1['b.medium']), [3, 3, 3])

        self.assertListEqual(list(on_demand_b_1['instance']), ['b.large', 'b.medium'])
        self.assertListEqual(list(on_demand_b_1['hourly_price']), [4, 2])

        self.assertListEqual(list(savings_plans_b_1['instance']), ['b.large', 'b.medium'])
        self.assertListEqual(list(savings_plans_b_1['hourly_price']), [2, 1])
        self.assertListEqual(list(savings_plans_b_1['duration']), [8760, 8760])

        demand_b_2 = pd.read_csv('output_tests/optimizations/bias_0.1_sd_0.0/b/total_demand.csv')
        on_demand_b_2 = pd.read_csv('output_tests/optimizations/bias_0.1_sd_0.0/b/on_demand_config.csv')
        savings_plans_b_2 = pd.read_csv('output_tests/optimizations/bias_0.1_sd_0.0/b/savings_plan_config.csv')

        self.assertListEqual(list(demand_b_2['b.large']), [6, 6, 6])
        self.assertListEqual(list(demand_b_2['b.medium']), [3, 3, 3])

        self.assertListEqual(list(on_demand_b_2['instance']), ['b.large', 'b.medium'])
        self.assertListEqual(list(on_demand_b_2['hourly_price']), [4, 2])

        self.assertListEqual(list(savings_plans_b_2['instance']), ['b.large', 'b.medium'])
        self.assertListEqual(list(savings_plans_b_2['hourly_price']), [2, 1])
        self.assertListEqual(list(savings_plans_b_2['duration']), [8760, 8760])
    
        demand_b_3 = pd.read_csv('output_tests/optimizations/bias_0.2_sd_0.0/b/total_demand.csv')
        on_demand_b_3 = pd.read_csv('output_tests/optimizations/bias_0.2_sd_0.0/b/on_demand_config.csv')
        savings_plans_b_3 = pd.read_csv('output_tests/optimizations/bias_0.2_sd_0.0/b/savings_plan_config.csv')

        self.assertListEqual(list(demand_b_3['b.large']), [6, 6, 6])
        self.assertListEqual(list(demand_b_3['b.medium']), [4, 4, 4])

        self.assertListEqual(list(on_demand_b_3['instance']), ['b.large', 'b.medium'])
        self.assertListEqual(list(on_demand_b_3['hourly_price']), [4, 2])

        self.assertListEqual(list(savings_plans_b_3['instance']), ['b.large', 'b.medium'])
        self.assertListEqual(list(savings_plans_b_3['hourly_price']), [2, 1])
        self.assertListEqual(list(savings_plans_b_3['duration']), [8760, 8760])
