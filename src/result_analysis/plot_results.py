import click
import pandas as pd
import matplotlib.pyplot as plt

@click.command()
@click.argument('results_path', type=click.Path(exists=True))
@click.option('--mode', type=click.Choice(['only_bias', 'bias_and_sd'], case_sensitive=False), default='bias_and_sd',
              help='Choose which type of experiment to plot: only_bias (only bias varies) or bias_and_sd.')
@click.option('--on-demand-cost', 'on_demand_cost', type=float, default=None,
              help='If provided, draw a horizontal red line at this y value representing 100% on-demand relative cost.')
@click.option('--plot-metrics', 'plot_metrics', is_flag=True, default=False,
              help='When set, and when using `only_bias` mode, also plot summary metrics `rel_tc_sp_idle` and `rel_tc_total_used` from summarize_results output.')
@click.option('--name', 'name', type=str, default=None,
              help='Name of the experiment, to be displayed in the graph')
@click.option('--y-upper-limit', 'y_upper_limit', type=float, default=None,
              help='Upper limit for the y-axis')
@click.option('--y-lower-limit', 'y_lower_limit', type=float, default=None,
              help='Lower limit for the y-axis')
def main(results_path, mode, on_demand_cost, plot_metrics, name, y_upper_limit, y_lower_limit):
    """CLI entrypoint to plot experiment results.

    The results CSV file must contain at least `bias_level`, `sd_level`, and `relative_cost`.
    """
    results_df = pd.read_csv(results_path)
    fig, ax = create_plot(results_df, mode, on_demand_cost, plot_metrics, name, y_upper_limit, y_lower_limit)
    plt.show()

def create_plot(results_df, mode='bias_and_sd', on_demand_cost=None, plot_summary_metrics=False, name=None, y_upper_limit=None, y_lower_limit=None):
    """Create a matplotlib figure for the given results and return (fig, ax).

    Args:
        results: DataFrame containing experiment results.
        mode: Either `bias_and_sd` to plot multiple sd lines or `only_bias` for only-bias experiments.
        on_demand_cost: Optional value to draw a horizontal 100% on-demand cost line.

    Returns:
        (fig, ax) tuple.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    if mode == 'bias_and_sd':
        plot_bias_and_sd(results_df, ax)
    elif mode == 'only_bias':
        plot_only_bias(results_df, ax, plot_summary_metrics=plot_summary_metrics)
    else:
        raise ValueError("mode must be 'bias_and_sd' or 'only_bias'")

    if on_demand_cost is not None:
        plot_on_demand_line(ax, on_demand_cost)

    ax.set_xlabel('Bias Level')
    ax.set_ylabel('Cost (%, relative to base total cost)')

    if name is not None:
        ax.set_title(f'Impact of Forecast Error in Cost - {name}')
    else:
        ax.set_title('Impact of Forecast Error in Cost')
    ax.legend()
    ax.grid(True)

    if y_upper_limit is not None:
        ax.set_ylim(top=y_upper_limit)

    if y_lower_limit is not None:
        ax.set_ylim(bottom=y_lower_limit)

    fig.tight_layout()
    return fig, ax

def plot_bias_and_sd(results_df, ax):
    """Plot results containing both bias and sd variation.

    Draws one line per `sd_level`.

    Args:
        results_df: DataFrame with results to plot.
        ax: Matplotlib axis where the lines will be drawn.
    """
    sd_levels = sorted(list(set(results_df['sd_level'])))
    colors = ['gold', 'orange', 'orangered']

    for i, sd_level in enumerate(sd_levels):
        results_sd_level = results_df[results_df['sd_level'] == sd_level]
        results_sd_level = results_sd_level.sort_values(by=['bias_level'])
        color = colors[i % len(colors)]
        ax.plot(results_sd_level['bias_level'], results_sd_level['relative_cost'], marker='o', linestyle='-', label=f'SD Level={sd_level}', color=color)


def plot_only_bias(results_df, ax, plot_summary_metrics=False):
    """Plot results that vary only bias (no sd variation).

    In this case there will be a single line for all bias levels.

    Args:
        results_df: DataFrame with results to plot.
        ax: Matplotlib axis where the line will be drawn.
    """
    results_df = results_df.sort_values(by=['bias_level'])

    if 'relative_cost' in results_df.columns:
        ax.plot(results_df['bias_level'], results_df['relative_cost'], marker='o', linestyle='-', label='Total Cost', linewidth=2)
    elif 'rel_total_cost' in results_df.columns:
        ax.plot(results_df['bias_level'], results_df['rel_total_cost'], marker='o', linestyle='-', label='Total Cost', linewidth=2)
    else:
        raise ValueError("Neither 'relative_cost' nor 'rel_total_cost' column found in results_df")
    
    if plot_summary_metrics:
        if 'rel_tc_sp_idle' in results_df.columns:
            ax.plot(results_df['bias_level'], results_df['rel_tc_sp_idle'], marker='o', linestyle='-', label='Savings Plans Idle', color='green', linewidth=1)
        else:
            pass

        if 'rel_tc_total_used' in results_df.columns:
            ax.plot(results_df['bias_level'], results_df['rel_tc_total_used'], marker='o', linestyle='-', label='Total Value Used', color='purple', linewidth=1)
        else:
            pass

        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)


def plot_on_demand_line(ax, on_demand_cost):
    """Plot a horizontal red line representing 100% on-demand cost.

    Args:
        ax: Matplotlib axis where the line will be drawn.
        on_demand_cost: Draw a horizontal red line at this y value and
            add a legend entry for it.
    """
    ax.axhline(y=on_demand_cost, color='red', linestyle='--', label='100% on-demand')


if __name__ == '__main__':
    main()