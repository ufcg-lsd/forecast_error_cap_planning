import unittest
from unittest.mock import patch
import os
import subprocess
import pandas as pd
import numpy as np
from parameterized import parameterized
from src.forecast_generation import forecast_main

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

    ################### No Error ###################

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

        out = subprocess.run(f'python3 forecast_cli.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        result = pd.read_csv('output_tests/demand_bias_0.0_sd_0.0.csv')

        self.assertEqual(result['a.large'].tolist(), [10, 10, 10, 10, 10, 10, 10, 10])
        self.assertEqual(result['a.medium'].tolist(), [10, 8, 3, 5, 11, 20, 15, 19])
    
    ################### Only Bias ###################
    
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

        out = subprocess.run(f'python3 forecast_cli.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
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

        out = subprocess.run(f'python3 forecast_cli.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
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

        out = subprocess.run(f'python3 forecast_cli.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
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

        out = subprocess.run(f'python3 forecast_cli.py demand.csv error_configs.csv output_tests --error_option {error_option}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        result_1 = pd.read_csv('output_tests/demand_bias_-0.1_sd_0.0.csv')
        self.assertEqual(result_1['a.large'].tolist(), [9, 9, 9, 9, 9, 9, 9, 9])
        self.assertEqual(result_1['a.medium'].tolist(), [9, 7, 3, 4, 10, 18, 14, 17])

        result_2 = pd.read_csv('output_tests/demand_bias_0.1_sd_0.0.csv')
        self.assertEqual(result_2['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result_2['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])
    
        result_3 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.0.csv')
        self.assertEqual(result_3['a.large'].tolist(), [10, 10, 10, 10, 10, 10, 10, 10])
        self.assertEqual(result_3['a.medium'].tolist(), [10, 8, 3, 5, 11, 20, 15, 19])

    ################### Only Sd ###################

    @parameterized.expand([1, 2, 3, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_one_config_sd(self, error_option, mock_get_snormal):
        error_option = 1
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.0],
                  'sd_level': [0.1]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_0.0_sd_0.1.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])

    @parameterized.expand([1, 2, 3, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_two_configs_sd(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.0, 0.0],
                  'sd_level': [0.1, 0.2]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')
        mock_get_snormal.assert_called_with(8)

        result_1 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.1.csv')
        self.assertEqual(result_1['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result_1['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])

        result_2 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.2.csv')
        self.assertEqual(result_2['a.large'].tolist(), [12, 12, 12, 12, 12, 12, 12, 12])
        self.assertEqual(result_2['a.medium'].tolist(), [12, 10, 4, 6, 13, 24, 18, 23])

    @parameterized.expand([1, 2, 3, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_three_configs_sd(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.0, 0.0, 0.0],
                  'sd_level': [0.05, 0.1, 0.2]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')
        mock_get_snormal.assert_called_with(8)

        result_1 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.05.csv')
        self.assertEqual(result_1['a.large'].tolist(), [10, 10, 10, 10, 10, 10, 10, 10])
        self.assertEqual(result_1['a.medium'].tolist(), [10, 8, 3, 5, 12, 21, 16, 20])

        result_2 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.1.csv')
        self.assertEqual(result_2['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result_2['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])
    
        result_3 = pd.read_csv('output_tests/demand_bias_0.0_sd_0.2.csv')
        self.assertEqual(result_3['a.large'].tolist(), [12, 12, 12, 12, 12, 12, 12, 12])
        self.assertEqual(result_3['a.medium'].tolist(), [12, 10, 4, 6, 13, 24, 18, 23])

    @parameterized.expand([1, 2, 3, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1.5, 0.5, 0, -1, -0.5, 1, 0.5, -2])) 
    def test_variable_distribution_sd(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.0],
                  'sd_level': [0.1]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_0.0_sd_0.1.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [12, 10, 10, 9, 10, 11, 10, 8])
        self.assertEqual(result['a.medium'].tolist(), [12, 8, 3, 4, 10, 22, 16, 15])

    ################### Bias and Sd ###################


    ############### Options 1 and 3 ###############

    @parameterized.expand([1, 3])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_one_config_sd_bias_positive(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.05],
                  'sd_level': [0.05]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_0.05_sd_0.05.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])
    
    @parameterized.expand([1, 3])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_one_config_sd_bias_negative(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [-0.1],
                  'sd_level': [0.2]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_-0.1_sd_0.2.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 16, 21])

    @parameterized.expand([1, 3])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1.5, 0.5, 0, -1, -0.5, 1, 0.5, -2])) 
    def test_variable_distribution_sd_bias(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.1],
                  'sd_level': [0.1]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_0.1_sd_0.1.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [12, 12, 11, 10, 10, 12, 12, 9])
        self.assertEqual(result['a.medium'].tolist(), [12, 9, 3, 5, 12, 24, 17, 17])

    ############### Options 2 and 4  ###############

    @parameterized.expand([2, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_one_config_sd_bias_positive(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.05],
                  'sd_level': [0.05]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_0.05_sd_0.05.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result['a.medium'].tolist(), [11, 9, 3, 6, 12, 22, 17, 21])
    
    @parameterized.expand([2, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1, 1, 1, 1, 1, 1, 1, 1])) 
    def test_one_config_sd_bias_negative(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [-0.1],
                  'sd_level': [0.2]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_-0.1_sd_0.2.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [11, 11, 11, 11, 11, 11, 11, 11])
        self.assertEqual(result['a.medium'].tolist(), [11, 9, 3, 5, 12, 22, 16, 21])

    @parameterized.expand([2, 4])
    @patch('src.forecast_generation.forecast_main.get_snormal', return_value=np.array([1.5, 0.5, 0, -1, -0.5, 1, 0.5, -2])) 
    def test_variable_distribution_sd_bias(self, error_option, mock_get_snormal):
        demand = {'timestamp': [0, 1, 2, 3, 4, 5, 6, 7],
                  'a.large': [10, 10, 10, 10, 10, 10, 10, 10],
                  'a.medium': [10, 8, 3, 5, 11, 20, 15, 19]}

        demand_df = pd.DataFrame(demand)
        demand_df.to_csv('demand.csv', index=False)

        error_configs = {'bias_level': [0.1],
                  'sd_level': [0.1]}
        
        error_configs_df = pd.DataFrame(error_configs)
        error_configs_df.to_csv('error_configs.csv', index=False)

        forecast_main.main('demand.csv', 'error_configs.csv', error_option, 'output_tests')

        result = pd.read_csv('output_tests/demand_bias_0.1_sd_0.1.csv')

        mock_get_snormal.assert_called_with(8)
        self.assertEqual(result['a.large'].tolist(), [13, 12, 11, 10, 10, 12, 12, 9])
        self.assertEqual(result['a.medium'].tolist(), [13, 9, 3, 5, 11, 24, 17, 17])