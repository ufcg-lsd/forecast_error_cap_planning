# Forecast generation

Given a demand, create variations to simulate forecasts of that demand, containing a certain level of error. The error has two aspects: the bias and the deviation. Both are expressed as proportions of the demand and the bias can be negative. It should be executed with *main.py* as a CLI, with the following parameters:

- `demand_path`: the path of the CSV file containing the demand for instances.
- `error_configs_path`: the path of the CSV file containing the error configurations. Each configuration contains a level of bias and deviation.
- `output_path`: the dir that will receive the output files. One CSV file is created for each error configuration.

The directory *example_input* contains examples of those two input files.

To run:

```
poetry run python3 main.py {path_of_demand_file} {path_of_error_configs_file} {path_of_output_dir}
```

An example:

```
poetry run python3 main.py example_input/demand.csv example_input/error_configs.csv example_output
```