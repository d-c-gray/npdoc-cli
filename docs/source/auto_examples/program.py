"""
Creating a Program
==================

This example doesn't do much, it just makes a simple plot
"""

from npdoc_cli import cli

@cli.program
def display(string: str):
    """
    Display a string in the console

    Parameters
    ----------
    string : str
        String to be displayed.

    Returns
    -------
    None.

    """
    print(string)

cli.build()
args = cli.parse_args(['myvalue'])
cli.dispatch(args)