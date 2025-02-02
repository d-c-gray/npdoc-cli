"""
Doc Strings
===========
In addition to parsing function signatures, the module assumes
that your functions are documenting using numpy style doc strings.

This tutorial goes over how to use the doc-strings to further customize
your CLI.
"""

from npdoc_cli import cli

# %%
# Summary
# -------
# The ``Summary`` and  ``Extended Summary`` of the doc string are converted into the
# help message of your parser. The descriptions in the ``Parameters`` section
# are converted into the help message for each argument

cli.reset()
@cli.program
def hello(name: str, number: int):
    """
    This is a summary line.

    This is an extended summary line.

    Parameters
    ----------
    name : str
        This is a help message.
    """
    for i in range(number):
        print('hello', name)


cli.build()
cli.print_help()

# %%
# Choices
# -------
# Sometimes a function expects specific choices.
# You can include those in the ``Parameters`` section, and they will be 
# added to the parser, which will check that a valid choice was passed
# as a command line argument.

cli.reset()
@cli.program
def options(o: str = 'a'):
    """
    Parameters
    ----------
    o : str, {a, b, c}
        This function expects a, b, or c.
    """
    print(o)

cli.build()
try:
    args = cli.parse_args(['-o', 'd'])
except SystemExit as e:
    print(e)

# %%
# Action, Nargs, and Required
# ---------------------------
# For the ``argparse.ArgumentParser.add_argument`` method, some settings
# don't fit nicely into the signature or numpydoc style guid. For those,
# you can include them in the argument description.
#
# These settings should be formatted as: 
# ``For CLI parser key = <val>...`` and ended with a period. The spaces and
# period are important and must be included properly on a single line.
#
# This line will not be included in the help message of the generated CLI.

cli.reset()
@cli.program
def options(mylist: list[str] = []):
    """
    Parameters
    ----------
    mylist : list[str]
        This function expects some strings.
        For CLI parser required = True, action = append, nargs = *.
    """
    print(mylist)

cli.build()
cli.print_help()
