"""Given a demand in number of instances per hour, calculates the total cost if all demand is served with on-demand instances.

This module provides a reusable function `aggregate_demand` that reads a
demand CSV (see `aux.read_demand`) and optionally a prices CSV (see
`aux.read_prices`) to filter instance types. It returns the aggregated
demand as a list of rows (first row is the header). A small Click CLI is
also provided to write the aggregated CSV to disk.
"""

import csv
import click

from .aux import read_demand, get_families, read_prices, select_types

@click.command()
@click.argument('demand_path', type=click.Path(exists=True))
@click.argument('prices_path', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def main(demand_path, prices_path, output_file):
    """CLI entrypoint that writes the aggregated demand CSV to `output_file`."""
    rows = aggregate_demand(demand_path, prices_path)

    if not rows:
        click.echo('No data to write.')
        return

    # Write CSV
    with open(output_file, mode='w', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerows(rows)

    click.echo(f'Wrote aggregated demand to {output_file}')

def aggregate_demand(demand_path, prices_path):
    """Aggregate instance-type demand to family-level demand.

    Args:
        demand_path: Path to the demand CSV. See `aux.read_demand` for format.
        prices_path: Optional path to a prices CSV. If provided, instance
            types without price entries will be ignored (via `select_types`).

    Returns:
        A list of rows where the first row is the header (`['timestamp', <families...>]`)
        and each subsequent row contains a timestamp followed by aggregated
        integer demand per family.
    """
    demand, timestamp = read_demand(demand_path)
    prices = read_prices(prices_path)

    instance_types = list(demand.keys())
    instance_types = [it for it in instance_types if it in prices]

    # Determine number of time-steps (n). Prefer the timestamp list if present.
    ts_list = timestamp.get('timestamp') if isinstance(timestamp, dict) else None
    n = None
    if ts_list:
        n = len(ts_list)
    else:
        # Fallback: find any demand series and use its length
        for values in demand.values():
            if values is not None:
                n = len(values)
                break

    if n is None:
        # No data found
        return []

    # Aggregate total demand across all selected instance types
    total = [0] * n
    for inst in instance_types:
        if inst not in demand:
            continue
        vals = demand[inst] or []
        # Normalize length: pad with zeros or truncate to n
        if len(vals) < n:
            vals = vals + [0] * (n - len(vals))
        elif len(vals) > n:
            vals = vals[:n]

        for i, v in enumerate(vals):
            try:
                total[i] += int(v)
            except Exception:
                total[i] += int(float(v))

    # Build output rows: header + rows per timestamp
    rows = []
    header = ["timestamp", "demand"]
    rows.append(header)

    # Use ts_list if available, otherwise use empty strings for timestamps
    for i in range(n):
        ts_val = ts_list[i] if ts_list and i < len(ts_list) else ""
        row = [ts_val, total[i]]
        rows.append(row)

    return rows

if __name__ == '__main__':
    main()