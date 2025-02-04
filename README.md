# npdoc-cli
A tool built with [argparse](https://docs.python.org/3/library/argparse.html)
that utilizes the [numpy style guide](https://numpydoc.readthedocs.io/en/latest/format.html)
to generate a command line interface (CLI). Paired with auto-generated
documentation with [sphinx](https://www.sphinx-doc.org/en/master/) you can
maintain a function's source code, documentation, and CLI all with the same
chunk of text.

For example a simple CLI for a function can be made with:

```python
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
```

Which produces a help message like:

```console
usage: hello [-h] name

Say hello!

positional arguments:
  name        Who is being greeted.

optional arguments:
  -h, --help  show this help message and exit
```

For more information, check out the [documentation](https://d-c-gray.github.io/npdoc-cli/).