"""
Naming
======

This module explains how naming rules can be applied to a CLI.
"""

from npdoc_cli import cli


# %%
# Dashes and Underscores
# ----------------------
# It's common for CLI to use dashes to seperate words when naming variables
# in the terminal, however Python obviously won't support that. 
# By default, ``cli.build()`` will turn replace underscores in program, command
# subcommand and argument names. You can turn this off in the build call.

@cli.program
def prog_name(my_arg: int, my_option: float = 0):
    """
    Summary.

    Parameters
    ----------
    my_arg : int
        DESCRIPTION.
    my_option : float,optional
        DESCRIPTION
    """
    pass

print('-- replace underscores --')
cli.build()
cli.print_help()

print('-- keep underscores --')
cli.build(replace_underscores=False)
cli.print_help()

# %%
# Short Flags
# -----------
# All keyword arguments are assigned a short flag and a long flag as
# optional arguments in the CLI. Long
# flags will always be the python arguments name as it exists in python + whatever
# naming rules are applied to the build call. However, the short flag will
# use the first letter of the argument's name. If another argument exists with
# that flag, it will keep adding letters until a unique short flag is created.
# In that respect, the order of arguments in the function signature will
# determine the short flag if arguments have similar names.

cli.reset()
@cli.program
def prog_name(option1: int = 0, option2: float = 0):
    """
    Summary.

    Parameters
    ----------
    option1 : int
        DESCRIPTION.
    option2 : float,optional
        DESCRIPTION
    """
    pass

cli.build()
cli.print_help()
