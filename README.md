# Impact of forecast error in cloud capacity planning


## Files templates

Contains the templates that the files should follow throughout this project. All of them are csv files.

### Demand

The demand contains the information about number of instances used of each instance type over time. The first column of the csv is 'timestamp', with integer as values. The other columns have the name of the instance type, such as 'c5.large' or 't3.micro'. The values of the instance types correpond to their demands over time and need to be integers.

### Prices

Contains the prices used by AWS. For the reserve markets (including savings plans), AWS provides 3 different purchasing options. In the all upfront option, the entire value of the reserve is paid at the beginning, while, with the no upfront option, the costumer should pay a hourly value. The partial upfront option is a mix of the two others, consisting of both upfront and hourly payments. The prices csv should contain 6 columns:

- flavor: name of the instance type;
- OnDemand: hourly price for the on-demand market;
- RAllUpfront1Y: upfront price for the all upfront option of the reserve or savings plans market;
- RPartialUpfront1YUP: upfront price for the partial upfront option of the reserve or savings plans market;
- RPartialUpfront1YM: hourly price for the partial upfront option of the reserve or savings plans market;
- RNoUpfront1YM: hourly price for the no upfront option of the reserve or savings plans market.

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

* Timestamp: current time on your allocation
* Market: this column represents a specific market type at this timestamp
* c4.2xlarge, c5.large, ..., md5.large: the number of instances allocated for some instance type at a timestamp

The second one  contains the cost of each market over time:

| timestamp | OnDemand  | RAll | RPartialUp | RPartialHr | RNo | AllMarkets |
|-----------|-----------|------|------------|------------|-----|------------|
|     0     |    0.0    | 0.0  |  17372.0   |   500.04   | 0.0 |  17872.04  |
|    3600   |    0.0    | 0.0  |      0.0   |   500.04   | 0.0 |    500.04  |
|    7200   |    0.0    | 0.0  |      0.0   |   500.04   | 0.0 |    500.04  |

* Timestamp: current time on your allocation
* OnDemand: On-demand cost at this timestamp
* RAll: Reserve All Upfront costs at this timestamp
* RPartialUp: Upfront cost of the Reserve Partial Upfront option at this timestamp
* RPartialHr: Hourly cost of the Reserve Partial Upfront option at this timestamp
* RNo: Reserve No Upfront costs at this timestamp
* AllMarkets: The cost of all markets at this timestamp

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