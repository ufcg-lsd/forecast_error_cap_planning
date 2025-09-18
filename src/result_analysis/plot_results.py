import click
import pandas as pd
import matplotlib.pyplot as plt

@click.command()
@click.argument('results_path', type=click.Path(exists=True))
@click.option('--mode', type=click.Choice(['only_bias', 'bias_and_sd'], case_sensitive=False), default='bias_and_sd',
              help='Choose which type of experiment to plot: only_bias (only bias varies) or bias_and_sd.')
@click.option('--on-demand-cost', 'on_demand_cost', type=float, default=None,
              help='If provided, draw a horizontal red line at this y value representing 100% on-demand relative cost.')
def main(results_path, mode, on_demand_cost):
    """CLI entrypoint to plot experiment results.

    The results CSV file must contain at least `bias_level`, `sd_level`, and `relative_cost`.
    """
    results_df = pd.read_csv(results_path)
    fig, ax = create_plot(results_df, mode=mode, on_demand_cost=on_demand_cost)
    plt.show()

def create_plot(results_df, mode='bias_and_sd', on_demand_cost=None):
    """Create a matplotlib figure for the given results and return (fig, ax).

    Args:
        results: DataFrame containing experiment results.
        mode: Either `bias_and_sd` to plot multiple sd lines or `only_bias` for only-bias experiments.
        on_demand_cost: Optional value to draw a horizontal 100% on-demand cost line.

    Returns:
        (fig, ax) tuple.
    """
    fig, ax = plt.subplots()

    if mode == 'bias_and_sd':
        plot_bias_and_sd(results_df, ax)
    elif mode == 'only_bias':
        plot_only_bias(results_df, ax)
    else:
        raise ValueError("mode must be 'bias_and_sd' or 'only_bias'")

    if on_demand_cost is not None:
        plot_on_demand_line(ax, on_demand_cost)

    ax.set_xlabel('Bias Level')
    ax.set_ylabel('Relative Cost')
    ax.set_title('Impact of Forecast Error in Cost')
    ax.legend()
    ax.grid(True)

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


def plot_only_bias(results_df, ax):
    """Plot results that vary only bias (no sd variation).

    In this case there will be a single line for all bias levels.

    Args:
        results_df: DataFrame with results to plot.
        ax: Matplotlib axis where the line will be drawn.
    """
    results_df = results_df.sort_values(by=['bias_level'])
    ax.plot(results_df['bias_level'], results_df['relative_cost'], marker='o', linestyle='-')


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