import pandas as pd
import sys

def main():
    demand_path = sys.argv[1]
    output_path = sys.argv[2]
    start_index = sys.argv[3]
    end_index = sys.argv[4]
    df_demand = pd.read_csv(demand_path)

    # end index not inclusive
    df_demand = df_demand.iloc[int(start_index):int(end_index)]
    df_demand.reset_index(drop=True, inplace=True)
    df_demand.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()