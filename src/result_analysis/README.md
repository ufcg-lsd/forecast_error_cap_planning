# Result Analysis

This folder contains scripts to analyze the results produced by the experiment. Use these scripts to aggregate costs, compare scenarios and produce plots.

## Summarize Results

`summarize_results.py` produces a CSV summary containing, for each scenario in an experiment, the costs for several metrics, both absolute and relative to the base scenario.

Inputs:
- `results_dir`: Path to the top-level results directory of an experiment.
- `output_file`: Path to write the output CSV summary.
- `prices_path`: Path to the prices file, as defined in the projects README.

Options:
- `--res_duration` (int, default 8760): Reserve duration in hours. Default is one year (8760 hours).
- `--base_scenario` (str, default `bias_0.0_sd_0.0`): Scenario used as the baseline when computing relative costs.
- `--process` (choice: `abs_costs`, `relative_costs`, `all`, default `all`): Select which data to include in the output. `abs_costs` will keep only absolute cost columns, `relative_costs` will compute and keep only relative cost columns, and `all` writes both absolute and relative columns.

Outputs
- The script writes a CSV file with one row per scenario. Columns include:
	- `bias_level`, `sd_level`: Scenario parameters.
	- `total_cost`: Total cost of the scenario, including all markets.
    - `od_cost`: Cost for only the on-demand market.
    - `sp_cost`: Cost for only the savings plans market.
	- `sp_used`: Part of the cost of the savings plans market that was effectivelly used to purchase instances.
    - `sp_idle`: Part of the cost of the savings plans market that was not used to purchase instances, being idle.
	- `total_used`: sum of the savings plans used and on-demand costs (`sp_used` + `od_cost`).
	- When `--process` includes relative costs, additional columns are added: `diff_sp_idle`,
		`diff_total_used`, `diff_total_cost`, `rel_sp_idle`, `rel_total_used`, `rel_tc_sp_idle`,
		`rel_tc_total_used`, `rel_total_cost`.
    - `diff_sp_idle`, `diff_total_used`, `diff_total_cost`: absolute cost difference to the same data of the base scenario (only computed when `--process` includes the relative costs).
    - `rel_sp_idle`, `rel_total_used`, `rel_total_cost`: relative cost difference (in percentage) to the same data of the base scenario (only computed when `--process` includes the relative costs).
    - `rel_tc_sp_idle`, `rel_tc_total_used`: relative cost difference (in percentage) to the total cost of the execution (`total_cost`) of the base scenario (only computed when `--process` includes the relative costs).

To run:

```
python3 summarize_results.py {path_of_experiment_results_dir} {path_of_output_file} {path_of_prices_file} --res_duration {num_hours_reserve_duration} --base_scenario {name_of_base_scenario} --process {which_info_to_process}
```

An example:

```
python3 summarize_results.py ../experiment/output/exec_2_2_2023_spot/ summirize_results_complete.py util/prices.csv--res_duration 8760 --base_scenario bias_0.0_sd_0.0 --process all
```

## Plot Results

`plot_results.py` generates simple matplotlib plots from the results CSV file produced by the experiment (or any CSV with the same columns).

Inputs
- `results_path`: Path to the results CSV file, which should contain at least the columns `bias_level`, `sd_level`, and `relative_cost`.

Options
- `--mode` (choice: `only_bias`, `bias_and_sd`, default `bias_and_sd`): Choose the plot type. Use `only_bias` when `sd_level` does not vary and you want a single line; use `bias_and_sd` to draw one line per `sd_level`.
- `--on-demand-cost` (float, optional): If provided, draws a horizontal line at the provided value, that should be the relative cost of the 100% on-demand strategy.
- `--plot-metrics` (flag, default off): When set and using `only_bias` mode, additionally plot summary metrics produced by `summarize_results.py` such as `rel_tc_sp_idle` and `rel_tc_total_used`.
- `--name` (string, optional): A short name for the experiment to display in the plot title.
- `--y-upper-limit` (float, optional): Upper limit for the y-axis.
- `--y-lower-limit` (float, optional): Lower limit for the y-axis. 

To run:

```
python3 plot_results.py {path_of_results_csv} --mode {which_type_of_plot} --on-demand-cost {relative_on_demand_cost} --plot-metrics --name {name_of_the_experiment} --y-upper-limit {value_of_the_y_axis_upper_limit} --y-lower-limit {value_of_the_y_axis_lower_limit}
```

Examples:

```
python3 plot_results.py output/exec_2_2_2023_spot/summary.csv --mode bias_and_sd
```

```
python3 plot_results.py output/exec_only_bias/summary.csv --mode only_bias --on-demand-cost 1.2 --plot-metrics --name data_2023 --y-upper-limit 50 --y-lower-limit 20
```

The script will open an interactive matplotlib window showing the plot.