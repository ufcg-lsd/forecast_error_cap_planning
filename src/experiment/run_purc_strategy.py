""" Runs one strategy to purchase savings plans.

In the experiment pipeline, the purchasing strategies receive the forecasted
demands and use them to purchase savings plans. The first strategy implemented
was the optimization tool. This CLI allows the implementation of several strategies,
given that they use the same input and output directory structure and files.
"""

import click

@click.command()
@click.argument('output_dir', type=click.Path(exists=True))
@click.option('--strategy', 
              type=str,
              default='optimization', 
              help='The purchasing strategy to use.')
def main(output_dir, strategy):
    pass

if __name__ == '__main__':
    main()