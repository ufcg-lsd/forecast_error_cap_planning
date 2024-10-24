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

## Objects

Contains the description of the objects used to store and transfer important data in this project.

### Demand

The demand for instances is a dictionary. The keys are the names of the instance types and the values are lists of integers, containing the demand for instances over time.

### Prices

The prices are stored in dictionary with the names of instance types as keys and objects of InstancePrices as values. This class has 9 attributes, containing the prices for the on-demand, reserve and savings plans. For the reserve and savings plans markets, contains the prices for each one of the 3 different purchasing options.