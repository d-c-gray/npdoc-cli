"""
Creating a Program
==================

This is a basic example for generating a simple program
with npdoc_cli.

# The attribute ``cli`` is a pre-made instance of 
# :py:obj:`npdoc_cli.NumpyDocCLI` for easy access across different
# modules. It is the access point for the  module.
"""

from npdoc_cli import cli

# %% 
# Build the CLI
# -------------
# First, define an entry point into the program by wrapping
# a method in `cli.program()` and document your function with 
# type hinting and numpy style doc strings. When ``cli.build()``
# is called, the function's type hinting and doc strings will be
# parsed and converted into a command line interface.

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

# %%
# Dispatching to Functions
# ------------------------
# Calling ``cli.parse_args()`` will parse any command line arguments
# into an argparse NameSpace. Passing that through
# ``cli.dispatch()`` will route the arguments to the correct function.
#
# Normally, we would call ``cli.parse_args()`` as empty to get the
# arguments from the command line that invoked the program. For this
# example, we pass our own arguments as a list. Calling ``cli.dispatch(args)`` will pass the
# arguments from the command line to the correct function.

args = cli.parse_args(['reader'])
cli.dispatch(args)

# %%%
# The function is stored in the attribute ``args.__routine__``, and can be
# accessed and called manually if desired.

args = cli.parse_args(['reader'])
print(args.__routine__)
args = vars(args)
func = args.pop('__routine__')
func(**args)




