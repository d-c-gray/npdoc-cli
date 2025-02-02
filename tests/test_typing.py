# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 12:05:26 2025

@author: coleg
"""
from pathlib import Path as Path
from npdoc_cli import cli, NumpyDocCommand

def test_actions():
    cli.reset()
    @cli.program
    def test(count: int = 0):
        """
        thing

        Parameters
        ----------
        count : int, optional
            Description
            For CLI argument action = count.

        Returns
        -------
        None.

        """
    doc = NumpyDocCommand(test)
    cli.build()
    a = cli.parse_args(['-ccc'])
    assert a.count == 3
    

def test_cli_requires():
    cli.reset()
    @cli.program
    def test(arg: int = 0):
        """
        thing

        Parameters
        ----------
        arg : int, optional, cli required
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
    cli.build()
    cli.parse_args(['-a','0'])

def test_nargs():
    cli.reset()
    @cli.program
    def test(ls: list[int]):
        """
        Thing.

        Parameters
        ----------
        ls : list[int]
            DESCRIPTION. The default is 0.

        """
    cli.build()
    args = cli.parse_args(['1','2','3'])
    expected = [1,2,3]
    assert all([e == a for a,e in zip(args.ls,expected)])

def test_choices():
    cli.reset()
    @cli.program
    def test(opt: float = 1.0):
        """
        Thing.

        Parameters
        ----------
        opt : {1.0, 2.0, 3.0}
            1.0, 2.0, or 3.0. The default is 0.

        """
    cli.build()
    # cli.print_help()
    npd = NumpyDocCommand(test)
    npd.disp()
    args = cli.parse_args([])
    assert args.opt == 1.0
    
    args = cli.parse_args(['-o','3.0'])
    assert args.opt == 3.0

    args = cli.parse_args(['-o','2.0'])
    assert args.opt == 2.0

def test_base_types():
    cli.reset()
    @cli.program
    def test_program(
            self,
            pint: int,
            pfloat: float,
            pstr: str,
            ppath: Path,
            false: bool = True,
            true: bool = False,
            ):
        """
        This is the summary of my function.
    
        Parameters
        ----------
        pint : int
            DESCRIPTION.
        pfloat : float
            DESCRIPTION.
        pstr : str
            DESCRIPTION.
        ppath : Path
            DESCRIPTION.
        false : bool, optional
            DESCRIPTION. The default is True.
        true : bool, optional
            DESCRIPTION. The default is False.
    
        Returns
        -------
        None.
    
        """
    cli.tree()
    cli.build()
    # cli.print_help()
    args = cli.parse_args([
        '1',
        '1.0',
        'input',
        'path',
        ])
    def check_val(val,typ):
        if type(val) != typ:
            raise ValueError(
                str(val) + 'should be'+ str(typ) + ', is ' + str(type(val))
                )

    check_val(args.pint,int)
    check_val(args.pfloat,float)
    check_val(args.pstr,str)
    check_val(args.ppath,type(Path('.')))
    assert args.false == True
    assert args.true == False
    assert args.__routine__ == test_program
    

if __name__ == '__main__':
    test_actions()
