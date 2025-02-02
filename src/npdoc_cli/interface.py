"""
Interface module for npdoc-cli.

Attributes
----------
cli: _NumpyDocCLI
    Class instance accessed for generating and defining the CLI from numpy
    doc strings.
NARGS_TYPES: list
    Types in this list are, when found in function signatures, assigned
    the nargs setting when calling argparse.ArgumentParser.add_argument.

"""
import argparse as _ap
import inspect as _inspect
import typing as _typing
from npdoc_cli.errors import CLIArgError
from numpydoc.docscrape import FunctionDoc as _scrape


NARGS_TYPES = [
    list,
    tuple,
    _typing.Tuple,
]


class _FunctionInput():
    """
    Class for organizing function inputs.

    Attributes
    ----------
    pa: list
        List of positional arguments.
    kwa:
        Dictionairy of key-word arguments.
    """

    def __init__(self):
        self.pa = []
        self.kwa = {}


class NumpyDocCommand():
    """
    Class for parsing function signatures/doc strings in argparse objects.

    Attributes
    ----------
    obj: callable
        Object to derive argparse object from.
    fname: str
        Name of function (obj.__name__)

    """

    def __init__(self, obj: callable):
        """
        Initialize a a NumpyDocObject.

        Parses a callable object's doc strings to generate
        settings for an argparse parser object.

        Parameters
        ----------
        obj : callable
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.obj = obj
        self.fname = obj.__name__

    def __repr__(self):
        return 'NumpDocCommand:'+str(self.obj.__qualname__)

    def __str__(self):
        return self.fname

    @property
    def defaults(self) -> dict:
        """
        Get dictionairy of keyword arguments and their default value.

        Returns
        -------
        dict
            Keys are argumentnames, values are defaults.

        """
        func = self.obj
        signature = _inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not _inspect.Parameter.empty
        }

    @property
    def types(self) -> dict:
        """
        Get dictionairy of arguments and types.

        Returns
        -------
        dict
            keys are argument names, values are argument type signature.

        """
        func = self.obj
        signature = _inspect.signature(func)
        return {
            k: v.annotation
            for k, v in signature.parameters.items()
        }

    def scrape(
            self,
            nargs: str = '+',
            replace_underscores: bool = True
    ) -> _FunctionInput:
        """
        Scrape doc strings and functions signature.

        Turns doc strings and function signatures into settings that can be
        passed into argparse to generate a command line interface.

        Parameters
        ----------
        nargs : str, optional
            How to handle multiple arguments. Type signatures in
            See nargs in npdoc_cli.NARG_TYPES are given this setting.
            See argparse documentation on nargs for more info.
            The default is '+'.
        replace_underscores : bool, optional
            Replace underscores in argument/function names with
            dashes, stylistic choice. The default is True.

        Raises
        ------
        CLIArgError
            If problem is found with an argument's signature or documentation.

        Returns
        -------
        parser_ins : _FunctionInput
            Inputs to be passed into argparse.ArgumentParser
        arg_ins_ls : _FunctionInput
            Inputs to be passed into argparse.ArgumentParser.add_argument

        """
        function = self.obj

        # output
        parser_ins = _FunctionInput()
        arg_ins_ls = []

        # scrape signature and doc strings
        doc = _scrape(function)
        params = doc['Parameters']
        summary = doc['Summary']
        defaults = self.defaults
        types = self.types

        # parser inputs

        # add command line name
        cli_name = function.__name__
        if replace_underscores:
            cli_name = cli_name.replace('_', '-')
        parser_ins.pa.append(cli_name)
        parser_ins.kwa['description'] = ''.join(summary)

        used_flags = []
        for p in params:
            arg_ins = _FunctionInput()
            # add command line name
            cli_name = p.name
            if replace_underscores:
                cli_name = cli_name.replace('_', '-')

            # positional arguments
            if p.name not in defaults:
                arg_ins.pa.append(cli_name)

            # not positional, so has a flag
            else:
                # make a short and long flag
                short = ''
                for s in cli_name:
                    short += s
                    if short not in used_flags:
                        used_flags += [short]
                        break
                arg_ins.pa.append('-' + short)
                arg_ins.pa.append('--' + cli_name)

                # flag as a required key word argument or not
                arg_ins.kwa['required'] = 'cli required' in p.type

            # bool flags require a default
            if 'bool' in p.type:
                try:
                    default = defaults[p.name]
                except KeyError:
                    raise CLIArgError('Booleans must provide a default value.')

                # set flag action, opposite of default
                arg_ins.kwa['action'] = 'store_true'
                if default:
                    arg_ins.kwa['action'] = 'store_false'

            # handle typing on non-bool things
            else:
                ptype = types[p.name]
                arg_ins.kwa['type'] = ptype

                # inspect for typings with 'nargs'
                if any([str(n) in str(ptype) for n in NARGS_TYPES]):
                    arg_ins.kwa['nargs'] = '+'

            # help
            arg_ins.kwa['help'] = ''.join(p.desc)

            # append to list
            arg_ins_ls.append(arg_ins)

        return parser_ins, arg_ins_ls


class _NumpyDocCLI():
    """
    Class for generating a CLI from numpy doc strings and type signatures.

    Attributes
    ----------
    entry: NumpyDocCommand
        Function that acts as entry point command, was wrapped by
        _NumpyDocCLI.program.
    commands: list[NumpyDocCommand]
        List of functions that are commands for entry.
    subcommands: dict[NumpyDocCommand]
        Dictionairy of subcommands for each command.

    """

    def __init__(self):
        self.entry = None
        self.commands = []
        self.subcommands = {}
        self.program_parser = None
        self.subcommand_parsers = {}
        self.command_parsers = []

    def reset(self):
        """
        Reset CLI to empty.

        Returns
        -------
        None.

        """
        self.commands = []
        self.subcommands = {}
        self.entry = None

    def program(self, function: callable) -> callable:
        """
        Wrapper function to define the entry point.

        Parameters
        ----------
        function : callable
            That is called.

        Returns
        -------
        function : callable
            The passed function, unmodified.

        """
        self.entry = NumpyDocCommand(function)
        return function

    def command(self, obj: object) -> object:
        """
        Wrapper function to defined commands for entry point.

        Parameters
        ----------
        obj : object
            Class definition if using subcommands, function it not.

        Returns
        -------
        object
            Same object passed as input, unmodified.

        """
        c = NumpyDocCommand(obj)
        self.commands.append(c)
        return obj

    def subcommand(self, function: callable) -> callable:
        """
        Wrapper function to define subcommands for a command.

        Parameters
        ----------
        function : object
            Function to be called as subcommand. Should belong as submethod
            to its parent commmand's class definition.

        Returns
        -------
        function : callable
            Same function passed, unmodified.

        """
        parent = function.__qualname__.split('.')[-2]
        sc = NumpyDocCommand(function)
        try:
            self.subcommands[parent].append(sc)
        except KeyError:
            self.subcommands[parent] = [sc]
        return function

    def tree(self):
        """
        Print program/command/subcommand heirarchy.

        Returns
        -------
        None.

        """
        print('----------------')
        print('CLI Command Tree')
        print('----------------')
        print(self.entry.fname)
        for c in self.commands:
            print('   >', c)
            for s in self.subcommands[c.fname]:
                print(' '*7, '>', s)
        print('----------------')

    def build_subparser(
            self,
            npdoc_command: NumpyDocCommand,
            parent_subparsers: _ap.ArgumentParser,
            scrape_settings: dict):
        """
        Build a argparse subparser.

        Parameters
        ----------
        npdoc_command : NumpyDocCommand
            Command to build.
        parent_subparsers : _ap.ArgumentParser
            subparsers object to add the newly created parser to. If NONE, will
            be created as a new program entry point.
        scrape_settings : dict
            Additional settings to pass to NumpyDocCommand.scrape.

        Returns
        -------
        argparse.ArgumentParser
            Parser object with settings defined by npdoc_command.

        """

        parser_ins, arg_ins = npdoc_command.scrape(**scrape_settings)

        if parent_subparsers:
            sparser = parent_subparsers.add_parser(
                *parser_ins.pa,
                **parser_ins.kwa
            )
        else:
            sparser = _ap.ArgumentParser(
                prog=parser_ins.pa[0],
                **parser_ins.kwa
            )
            sparser.set_defaults(__routine__=npdoc_command.obj)
        for a in arg_ins:
            sparser.add_argument(
                *a.pa,
                **a.kwa
            )

        return sparser

    def build(self,
              *command_instances: object,
              replace_underscores: bool = True,
              alphabetical: bool = True
              ):
        """
        Build a CLI.

        Parameters
        ----------
        *instances : object
            Instances of classes wrapped in command to use when calling
            subcommands. If an instance of a command wrapped class is not
            passed, the class itself will be used to call the subcommand.
        replace_underscores : bool, optional
            Repace underscores in argument/command names with dashes.
            The default is True.
        alphabetical : bool, optional
            Sort commands and subcommands alphabetically. The default is True.

        Returns
        -------
        None.

        """
        scrape_sets = dict(
            replace_underscores=replace_underscores
        )

        program = self.build_subparser(
            self.entry,
            None,
            scrape_sets
        )

        commands = []
        subcommands = {}

        if self.commands:
            program_subparsers = program.add_subparsers(help='command help')
            if alphabetical:
                cnames = [c.fname for c in self.commands]
                self.commands = [c for _, _, c in sorted(
                    zip(cnames, cnames, self.commands))]

            for c in self.commands:
                # add sparser for program
                cparser = self.build_subparser(
                    c,
                    program_subparsers,
                    scrape_sets)

                subs = None
                if c.fname in self.subcommands:
                    subs = self.subcommands[c.fname]
                if subs:
                    # add subparser for subcommands
                    subcommands[c] = []
                    command_subparsers = cparser.add_subparsers(
                        help='subcommand help')
                    # sort if asked to
                    if alphabetical:
                        cnames = [c.fname for c in subs]
                        subs = [c for _, _, c in sorted(
                            zip(cnames, cnames, subs))]

                    # build parser for each subcommand
                    for s in subs:
                        sc = self.build_subparser(
                            s,
                            command_subparsers,
                            scrape_sets)
                        subcommands[c].append(sc)

        self.program_parser = program
        self.command_parsers = commands
        self.subcommand_parsers = subcommands

    def parse_args(self, args: list[str] = None) -> _ap.Namespace:
        """
        Parse command line arguments.

        See argparse.ArgumentParser.parse_args for more info.

        Parameters
        ----------
        args : list[str], optional
            List of arguments to parse. If None, parses from command line.

        Returns
        -------
        argparse.Namespace
            Parsed arguments.

        """
        return self.program_parser.parse_args(args)

    def print_help(self):
        """
        Print help string for CLI

        Returns
        -------
        None.

        """
        self.program_parser.print_help()


cli = _NumpyDocCLI()
