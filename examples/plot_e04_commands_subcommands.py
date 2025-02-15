"""
Commands and Subcommands
========================

This module explains how to organize a CLI into different commands and
subcommands.
"""

from npdoc_cli import cli


# %%
# Commands
# --------
# Commands can be added to the program by using the wrapper ``cli.command`` on
# additional functions, and adding type hinting and documentation the same
# way you would a program. You can do this with multiple commands.

@cli.program
def program():
    """
    Description of program.

    """
    pass


@cli.command
def hello(name: str):
    """
    Say hello.

    Parameters
    ----------
    name : str
        Say hello to?.

    """
    print('hello', name)

@cli.command
def goodbye(name: str):
    """
    Say goodbye.

    Parameters
    ----------
    name : str
        Say goodbye to?.

    """
    print('goodbye', name)

cli.build()
cli.print_help()
print('--dispatch--')
args = cli.parse_args(['hello','reader'])
cli.dispatch(args)
args = cli.parse_args(['goodbye','reader'])
cli.dispatch(args)

# %%
# Subcommands
# -----------
# If you want, you can got one step further and
# organize subcommands under any command
# by instead wrapping ``cli.command`` around a class, and wrapping
# ``cli.subcommand`` around methods you would like to expose to the
# interface. Use a the static method wrapper if you don't need a class instance
# to invoke the call.

cli.reset()

@cli.program
def program():
    """
    Description of program.

    """
    pass

@cli.command
class say():
    """
    This is a command for saying things.
    """
    @cli.subcommand
    @staticmethod
    def hello(name: str):
        """
        Say hello.
    
        Parameters
        ----------
        name : str
            Say hello to?.
    
        """
        print('hello', name)

    @cli.subcommand
    @staticmethod
    def goodbye(name: str):
        """
        Say goodbye.

        Parameters
        ----------
        name : str
            Say goodbye to?.

        """
        print('goodbye', name)

cli.build(say())
args = cli.parse_args(['say', 'hello','reader'])
cli.dispatch(args)
args = cli.parse_args(['say', 'goodbye','reader'])
cli.dispatch(args)

# %%
# Class Instances
# ^^^^^^^^^^^^^^^
# By default, the build method will assign the class itself to call the
# routine when building the CLI. If your function requires an instance of the 
# class to call the function (i.e. an instance method) then you need to
# pass that instance to the build call ``cli.build(inst1,inst2,...)``.

cli.reset()

@cli.program
def program():
    """
    Description of program.

    """
    pass

@cli.command
class say():
    """
    This is a command for saying things.
    """
    def __init__(self,name:str):
        self.name = name

    @cli.subcommand
    def hello(self):
        """
        Say hello.

        """
        print('hello', self.name)

s = say('reader')
cli.build(s)
args = cli.parse_args(['say','hello'])
cli.dispatch(args)

# %%
# Resolution Order
# ----------------
# The :py:obj:`NumpyDocCLI` class (of which ``cli`` is an instance) delays
# building the CLI until ``cli.build()`` is called. You don't need to declare
# your programs/commands/subcommands in any particular order. By default,
# commands and subcommands will be added in the order they are defined.
# If they are spread out across modules, that will depend on the order the
# modules are imported. Optionally, you can change the sort setting when calling
# ``cli.build``.

cli.reset()

@cli.command
def hello(name: str):
    """
    Say hello.

    Parameters
    ----------
    name : str
        Say hello to?.

    """
    print('hello', name)

@cli.command
def goodbye(name: str):
    """
    Say goodbye.

    Parameters
    ----------
    name : str
        Say goodbye to?.

    """
    print('goodbye', name)

@cli.program
def program():
    """
    Description of program.

    """
    pass


print('-- unsorted --')
cli.build()
cli.print_help()
print('\n-- alphabetical --')
cli.build(sort = 'alphabetical')
cli.print_help()

