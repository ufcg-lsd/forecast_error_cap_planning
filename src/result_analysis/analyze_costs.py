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

    #plot_by_family(costs_df, output_dir)
    plot_by_scenario(costs_df, output_dir)

def get_costs(results_dir, res_duration, base_scenario):
    """ Creates a dataframe with the costs by family and scenario
    """

    costs_df = pd.DataFrame(columns=['scenario', 'family', 'od_cost', 'sp_cost', 'total_cost', 'relative_cost'])

    allocations_path = os.path.join(results_dir, 'allocations')

    base_scenario_path = os.path.join(allocations_path, base_scenario)
    for family in os.listdir(base_scenario_path):
        alloc_cost, total_purchases_sp = read_alloc_files(family, scenario_path)
        
        od_cost = sum(alloc_cost['OnDemand'])
        sp_cost = sum(total_purchases_sp['value_reserves']) * res_duration
        total_cost = od_cost + sp_cost

        costs_df.loc[len(costs_df)] = [base_scenario, family, od_cost, sp_cost, total_cost, 1]

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

                if base_cost == 0 and total_cost == 0:
                    relative_cost = 1
                else:
                    relative_cost = total_cost / base_cost

                costs_df.loc[len(costs_df)] = [scenario, family, od_cost, sp_cost, total_cost, relative_cost]
    
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
    
#def plot_by_family(costs_df, output_dir):

def plot_by_scenario(costs_df, output_dir):
    # Set the style
    sns.set_style("whitegrid")

    # Create histogram plots for each scenario
    scenarios = costs_df['scenario'].unique()
    fig, axes = plt.subplots(nrows=1, ncols=len(scenarios), figsize=(5 * len(scenarios), 4), sharey=True)

    if len(scenarios) == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one scenario

    for ax, scenario in zip(axes, scenarios):
        sns.histplot(costs_df[costs_df['scenario'] == scenario]['relative_cost'], bins=10, kde=True, ax=ax)
        ax.set_title(f'Scenario {scenario}')
        ax.set_xlabel('Total Cost')
        ax.set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()