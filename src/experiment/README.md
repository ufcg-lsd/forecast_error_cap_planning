# Experiment

Runs the complete experiment. It should be executed with *main.py* as a CLI, with the following parameters:

- `demand_path`: the path of the CSV file containing the demand for instances.
- `prices_path`: the path of the CSV file containing the prices of the instance types
- `error_configs_path`: the path of the CSV file containing the error configurations. Each configuration contains a level of bias and deviation.
- `cost_allocation_path`: the path of the CSV file with the cost allocation, that contains the cost of each market type over time.
- `output_path`: the dir that will receive the output files. One CSV file is created for each error configuration.

The directory *example_input* contains examples of those input files. Be aware that this experiment runs for one instance family only, so the demand should have only instance types of one family and the cost allocation should have the savings plans values for that family.

To run:

```
poetry run python3 main.py {path_of_demand_file} {path_of_prices_file} {path_of_error_configs_file} {path_of_cost_allocation_file} {path_of_output_dir}
```

An example:

```
poetry run python3 main.py example_input/demand.csv example_input/prices.csv example_input/error_configs.csv example_input/cost_allocation.csv example_output
```

## Multiple families

For running with multiple families, there is the script *run_multiple_families.py*. It calls the experiment multiple times, one for each family, and groups the results into two files (*summary.csv*, *detailed_summary.csv*). Note that the input should have a specific directory and file structure:

    └── families_path
        ├── family_a
        │   ├── input
        |   |   ├── demand.csv
        |   |   └── cost_allocation.csv
        |   └── output
        └── family_b
            ├── input
            |   ├── demand.csv
            |   └── cost_allocation.csv
            └── output

## Tests

The tests for the allocator are in *test_experiment.py*. To run all tests:

```
poetry run python3 -m unittest
```

To run a single test:

```
poetry run python3 -m unittest test_experiment.TestExperiment.{name of the test case}
```