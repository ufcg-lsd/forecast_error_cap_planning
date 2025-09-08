# Util

Usefull scripts for the project.

## Filter Demands

Filter a demand file, in the format used in the project, by time. Receives the orginal demand path, the filtered demand path and the start and end index. Note that, in pandas, the index starts with 0 and the end index is not inclusive.

Execution examples:

```
python3 filter_demands.py 2021_2023_with_spot.csv 2021_with_spot.csv 0 8760
```

```
python3 filter_demands.py 2021_2023_with_spot.csv 2022_with_spot.csv 8760 17520
```

## Check Optimizations Progress

Check the progress of the execution of the optimizations in a vm, by counting the number of families optimized compared to the total number of existing families. It receives as a parameter the name of that set of scenarios and has constants for the path of the executions and the vm's ip.

Execution example:

```
bash check_opt_progress.bash exec_2_2_2023_spot
```