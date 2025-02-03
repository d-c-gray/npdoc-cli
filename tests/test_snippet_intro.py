import sys
with open('tests/snippet_intro_out.txt','w') as sys.stdout:
    from npdoc_cli import cli
    
    @cli.program
    def hello(name: str):
        """
        Say hello!
    
        Parameters
        ----------
        name : str
            Who is being greeted.
        """
        print('hello', name)
    
    cli.build()
    cli.print_help()