
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "auto_examples\plot_e01_program.py"
.. LINE NUMBERS ARE GIVEN BELOW.

.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        :ref:`Go to the end <sphx_glr_download_auto_examples_plot_e01_program.py>`
        to download the full example code.

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_e01_program.py:


Creating a Program
==================

This is a basic example for generating a simple program
with npdoc_cli.

The attribute ``cli`` is a pre-made instance of 
:py:obj:`npdoc_cli.NumpyDocCLI` for easy access across different
modules. It is the access point for the  module.

.. GENERATED FROM PYTHON SOURCE LINES 12-15

.. code-block:: Python


    from npdoc_cli import cli








.. GENERATED FROM PYTHON SOURCE LINES 16-23

Build the CLI
-------------
First, define an entry point into the program by wrapping
a method in ``cli.program()`` and document your function with 
type hinting and numpy style doc strings. When ``cli.build()``
is called, the function's type hinting and doc strings will be
parsed and converted into a command line interface.

.. GENERATED FROM PYTHON SOURCE LINES 23-39

.. code-block:: Python


    @cli.program
    def hello(name: str):
        """
        Say hello!

        Parameters
        ----------
        name : str
            Who is being greeted.
        """
        print('hello',name)

    cli.build()
    cli.print_help()





.. rst-class:: sphx-glr-script-out

 .. code-block:: none

    usage: hello [-h] name

    Say hello!

    positional arguments:
      name        Who is being greeted.

    options:
      -h, --help  show this help message and exit




.. GENERATED FROM PYTHON SOURCE LINES 40-50

Dispatching to Functions
------------------------
Calling ``cli.parse_args()`` will parse any command line arguments
into an |argparse namespace|_. Passing that through
``cli.dispatch()`` will route the arguments to the correct function.

Normally, we would call ``cli.parse_args()`` as empty to get the
arguments from the command line that invoked the program. For this
example, we pass our own arguments as a list. Calling ``cli.dispatch(args)`` will pass the
arguments from the command line to the correct function.

.. GENERATED FROM PYTHON SOURCE LINES 50-54

.. code-block:: Python


    args = cli.parse_args(['reader'])
    cli.dispatch(args)





.. rst-class:: sphx-glr-script-out

 .. code-block:: none

    hello reader




.. GENERATED FROM PYTHON SOURCE LINES 55-57

The function is stored in the attribute ``args.__routine__``, and can be
accessed and called manually if desired.

.. GENERATED FROM PYTHON SOURCE LINES 57-67

.. code-block:: Python


    args = cli.parse_args(['reader'])
    print(args.__routine__)
    args = vars(args)
    func = args.pop('__routine__')
    func(**args)








.. rst-class:: sphx-glr-script-out

 .. code-block:: none

    <function hello at 0x0000027DD5F9E5C0>
    hello reader





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** (0 minutes 0.009 seconds)


.. _sphx_glr_download_auto_examples_plot_e01_program.py:

.. only:: html

  .. container:: sphx-glr-footer sphx-glr-footer-example

    .. container:: sphx-glr-download sphx-glr-download-jupyter

      :download:`Download Jupyter notebook: plot_e01_program.ipynb <plot_e01_program.ipynb>`

    .. container:: sphx-glr-download sphx-glr-download-python

      :download:`Download Python source code: plot_e01_program.py <plot_e01_program.py>`

    .. container:: sphx-glr-download sphx-glr-download-zip

      :download:`Download zipped: plot_e01_program.zip <plot_e01_program.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
