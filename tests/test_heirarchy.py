"""Pytest functions for testing the command heirarchy."""
from npdoc_cli import cli

def test_subcommands():
    """Test for nesting subcommands, commands, and programs"""
    cli.reset()
    @cli.program
    def test_program():
        pass

    @cli.command
    class command2():
        @cli.subcommand
        def c2sub2(self):
            pass

        @cli.subcommand
        def c2sub1(self):
            pass

    @cli.command
    class command1():
        @cli.subcommand
        def c1sub1(self):
            pass

        @cli.subcommand
        def c1sub2(self):
            pass
    c1 = command1()
    cli.tree()
    cli.build()
    cli.parse_args(['command1','c1sub1'])
    cli.parse_args(['command1','c1sub2'])
    cli.parse_args(['command2','c2sub1'])
    cli.parse_args(['command2','c2sub2'])

def test_program_only():
    """Test that programs function properly"""
    cli.reset()
    @cli.program
    def test_program(arg1: str):
        """
        Summary

        Parameters
        ----------
        arg1 : str
            test argument.

        Returns
        -------
        None.

        """
        pass
    cli.build()
    args = cli.parse_args(['input'])
    if args.arg1 != 'input':
        assert args.arg1 == 'input'

    args = vars(args)
    # 1 arg + __routine__
    assert len(args) == 2

def test_commands_only():
    cli.reset()
    @cli.program
    def prog():
        """ Sample program."""
        pass
    @cli.command
    def comm(file: str):
        """
        Print a str.

        Parameters
        ----------
        file : str
            Print a file string.

        """
        print(file)
    cli.build()
    args = cli.parse_args(['comm','file/path'])
    assert args.file == 'file/path'
if __name__ == '__main__':
    test_commands_only()
