import unittest
import os
import subprocess
import pandas as pd
from parameterized import parameterized

class TestForecast(unittest.TestCase):

    def setUp(self):
        os.mkdir('output_tests')

    def safe_remove(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def tearDown(self):
        self.safe_remove('demand.csv')
        self.safe_remove('error_configs.csv')

        for file in os.listdir('output_tests'):
            file_path = os.path.join('output_tests', file)
            os.remove(file_path)
        os.rmdir('output_tests')

    @parameterized.expand([1, 2, 3, 4])
    def test_one_config_no_error(self, error_option):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.0],
                  'sd_level': [0.0]}

        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        out = subprocess.run(f'python3 main.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        result = pd.read_csv('output_tests/demand_bias_0.0_sd_0.0.csv')

        self.assertEqual(result['a.large'].tolist(), [10, 10, 10, 10, 10, 10, 10, 10])
        self.assertEqual(result['a.medium'].tolist(), [10, 8, 3, 5, 11, 20, 15, 19])
    
    @parameterized.expand([1, 2, 3, 4])
    def test_one_config_positive_bias(self, error_option):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.1],
                  'sd_level': [0.0]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        out = subprocess.run(f'python3 main.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        result = pd.read_csv('output_tests/demand_bias_0.1_sd_0.0.csv')

        self.assertEqual(result['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])

    @parameterized.expand([1, 2, 3, 4])
    def test_one_config_negative_bias(self, error_option):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [-0.1],
                  'sd_level': [0.0]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        out = subprocess.run(f'python3 main.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        result = pd.read_csv('output_tests/demand_bias_-0.1_sd_0.0.csv')

        self.assertEqual(result['a.large'].tolist(), [9, 9, 9, 9, 9, 9, 9, 9])
        self.assertEqual(result['a.medium'].tolist(), [9, 7, 3, 4, 10, 18, 14, 17])

    @parameterized.expand([1, 2, 3, 4])
    def test_two_configs_bias(self, error_option):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [-0.1, 0.1],
                  'sd_level': [0.0, 0.0]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        out = subprocess.run(f'python3 main.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        result_1 = pd.read_csv('output_tests/demand_bias_-0.1_sd_0.0.csv')
        self.assertEqual(result_1['a.large'].tolist(), [9, 9, 9, 9, 9, 9, 9, 9])
        self.assertEqual(result_1['a.medium'].tolist(), [9, 7, 3, 4, 10, 18, 14, 17])

        result_2 = pd.read_csv('output_tests/demand_bias_0.1_sd_0.0.csv')
        self.assertEqual(result_2['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result_2['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])

    @parameterized.expand([1, 2, 3, 4])
    def test_three_configs_bias(self, error_option):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [-0.1, 0.1, 0.0],
                  'sd_level': [0.0, 0.0, 0.0]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        out = subprocess.run(f'python3 main.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        result_1 = pd.read_csv('output_tests/demand_bias_-0.1_sd_0.0.csv')
        self.assertEqual(result_1['a.large'].tolist(), [9, 9, 9, 9, 9, 9, 9, 9])
        self.assertEqual(result_1['a.medium'].tolist(), [9, 7, 3, 4, 10, 18, 14, 17])

        result_2 = pd.read_csv('output_tests/demand_bias_0.1_sd_0.0.csv')
        self.assertEqual(result_2['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result_2['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])
    
        result_3 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.0.csv')
        self.assertEqual(result_3['a.large'].tolist(), [10, 10, 10, 10, 10, 10, 10, 10])
        self.assertEqual(result_3['a.medium'].tolist(), [10, 8, 3, 5, 11, 20, 15, 19])