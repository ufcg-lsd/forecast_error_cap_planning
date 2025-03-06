# Impact of forecast error in cloud capacity planning

This repository contains the code for the experiment that analyses the cost of forecast error in cloud capacity planning. The starting point of this study is that long-term commitment plans for cloud resources are bought in advance, considering forecasts of future demand. However, as the forecasts are not perfect, the purchases of the plans are not the best possible. The aim of this experiment is to quantify the cost difference in the cloud allocation between buying long-term commitments with a perfect forecasts and forecasts with different levels of error.

The scripts that run the entire experiment are in the dir `scr/experiment`. Its `README.md` contains the details about running the experiment. There are two other modules: `src/forecast_generation` and `src/allocator`. They are used in the experiment and also have `README.md` files with more details.

## Running

This project uses Python 3 and Poetry for dependency management. To install the dependencies, run:

```
poetry install
```

For installing poetry, see the instructions in its [documentation](https://python-poetry.org/docs/)

## Files templates

Contains the templates that the files should follow throughout this project. All of them are csv files.

### Demand

The demand data file records the number of instances used for each instance type at specific times. The first column, `timestamp`, contains UNIX timestamps in seconds, representing each time interval. Subsequent columns correspond to instance types, such as `c5.large`, `t3.micro`, and `m5.xlarge`, with integer values indicating the demand (number of instances) for each type at the given timestamp.

| timestamp  | c5.large | ... | t3.micro | m5.xlarge |
|------------|----------|-----|----------|-----------|
| 1609459200 | 3        | ... | 5        | 2         |
| 1609462800 | 2        | ... | 4        | 3         |
| 1609466400 | 4        | ... | 2        | 1         |
| 1609470000 | 3        | ... | 6        | 4         |
| 1609473600 | 5        | ... | 7        | 2         |

### Prices

This CSV file contains AWS instance pricing details, covering both on-demand and reserved markets (including savings plans). For reserved markets, AWS offers three payment options:
- **All Upfront**: The entire cost of the reserved instance is paid at the beginning of the term.
- **Partial Upfront**: A portion is paid upfront, and the remainder is spread out with an hourly rate.
- **No Upfront**: No upfront cost; payment is made entirely through an hourly rate.

The CSV file includes the following six columns:
- `flavor`: Name of the instance type.
- `OnDemand`: Hourly rate for on-demand usage.
- `RAllUpfront1Y`: Total upfront price for a one-year commitment under the all upfront option in the reserved or savings plans market.
- `RPartialUpfront1YUP`: Upfront price for the one-year partial upfront option.
- `RPartialUpfront1YM`: Hourly rate for the one-year partial upfront option.
- `RNoUpfront1YM:` Hourly rate for the one-year no upfront option.

| flavor    | OnDemand | RAllUpfront1Y | RPartialUpfront1YUP | RPartialUpfront1YM | RNoUpfront1YM |
|-----------|----------|---------------|----------------------|--------------------|---------------|
| c5.large  | 0.096    | 500           | 300                 | 0.02               | 0.04          |
| t3.micro  | 0.0116   | 60            | 40                  | 0.005              | 0.007         |
| m5.xlarge | 0.192    | 1000          | 600                 | 0.04               | 0.08          |
| r5.large  | 0.126    | 650           | 390                 | 0.03               | 0.05          |
| t3.small  | 0.023    | 120           | 80                  | 0.006              | 0.008         |



### Alocation

The result of an allocation consists of two files.

The first one contains the number of instances in each market over time:

| timestamp |    market   | c4.2xlarge | c5.large | ... | md5.large |
|-----------|-------------|------------|----------|-----|-----------|
|     0     |  on_demand  |     10     |    15    | ... |    14     |
|     0     |    r_all    |      0     |     0    | ... |     0     |
|     0     |  r_partial  |     10     |     0    | ... |     1     |
|     0     |    r_no     |      5     |     5    | ... |     0     |
|   3600    |  on_demand  |     10     |    15    | ... |    14     |
|   3600    |    r_all    |      0     |     0    | ... |     0     |
|   3600    |  r_partial  |     10     |     0    | ... |     1     |
|   3600    |    r_no     |      5     |     5    | ... |     0     |

* `Timestamp`: Current time on your allocation
* `Market`: This column represents a specific market type at this timestamp
* `c4.2xlarge`, `c5.large`, ..., `md5.large`: The number of instances allocated for some instance type at a timestamp

The second one  contains the cost of each market over time:

| timestamp | OnDemand  | RAll | RPartialUp | RPartialHr | RNo | AllMarkets |
|-----------|-----------|------|------------|------------|-----|------------|
|     0     |    0.0    | 0.0  |  17372.0   |   500.04   | 0.0 |  17872.04  |
|    3600   |    0.0    | 0.0  |      0.0   |   500.04   | 0.0 |    500.04  |
|    7200   |    0.0    | 0.0  |      0.0   |   500.04   | 0.0 |    500.04  |

* `Timestamp`: current time on your allocation
* `OnDemand`: On-demand cost at this timestamp
* `RAll`: Reserve All Upfront costs at this timestamp
* `RPartialUp`: Upfront cost of the Reserve Partial Upfront option at this timestamp
* `RPartialHr`: Hourly cost of the Reserve Partial Upfront option at this timestamp
* `RNo`: Reserve No Upfront costs at this timestamp
* `AllMarkets`: The cost of all markets at this timestamp

Note that, for the savings plans markets, this file contains the cost of savings plans bought, but not used.

## Objects

Contains the description of the objects used to store and transfer important data in this project.

### Demand

The demand for instances is a dictionary. The keys are the names of the instance types and the values are lists of integers, containing the demand for instances over time.

### Prices

The prices are stored in dictionary with the names of instance types as keys and objects of InstancePrices as values. This class has 5 attributes, containing the prices for the on-demand and reserve or savings plans. For the reserve or savings plans markets, contains the prices for each one of the 3 different purchasing options.

### Allocation

The instances allocation is a dictionary containing 4 attributes, one for each market option. Each market contains another dictionary, with the instance types as keys and a list of integers as values. This list represents the number of instances of that instance type allocated to the market over time.

```
instance_allocation = {'OnDemand': {'a1.large': [], 't1.medium': []},
                     'RAll': {'a1.large': [], 't1.medium': []}, 
                     'RPartial': {'a1.large': [], 't1.medium': []}, 
                     'RNo': {'a1.large': [], 't1.medium': []}}
```

The cost of an allocation is a dictionary with the markets as keys and lists with floats as values:

```
cost_allocation = {'OnDemand': [], 'RAll': [], 'RPartialUp': [], 'RPartialHr': [], 'RNo': []}
```

## Credits

This project used both code and docs from the repository [AWSome-Savings](https://github.com/ufcg-lsd/AWSome-Savings).