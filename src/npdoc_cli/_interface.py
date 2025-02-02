"""
Interface module for npdoc-cli.
"""
import argparse as _ap
import inspect as _inspect
import typing as _typing
import re as _re
from npdoc_cli._errors import CLIArgError
from numpydoc.docscrape import FunctionDoc as _scrape

class FunctionInput():
    """Class for organizing function inputs."""

    def __init__(self):
        self.pa = []
        """List of positional arguments for a function input."""
        self.kwa = {}
        """Dictionairy of keyword arguments for a function input."""
    def disp(self):
        print('args')
        for a in self.pa:
            print('   ',a)
        print('kwargs')
        for k,v in self.kwa.items():
            print(k,' : ', v)


class NumpyDocCommand():
    """
    Class for parsing function signatures/doc strings in argparse objects.
    """

    def __init__(self, obj: callable):
        """
        Initialize a :NumpyDocObject.

        Parses a callable object's doc strings to generate
        settings for an argparse parser object.

        Parameters
        ----------
        obj : callable
            Function or class definition being defined as a commmand.

        Attributes
        ----------
        obj: callable
            Object to derive argparse object from.
        fname: str
            Name of function (obj.__name__)

        Returns
        -------
        None.

        """
        self.obj = obj
        """Object called to and called during cli dispatch."""
        self.fname = obj.__name__
        """Name of ``obj``."""

    def __repr__(self):
        return 'NumpDocCommand:'+str(self.obj.__qualname__)

    def __str__(self):
        return self.fname

    @property
    def defaults(self) -> dict:
        """Dictionairy of keyword arguments and their default value"""
        func = self.obj
        signature = _inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not _inspect.Parameter.empty
        }

    @property
    def types(self) -> dict:
        """Dictionairy of arguments and types."""
        func = self.obj
        signature = _inspect.signature(func)
        return {
            k: v.annotation
            for k, v in signature.parameters.items()
        }

    def disp(self):
        """Print scraped settings for debugging."""
        a,b = self.scrape()
        a.disp()
        for bi in b:
            print('')
            bi.disp()

    def scrape(
            self,
            replace_underscores: bool = True
    ) -> FunctionInput:
        """
        Scrape doc strings and functions signature.

        Turns doc strings and function signatures into settings that can be
        passed into argparse to generate a command line interface.

        Parameters
        ----------
        replace_underscores : bool, optional
            Replace underscores in argument/function names with
            dashes, stylistic choice. The default is True.


        Raises
        ------
        CLIArgError
            If problem is found with an argument's signature or documentation.

        Returns
        -------
        parser_ins : :py:obj:`FunctionInput`
            Inputs to be passed into argparse.ArgumentParser
        arg_ins_ls : :py:obj:`FunctionInput`
            Inputs to be passed into argparse.ArgumentParser.add_argument

        """
        function = self.obj

        # output
        parser_ins = FunctionInput()
        arg_ins_ls = []

        # scrape signature and doc strings
        doc = _scrape(function)
        params = doc['Parameters']
        summary = ' '.join(doc['Summary'] + doc['Extended Summary'])
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
            arg_ins = FunctionInput()

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
                arg_ins.kwa['default'] = defaults[p.name]

            # bool flags require a default
            # check for matching names
            try:
                types[p.name]
            except KeyError:
                raise CLIArgError('signature doesnt match doc string. ' + str(function))

            if 'bool' in p.type:
                try:
                    default = defaults[p.name]
                except KeyError:
                    raise CLIArgError('Booleans must provide a default value.')

                # set flag action, opposite of default
                arg_ins.kwa['action'] = 'store_true'
                if default:
                    arg_ins.kwa['action'] = 'store_false'

            # handle typing, choices on non-bool things
            else:
                # handle nargs and type assignment
                ptype = types[p.name]
                if list == _typing.get_origin(ptype):
                    arg_ins.kwa['nargs'] = '+'
                    arg_ins.kwa['action'] =  'extend'
                    type_args = _typing.get_args(ptype)
                    arg_ins.kwa['type'] = type_args[0]
                # not a special type of input, pass as given
                else:
                    arg_ins.kwa['type'] = ptype
                
                # look for choices option
                # expecting {a, b, c}
                choices = _re.search(r'\{(.*?)\}', p.type)
                if choices is not None:
                    choices = choices.group(0).replace('{','').replace('}','')
                    choices = choices.split(', ')
                    arg_ins.kwa['choices'] = [
                        arg_ins.kwa['type'](c) for c in choices
                        ]

            # look for additional arguments CLI argument settings
            # expecting a line in description of argument that looks like
            # For CLI argument key = value, key2 = value.
            cli_line = [line for line in p.desc if 'For CLI argument ' in line]
            if cli_line:
                cli_line = cli_line[0]
                if cli_line[-1] != '.':
                    raise CLIArgError('Expected period at end of For ClI argument ' + str(function))
                cli_line = cli_line.replace('For CLI argument ','')[0:-1]
                cli_line = cli_line.split(', ')
                for setting in cli_line:
                    pair = setting.split(' = ')
                    if len(pair) != 2:
                        raise CLIArgError(
                            str(function) + ' CLI settings in argument doc should be csv of key = value spaces matter.'
                            )
                    arg_ins.kwa[pair[0]] = pair[1]


            # help
            arg_ins.kwa['help'] = ''.join(p.desc)

            # handle special cases where things populated that shouldn't be
            # passed to the parser

            # count actions shouldn't pass there type
            if 'action' in arg_ins.kwa:
                # this means it's a count
                if arg_ins.kwa['action'] == 'count':
                    if 'type' not in arg_ins.kwa or arg_ins.kwa['type'] != int:
                        raise CLIArgError(str(function)+': count action expected type int')
                    arg_ins.kwa.pop('type')

            # append to list
            arg_ins_ls.append(arg_ins)

        return parser_ins, arg_ins_ls


