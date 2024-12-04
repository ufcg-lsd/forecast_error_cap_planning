# Experiment

Runs the complete experiment. It should be executed with *main.py* as a CLI, with the following parameters:

- `demand_path`: the path of the CSV file containing the demand for instances.
- `prices_path`: the path of the CSV file containing the prices of the instance types
- `error_configs_path`: the path of the CSV file containing the error configurations. Each configuration contains a level of bias and deviation.
- `cost_allocation_path`: the path of the CSV file with the cost allocation, that contains the cost of each market type over time.
- `output_path`: the dir that will receive the output files. One CSV file is created for each error configuration.

The directory *example_input* contains examples of those two input files.

To run:

```
poetry run python3 main.py {path_of_demand_file} {path_of_prices_file} {path_of_error_configs_file} {path_of_cost_allocation_file} {path_of_output_dir}
```

An example:

```
poetry run python3 main.py example_input/demand.csv example_input/prices.csv example_input/error_configs.csv example_input/cost_allocation.csv example_output
```

## Tests

The tests for the allocator are in *test_experiment.py*. To run all tests:

```
poetry run python3 -m unittest
```

To run a single test:

```
poetry run python3 -m unittest test_experiment.TestExperiment.{name of the test case}
```