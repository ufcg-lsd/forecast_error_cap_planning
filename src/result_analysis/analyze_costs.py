""" Create a file and plots to help understing the results

Create a file that has the individual costs by family and scenario.
Plots one histogram for each scenario containing distribution of the 
relative costs by family.
Two sets of histograns are created, one with the relative costs to the heuristic
cost with perfect forecast and another with the relative costs to the optimization
cost with perfect forecast.
"""

# entender melhor os custos
    # dividir os custos por família --> grande tabela com custos finais de cada família para cada cenário
    # como é a distribuição dos custos? quantos aumentam? quantos ficam iguais?
        # cada uma das famílias teria um gráfico com os custos dos cenários
        # cada um dos 15 cenários teria um histograma/boxplot
    # analisar alguns cenários de famílias específicas com comportamentos interessantes ou estranhos

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import click
import os

@click.command()
@click.argument('results_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option('--res_duration',
              type=int,
              default=8760)
@click.option('--base_scenario',
              type=str,
              default='bias_0.0_sd_0.0')
def main(results_dir, output_dir, res_duration, base_scenario):
    costs_df = get_costs(results_dir, res_duration, base_scenario)
    costs_df.to_csv(os.path.join(output_dir, 'costs.csv'), index=False)

    plot_by_scenario(costs_df, output_dir)
    plot_by_scenario_opt(costs_df, output_dir)

def get_costs(results_dir, res_duration, base_scenario):
    """ Creates a dataframe with the costs by family and scenario
    """

    costs_df = pd.DataFrame(columns=['scenario', 'family', 'od_cost', 'sp_cost', 'total_cost', 'relative_cost', 'total_cost_opt', 'relative_cost_opt'])

    allocations_path = os.path.join(results_dir, 'allocations')
    opt_path = os.path.join(results_dir, 'optimizations')

    base_scenario_path = os.path.join(allocations_path, base_scenario)
    base_scenario_opt_path = os.path.join(opt_path, base_scenario)
    for family in os.listdir(base_scenario_path):
        alloc_cost, total_purchases_sp = read_alloc_files(family, base_scenario_path)
        
        od_cost = sum(alloc_cost['OnDemand'])
        sp_cost = sum(total_purchases_sp['value_reserves']) * res_duration
        total_cost = od_cost + sp_cost

        total_opt_cost = get_opt_cost(family, base_scenario_opt_path)

        if total_cost == 0 and total_opt_cost == 0:
            relative_cost_opt = 1
        else:
            relative_cost_opt = total_cost/total_opt_cost


        costs_df.loc[len(costs_df)] = [base_scenario, family, od_cost, sp_cost, total_cost, 1, total_opt_cost, relative_cost_opt]

    for scenario in os.listdir(allocations_path):
        if scenario != base_scenario:
            scenario_path = os.path.join(allocations_path, scenario)
            for family in os.listdir(scenario_path):
                alloc_cost, total_purchases_sp = read_alloc_files(family, scenario_path)
                
                od_cost = sum(alloc_cost['OnDemand'])
                sp_cost = sum(total_purchases_sp['value_reserves']) * res_duration
                total_cost = od_cost + sp_cost
        
                base_cost = costs_df.loc[
                    (costs_df['scenario'] == base_scenario) & (costs_df['family'] == family), 
                    'total_cost'
                ]
                base_cost = float(base_cost.iloc[0])

                base_cost_opt = costs_df.loc[
                    (costs_df['scenario'] == base_scenario) & (costs_df['family'] == family), 
                    'total_cost_opt'
                ]
                base_cost_opt = float(base_cost_opt.iloc[0])

                if base_cost == 0 and total_cost == 0 and base_cost_opt == 0:
                    relative_cost = 1
                    relative_cost_opt = 1
                else:
                    relative_cost = total_cost / base_cost
                    relative_cost_opt = total_cost/base_cost_opt

                costs_df.loc[len(costs_df)] = [scenario, family, od_cost, sp_cost, total_cost, relative_cost, -1, relative_cost_opt]
    
    return costs_df

def read_alloc_files(family, scenario_path):
    """ Reads alloc_cost and total_purchases for a family and scenario
    """
    
    family_path = os.path.join(scenario_path, family)
    alloc_cost_path = os.path.join(family_path, 'alloc_cost.csv')
    alloc_cost = pd.read_csv(alloc_cost_path)
    total_purchases_sp_path = os.path.join(family_path, 'total_purchases_sp.csv')
    total_purchases_sp = pd.read_csv(total_purchases_sp_path)

    return alloc_cost, total_purchases_sp
    

def get_opt_cost(family, base_scenario_opt_path):
    results_opt_dir = os.path.join(base_scenario_opt_path, family)
    results_opt_path = os.path.join(results_opt_dir, 'output/result_cost.csv')
    results_opt = pd.read_csv(results_opt_path)
    total_opt_cost = results_opt.loc[0, 'total_cost']

    return total_opt_cost

def plot_by_scenario(costs_df, output_dir):
    sns.set_style("whitegrid")    
    scenarios = costs_df['scenario'].unique()
    
    for scenario in scenarios:
        plt.figure(figsize=(6, 4))
        sns.histplot(costs_df[costs_df['scenario'] == scenario]['relative_cost'], bins=10, kde=True)
        plt.title(f'Scenario {scenario}')
        plt.xlabel('Total Cost (conpared to alloc heuristic with perfect forecast)')
        plt.ylabel('Frequency')
        
        output_path = os.path.join(output_dir, f'scenario_{scenario}.png')
        plt.savefig(output_path)
        plt.close()

def plot_by_scenario_opt(costs_df, output_dir):
    sns.set_style("whitegrid")  
    scenarios = costs_df['scenario'].unique()
    
    for scenario in scenarios:
        plt.figure(figsize=(6, 4))
        sns.histplot(costs_df[costs_df['scenario'] == scenario]['relative_cost_opt'], bins=10, kde=True)
        plt.title(f'Scenario {scenario}')
        plt.xlabel('Total Cost (compared to opt with perfect forecast)')
        plt.ylabel('Frequency')
        
        output_path = os.path.join(output_dir, f'compared_to_opt_{scenario}.png')
        plt.savefig(output_path)
        plt.close()

if __name__ == '__main__':
    main()