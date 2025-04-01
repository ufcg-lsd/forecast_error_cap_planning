# verificar se os diretórios e arquivos de allocations estão sendo criados
# verificar se purchases_sp.csv está correto

import os
import unittest
import subprocess
import shutil
import pandas as pd

class TestAfterOpt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir('output_tests')
        cls.create_files()
        out = subprocess.run(f'poetry run python3 before_opt.py demand.csv prices.csv error_configs.csv output_tests --res_duration 4 --error_option 1', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        cls.create_opt_results()
        out = subprocess.run(f'poetry run python3 after_opt.py prices.csv output_tests --res_duration 4', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

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

    def create_opt_results():
        # bias_0.0_sd_0.0
        purc_sp = {'hour': [0, 1, 2],
                'market': ['savings_plan', 'savings_plan', 'savings_plan'],
                'value_active': [5, 5, 5],
                'value_reserves': [5, 0, 0]}

        purc_sp_df = pd.DataFrame(purc_sp)
        purc_sp_df.to_csv('output_tests/optimizations/bias_0.0_sd_0.0/a/output/total_purchases_savings_plan.csv', index=False)

        purc_sp = {'hour': [0, 1, 2],
                'market': ['savings_plan', 'savings_plan', 'savings_plan'],
                'value_active': [10, 10, 10],
                'value_reserves': [10, 0, 0]}

        purc_sp_df = pd.DataFrame(purc_sp)
        purc_sp_df.to_csv('output_tests/optimizations/bias_0.0_sd_0.0/b/output/total_purchases_savings_plan.csv', index=False)

        # bias_0.1_sd_0.0
        purc_sp = {'hour': [0, 1, 2],
                'market': ['savings_plan', 'savings_plan', 'savings_plan'],
                'value_active': [5, 5, 5],
                'value_reserves': [5, 0, 0]}

        purc_sp_df = pd.DataFrame(purc_sp)
        purc_sp_df.to_csv('output_tests/optimizations/bias_0.1_sd_0.0/a/output/total_purchases_savings_plan.csv', index=False)

        purc_sp = {'hour': [0, 1, 2],
                'market': ['savings_plan', 'savings_plan', 'savings_plan'],
                'value_active': [10, 10, 10],
                'value_reserves': [10, 0, 0]}

        purc_sp_df = pd.DataFrame(purc_sp)
        purc_sp_df.to_csv('output_tests/optimizations/bias_0.1_sd_0.0/b/output/total_purchases_savings_plan.csv', index=False)

        # bias_0.2_sd_0.0
        purc_sp = {'hour': [0, 1, 2],
                'market': ['savings_plan', 'savings_plan', 'savings_plan'],
                'value_active': [5, 5, 5],
                'value_reserves': [5, 0, 0]}

        purc_sp_df = pd.DataFrame(purc_sp)
        purc_sp_df.to_csv('output_tests/optimizations/bias_0.2_sd_0.0/a/output/total_purchases_savings_plan.csv', index=False)

        purc_sp = {'hour': [0, 1, 2],
                'market': ['savings_plan', 'savings_plan', 'savings_plan'],
                'value_active': [10, 10, 10],
                'value_reserves': [10, 0, 0]}

        purc_sp_df = pd.DataFrame(purc_sp)
        purc_sp_df.to_csv('output_tests/optimizations/bias_0.2_sd_0.0/b/output/total_purchases_savings_plan.csv', index=False)

    def safe_remove(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def test_dir_structure(self):
        self.assertTrue(os.path.isdir('output_tests/allocations'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.0_sd_0.0'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.1_sd_0.0'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.2_sd_0.0'))

        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.0_sd_0.0/a'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.1_sd_0.0/a'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.2_sd_0.0/a'))

        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.0_sd_0.0/b'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.1_sd_0.0/b'))
        self.assertTrue(os.path.isdir('output_tests/allocations/bias_0.2_sd_0.0/b'))

    def test_files(self):
        self.assertTrue(os.path.isfile('output_tests/results.csv'))

        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.0_sd_0.0/a/alloc_instance.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.1_sd_0.0/a/alloc_instance.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.2_sd_0.0/a/alloc_instance.csv'))

        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.0_sd_0.0/a/alloc_cost.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.1_sd_0.0/a/alloc_cost.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.2_sd_0.0/a/alloc_cost.csv'))

        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.0_sd_0.0/b/alloc_instance.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.1_sd_0.0/b/alloc_instance.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.2_sd_0.0/b/alloc_instance.csv'))

        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.0_sd_0.0/b/alloc_cost.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.1_sd_0.0/b/alloc_cost.csv'))
        self.assertTrue(os.path.isfile('output_tests/allocations/bias_0.2_sd_0.0/b/alloc_cost.csv'))
    
    def test_alloc_a(self):
        alloc_cost_a_1 = pd.read_csv('output_tests/allocations/bias_0.0_sd_0.0/a/alloc_cost.csv')

        self.assertListEqual(list(alloc_cost_a_1['OnDemand']), [5*2 + 1*1, 5*2 + 1*1, 5*2 + 1*1])
        self.assertListEqual(list(alloc_cost_a_1['RNo']), [5, 5, 5])
        self.assertListEqual(list(alloc_cost_a_1['AllMarkets']), [16, 16, 16])
    
        alloc_cost_a_2 = pd.read_csv('output_tests/allocations/bias_0.1_sd_0.0/a/alloc_cost.csv')

        self.assertListEqual(list(alloc_cost_a_2['OnDemand']), [5*2 + 1*1, 5*2 + 1*1, 5*2 + 1*1])
        self.assertListEqual(list(alloc_cost_a_2['RNo']), [5, 5, 5])
        self.assertListEqual(list(alloc_cost_a_2['AllMarkets']), [16, 16, 16])

        alloc_cost_a_3 = pd.read_csv('output_tests/allocations/bias_0.2_sd_0.0/a/alloc_cost.csv')

        self.assertListEqual(list(alloc_cost_a_3['OnDemand']), [5*2 + 1*1, 5*2 + 1*1, 5*2 + 1*1])
        self.assertListEqual(list(alloc_cost_a_3['RNo']), [5, 5, 5])
        self.assertListEqual(list(alloc_cost_a_3['AllMarkets']), [16, 16, 16])

    def test_alloc_b(self):
        alloc_cost_b_1 = pd.read_csv('output_tests/allocations/bias_0.0_sd_0.0/b/alloc_cost.csv')

        self.assertListEqual(list(alloc_cost_b_1['OnDemand']), [3*2, 3*2, 3*2])
        self.assertListEqual(list(alloc_cost_b_1['RNo']), [10, 10, 10])
        self.assertListEqual(list(alloc_cost_b_1['AllMarkets']), [16, 16, 16])
    
        alloc_cost_b_2 = pd.read_csv('output_tests/allocations/bias_0.1_sd_0.0/b/alloc_cost.csv')

        self.assertListEqual(list(alloc_cost_b_2['OnDemand']), [3*2, 3*2, 3*2])
        self.assertListEqual(list(alloc_cost_b_2['RNo']), [10, 10, 10])
        self.assertListEqual(list(alloc_cost_b_2['AllMarkets']), [16, 16, 16])

        alloc_cost_b_3 = pd.read_csv('output_tests/allocations/bias_0.2_sd_0.0/b/alloc_cost.csv')

        self.assertListEqual(list(alloc_cost_b_3['OnDemand']), [3*2, 3*2, 3*2])
        self.assertListEqual(list(alloc_cost_b_3['RNo']), [10, 10, 10])
        self.assertListEqual(list(alloc_cost_b_3['AllMarkets']), [16, 16, 16])

    def test_results(self):
        results = pd.read_csv('output_tests/results.csv')

        results.sort_values('bias_level', axis=0, ascending=True, inplace=True)

        self.assertListEqual(list(results['bias_level']), [0.0, 0.1, 0.2])
        self.assertListEqual(list(results['sd_level']), [0.0, 0.0, 0.0])
        self.assertListEqual(list(results['cost']), [111, 111, 111])
        self.assertListEqual(list(results['relative_cost']), [1, 1, 1])