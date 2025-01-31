""" Given the input and output files of the optimizations, converts to the file structure used by the experiment
"""

import os
import sys
import shutil
import pandas as pd

def main():
    path = sys.argv[1]

    for family in os.listdir(path):
        if os.path.isdir(f'{path}/{family}'):
            #create the dir input
            os.mkdir(f'{path}/{family}/input')

            #move total_demand.csv to input as demand.csv
            demand = pd.read_csv(f'{path}/{family}/total_demand.csv')
            demand.rename(columns={'hour': 'timestamp'}, inplace=True)
            demand.to_csv(f'{path}/{family}/input/demand.csv', index=False)
            os.remove(f'{path}/{family}/total_demand.csv')

            #create cost_allocation.csv from total_purchases_savings_plans
            total_purchases_sp = pd.read_csv(f'{path}/{family}/output/total_purchases_savings_plan.csv')
            sp_values = total_purchases_sp['value_active'].tolist()

            final_t =  len(sp_values)
            cost_allocation = {'timestamp': [i for i in range(final_t)], 'OnDemand': [0 for i in range(final_t)], 'RAll': [0 for i in range(final_t)], 'RPartialUp': [0 for i in range(final_t)], 'RPartialHr': [0 for i in range(final_t)], 'RNo': sp_values}
            cost_allocation_df = pd.DataFrame(cost_allocation)
            cost_allocation_df.to_csv(f'{path}/{family}/input/cost_allocation.csv', index=False)

            #delete output dir
            shutil.rmtree(f'{path}/{family}/output')

            #delete on_demand_config.csv and savings_plans_config.csv
            os.remove(f'{path}/{family}/on_demand_config.csv')
            os.remove(f'{path}/{family}/savings_plan_config.csv')

            #creates empty output dir
            os.mkdir(f'{path}/{family}/output')

if __name__ == '__main__':
    main()