class NumpyDocCLI():
    """
    Class for generating a CLI from numpy doc strings and type signatures.
    """

    def __init__(self):
        self.entry = None
        """:py:obj:`NumpyDocCommand` of program entry point."""
        self.commands = []
        """List of :py:obj:`NumpyDocCommand` for program commands."""
        self.subcommands = {}
        """Dictionairy of :py:obj:`NumpyDocCommand` for each subcommands."""
        self.program_parser = None
        """ArgumentParser for program entry point."""
        self.command_parsers = []
        """ArgumentParser for each command."""
        self.subcommand_parsers = {}
        """ArgumentParser for each subcommand"""


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

    def _build_subparser(
            self,
            npdoc_command: NumpyDocCommand,
            parent_subparsers: _ap.ArgumentParser,
            scrape_settings: dict):
        """
        Build a argparse subparser.

        Parameters
        ----------
        npdoc_command : :py:obj`NumpyDocCommand`.
            Command to build.
        parent_subparsers : ArgumentParser
            Subparsers object to add the newly created parser to. If NONE, will
            be created as a new program entry point.
        scrape_settings : dict
            Additional settings to pass to :py:obj`NumpyDocCommand`.scrape.

        Returns
        -------
        ArgumentParser
            Parser object with settings defined by ``npdoc_command``.

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

        program = self._build_subparser(
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
                cparser = self._build_subparser(
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
                        sc = self._build_subparser(
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

    def dispatch(self, args: _ap.Namespace):
        """
        Dispatch command line arguments to a the right function.

        Parameters
        ----------
        args : _ap.Namespace
            Output of :py:meth:`NumpyDocCLI.parse_args`.

        Returns
        -------
        any
            Output of dispatched function.

        """
        a = vars(args)
        routine = a.pop('__routine__')
        return routine(**a)


cli = NumpyDocCLI()
"""
Instance of :py:obj:`NumpyDocCLI` for generating CLI's.
"""