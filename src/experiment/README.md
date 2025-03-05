# Experiment

This directory contains the scripts needed to run the entire experiment. There are three steps in the experiment: forecast generation, optimizations and allocator. There are also three scripts for running the experiment, that should be executed in that order:

- `before_opt.py`
- `run_opt.bash`
- `after_opt.py`

## Before Optimization

The script `before_opt.py` receives the total demand, prices and error configurations. It calls `forecast_generation` to create the demands for the simulated forecasts and, after that, sets up the file and directory structure for the optimizations.

To run:

```
poetry run python3 before_opt.py {path_of_total_demand} {path_of_prices} {path_of_error_configs} {path_of_output_dir}
```

An example:

```
poetry run python3 before_opt.py data/2023_with_spot.csv data/prices.csv data/error_configs.csv output/exec_2023_spot
```

## Optimizations

The optimizations use an external tool, that is used as a docker image, hosted on GitLab. Besides that, it is, by far, the step with the longest execution time. The script `run_opt.sh` reads the directory tree created before and, for each instance family, calls the optimization tool. It receives the path of the parent output directory. Each optimization execution is independent, but, with this script, they run sequentially.

To run:

```
sudo bash run_opt.sh {path_of_optimizations_dir}
```

An example:

```
sudo bash run_opt.sh ~/tcc-caio/src/experiment/output/exec_2023_spot/
```

Note the command should be run with sudo (because of docker) and the path should be the absolute path. It also should have the last `/` for the script to work.

## After Optimization

The final step, after the optimizations, is to run the allocator, that calculates the real cost of the usage of the savings plans purchased acording to the optimizations. The script `after_opt.py` calls the allocator with the output of the optimizations and calculates the final cost of each forecast scenario, creating a csv file with the results. It receives the prices, the main output directory, the name of the base forecast scenario (by default bias_0.0_sd_0.0) and the path of the results csv file.

To run:

```
poetry run python3 after_opt.py {path_of_prices} {path_of_output} {path_of_results_file} --base_scenario {name_of_base_scenario}
```

An example:

```
poetry run python3 after_opt.py data/prices.csv output/exec_2023_spot output/exec_2023_spot/results.csv --base_scenario bias_0.0_sd_0.0
```

## Output Directory

The scripts save the results of the experiment in a directory specified by the user, including the intermediate files. It should be empty before calling the first script. After all the scripts, this directory should look like that:

```
output
├── results.csv
├── allocations
|   ├── bias_0.0_sd_0.0
|   |   ├── a1
|   |   |   ├── alloc_cost.csv
|   |   |   ├── alloc_instance.csv
|   |   |   └── purchases_sp.csv
|   |   ├── c1
|   |   └── c3
|   ├── bias_0.0_sd_0.1
|   └── bias_0.0_sd_0.05
├── forecasts
|   ├── demand_bias_0.0_sd_0.0.csv
|   ├── demand_bias_0.0_sd_0.1.csv
|   └── demand_bias_0.0_sd_0.05.csv
└── optimizations
    ├── bias_0.0_sd_0.0
    |   ├── a1
    |   |   ├── output
    |   |   |   ├── result_cost.csv  
    |   |   |   ├── total_purchases_a1.large.csv
    |   |   |   ├── total_purchases_a1.medium.csv
    |   |   |   └── total_purchases_savings_plans.csv
    |   |   ├── on_demand_config.csv
    |   |   ├── savings_plans_config.csv
    |   |   └── total_demand.csv
    |   ├── c1
    |   └── c3
    ├── bias_0.0_sd_0.1
    └── bias_0.0_sd_0.05
```

Each forecast scenario is independent, having separe total costs. Inside each scenario, there are several instance families. The optimization tool and the allocator receive the family input, so they run one time for each family.