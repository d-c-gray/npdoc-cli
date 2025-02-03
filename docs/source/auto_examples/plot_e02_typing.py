"""
Function Signatures
===================

This tutorial goes over how npdoc-cli parses function signatures
affect the command line interface.
"""


from pathlib import Path
from npdoc_cli import cli

# %%
# Type Signatures
# ---------------
# Arguments given to the command line are cast into the provided type
# signature.


@cli.program
def hello(name: str, number: int):
    """
    Say hello!

    Parameters
    ----------
    name : str
        Who is being greeted.
    number : int
        Number of times to greet.
    """
    for i in range(number):
        print('hello', name)


cli.build()
args = cli.parse_args(['reader', '3'])
cli.dispatch(args)

# %%%
# Booleans
# --------
# Booleans are a special case, as simply casting any string to bool
# will results in ``True``. To create an optional argument with a 
# flag that stores ``True`` or ``False``, create a keyword argument
# in the function signature with the default value (when the option isn't 
# specified in the CLI).
cli.reset()
@cli.program
def flags(flag_false: bool = True, flag_true: bool = False):
    """
    Parameters
    ----------
    flag_false : bool, optional
        Flag a false value.
    flag_true : bool, optional
        Flag a true value
    """
    print(flag_false)
    print(flag_true)

cli.build()
print('-- dispatch --')
args = cli.parse_args(['--flag-false','--flag-true'])
cli.dispatch(args)

# %%%
# Custom Types
# ------------
# The type casting is called as ``<type>(argument)``, so any arbitrary type
# can be used in a signature provided it can be called with the raw
# string as an input.
cli.reset()


@cli.program
def show_path(path: Path):
    """
    Parameters
    ----------
    path : Path
        Path to show.

    """
    print(path, type(path))


cli.build()
args = cli.parse_args(['my/path/file.ext'])
cli.dispatch(args)

# %%%
# You can define your own types or use functions to parse the string.

cli.reset()


def hello(string):
    return 'hello ' + string


class my_int():
    def __init__(self, string):
        self.val = int(string)


@cli.program
def show_path(string: hello, count: my_int):
    """
    Parameters
    ----------
    string : hello
        hello to who?
    count : my_int
        hello how many times?

    """
    for i in range(count.val):
        print(string)


cli.build()
args = cli.parse_args(['reader', '3'])
cli.dispatch(args)

# %%
# Positional and Optional arguments
# ---------------------------------
# By default, positional arguments in the function signature are
# turned into positional arguments in the CLI. Keyword arguments
# are turned into optional arguments in the in the CLI

cli.reset()
@cli.program
def hello(name: str, number: int = 1):
    """
    Parameters
    ----------
    name : str
        Who is being greeted.
    number : int
        Number of times to greet.
    """
    for i in range(number):
        print('hello', name)

cli.build()
cli.print_help()

# %%%
# Lists
# -----
# Adding the ``list[type]`` to a function signature will
# tell the parser that function is to take multiple arguments.
# Each argument will be cast into the type enclosed in ``list[]``.
# By default, arguments with this signature will have the |argparse argument|_
# set to ``action = 'extend'`` and ``nargs = '+'``.

cli.reset()
@cli.program
def hello(names: list[str]):
    """
    Parameters
    ----------
    names : list[str]
        Who is being greeted.
    """
    for n in names: print(n)

cli.build()
cli.print_help()

