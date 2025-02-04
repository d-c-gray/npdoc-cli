.. npdoc-cli documentation master file, created by
   sphinx-quickstart on Sat Feb  1 18:04:04 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to npdoc-cli's documentation!
=====================================

``npdoc-cli`` is a wrapper for |argparse|_ that utilizes the |numpy style guide|_
to generate a command line interface (CLI). Paired with auto-generated
documentation with |sphinx|_, it allows the definitions of a functions source
code, source code documentation, and command line interface definition to be
tied together all in the same block of code. Maintaining the source code,
documentation, and the CLI interface all happens in the same place!

For example, a simple CLI can be made:

.. literalinclude :: ../../tests/test_snippet_intro.py
   :language: python
   :lines: 3-
   :dedent:

Which produces a help message:

.. literalinclude :: ../../tests/snippet_intro_out.txt
   :language: console

Command line arguments can be parsed and dispatched to the right function by:

.. code-block:: python

    args = cli.parse_args()
    cli.dispatch(args)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   auto_examples/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
