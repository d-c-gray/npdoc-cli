# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 12:05:26 2025

@author: coleg
"""
from pathlib import Path as Path
from npdoc_cli import cli

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
    cli.print_help()
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
    test_base_types()