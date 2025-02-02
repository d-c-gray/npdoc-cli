"""
Type Hinting
============

The type of command line argument is inferred from the type hinting
of the functions signature.
"""

from npdoc_cli import cli

@cli.program
def hello(name: str):
    """
    Say hello!

    Parameters
    ----------
    name : str
        Who is being greeted.
    """
    print('hello',name)

cli.build()
cli.print_help()




