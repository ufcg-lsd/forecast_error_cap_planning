import os
import sys
import shutil
import pandas as pd

RES_DURATION = 8760

def main():
    path = sys.argv[1]
    demand_path = sys.argv[2]
    prices_path = sys.argv[3]

    #dividir demanda em famílias

    for family in families:
        os.mkdir(f'{path}/{family}')
        os.mkdir(f'{path}/{family}/output')

        #criar on_demand config

        od_config.to_csv(f'{path}/{family}/on_demand_config.csv', index=False)
        #criar sp_config

        sp_config.to_csv(f'{path}/{family}/savings_plan_config.csv', index=False)




if __name__ == '__main__':
    main()