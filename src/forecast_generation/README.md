# Forecast generation

Given a demand, create variations to simulate forecasts of that demand, that contain a certain level of error. The error has two aspects: the bias and the deviation. Both are expressed as proportions of the demand and the bias can be negative.

To run:

```
poetry run python3 main.py {path_of_demand_file} {path_of_error_configs_file} {path_of_output_dir}
```

An example:

```
poetry run python3 main.py example_input/demand.csv example_input/error_configs.csv example_output
```