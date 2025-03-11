# Forecast generation

Given a demand, create variations to simulate forecasts of that demand, containing a certain level of error. The error has two aspects: the bias and the deviation. Both are expressed as proportions of the demand and the bias can be negative. It should be executed with *main.py* as a CLI, with the following parameters:

- `demand_path`: the path of the CSV file containing the demand for instances.
- `error_configs_path`: the path of the CSV file containing the error configurations. Each configuration contains a level of bias and deviation.
- `output_path`: the dir that will receive the output files. One CSV file is created for each error configuration.
- `error_option`: chooses the way in which the error is added into the demand.

The directory *example_input* contains examples of those two input files.

To run:

```
poetry run python3 main.py {path_of_demand_file} {path_of_error_configs_file} {path_of_output_dir} --error_option {number_of_error_option}
```

An example:

```
poetry run python3 main.py example_input/demand.csv example_input/error_configs.csv example_output --error_option 1
```

## Error generation

The error is generated using two parameters: `bias_level` and `sd_level`. The bias level is a value that multiples the entire demand and can be positive or negative. On the other hand, the standard deviation level determines the level in which a random normal distribution is added in the demand. The ideia behind it is to increase the variability of the demand. The random normal distribution is a list of numbers generated with the size of the demand. It is multiplied by the standard deviation level and added to the original demand. In the code, there are two ways of creating the list containing the random normal distribution. The first one is to create a different list for each instance type in each forecast error scenario. This creates more variability inside the demand and between the different scenarios. The other option is to create a single list and use it for all the instance types in all the scenarios. Besides that, there are two formulas for adding the error: 

- new_demand[instance_type] = round(demand[instance_type] * (1 + bias_level + sd_level * snormal))
- new_demand[instance_type] = round(demand[instance_type] * (1 + bias_level) * (1 + (sd_level * snormal)))

The second one creates a commulative effect between the bias and the standard deviation levels, increasing the overall error.

Combining the two options for the random normal distribution and the two options for the formula, we finish with four options for error generation:

- 1: individual normal distribution generation and first formula;
- 2: individual normal distribution generation and second formula;
- 3: global normal distribution generation and first formula;
- 4: global normal distribution generation and second formula.

## Tests

The tests for the forecast generation are in *test_forecast.py*. To run all tests:

```
poetry run python3 -m unittest
```

To run a single test:

```
poetry run python3 -m unittest test_forecast.TestForecast.{name of the test case}