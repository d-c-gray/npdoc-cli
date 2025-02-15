npdoc_cli
=========

.. py:module:: npdoc_cli

.. autoapi-nested-parse::

   
   Created on Sat Feb  1 11:54:32 2025

   @author: coleg















   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   npdoc_cli.cli


Exceptions
----------

.. autoapisummary::

   npdoc_cli.CLIArgError


Classes
-------

.. autoapisummary::

   npdoc_cli.FunctionInput
   npdoc_cli.NumpyDocCommand
   npdoc_cli.NumpyDocCLI


Package Contents
----------------

.. py:exception:: CLIArgError

   Bases: :py:obj:`Exception`


   
   Error caused by invalid doc strings.
















   ..
       !! processed by numpydoc !!

.. py:class:: FunctionInput

   
   Class for organizing function inputs.
















   ..
       !! processed by numpydoc !!

   .. py:attribute:: pa
      :value: []


      
      List of positional arguments for a function input.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: kwa

      
      Dictionairy of keyword arguments for a function input.
















      ..
          !! processed by numpydoc !!


   .. py:method:: disp()


.. py:class:: NumpyDocCommand(obj: callable)

   
   Class for parsing function signatures/doc strings in argparse objects.
















   ..
       !! processed by numpydoc !!

   .. py:attribute:: obj

      
      Object called to and called during cli dispatch.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: fname

      
      Name of ``obj``.
















      ..
          !! processed by numpydoc !!


   .. py:property:: defaults
      :type: dict


      
      Dictionairy of keyword arguments and their default value
















      ..
          !! processed by numpydoc !!


   .. py:property:: types
      :type: dict


      
      Dictionairy of arguments and types.
















      ..
          !! processed by numpydoc !!


   .. py:method:: disp()

      
      Print scraped settings for debugging.
















      ..
          !! processed by numpydoc !!


   .. py:method:: scrape(replace_underscores: bool = True) -> FunctionInput

      
      Scrape doc strings and functions signature.

      Turns doc strings and function signatures into settings that can be
      passed into argparse to generate a command line interface.

      :Parameters:

          **replace_underscores** : bool, optional
              Replace underscores in argument/function names with
              dashes, stylistic choice. The default is True.



      :Returns:

          **parser_ins** : :py:obj:`FunctionInput`
              Inputs to be passed into argparse.ArgumentParser

          **arg_ins_ls** : :py:obj:`FunctionInput`
              Inputs to be passed into argparse.ArgumentParser.add_argument




      :Raises:

          CLIArgError
              If problem is found with an argument's signature or documentation.







      ..
          !! processed by numpydoc !!


.. py:class:: NumpyDocCLI

   
   Class for generating a CLI from numpy doc strings and type signatures.
















   ..
       !! processed by numpydoc !!

   .. py:attribute:: entry
      :value: None


      
      :py:obj:`NumpyDocCommand` of program entry point.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: commands
      :value: []


      
      List of :py:obj:`NumpyDocCommand` for program commands.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: subcommands

      
      Dictionairy of :py:obj:`NumpyDocCommand` for each subcommands.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: program_parser
      :value: None


      
      ArgumentParser for program entry point.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: command_parsers
      :value: []


      
      ArgumentParser for each command.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: subcommand_parsers

      
      ArgumentParser for each subcommand
















      ..
          !! processed by numpydoc !!


   .. py:method:: reset()

      
      Reset CLI to empty.





      :Returns:

          None.
              ..











      ..
          !! processed by numpydoc !!


   .. py:method:: program(function: callable) -> callable

      
      Wrapper function to define the entry point.


      :Parameters:

          **function** : callable
              That is called.



      :Returns:

          **function** : callable
              The passed function, unmodified.











      ..
          !! processed by numpydoc !!


   .. py:method:: command(obj: object) -> object

      
      Wrapper function to defined commands for entry point.


      :Parameters:

          **obj** : object
              Class definition if using subcommands, function it not.



      :Returns:

          object
              Same object passed as input, unmodified.











      ..
          !! processed by numpydoc !!


   .. py:method:: subcommand(function: callable) -> callable

      
      Wrapper function to define subcommands for a command.


      :Parameters:

          **function** : object
              Function to be called as subcommand. Should belong as submethod
              to its parent commmand's class definition.



      :Returns:

          **function** : callable
              Same function passed, unmodified.











      ..
          !! processed by numpydoc !!


   .. py:method:: tree()

      
      Print program/command/subcommand heirarchy.





      :Returns:

          None.
              ..











      ..
          !! processed by numpydoc !!


   .. py:method:: build(*command_instances: object, replace_underscores: bool = True, sort: str = 'None')

      
      Build a CLI.


      :Parameters:

          **\*instances** : object
              Instances of classes wrapped in command to use when calling
              subcommands. If an instance of a command wrapped class is not
              passed, the class itself will be used to call the subcommand.

          **replace_underscores** : bool, optional
              Repace underscores in argument/command names with dashes.
              The default is True.

          **sort** : str, {None, alphabetical}
              Sort commands and subcommands by key.



      :Returns:

          None.
              ..











      ..
          !! processed by numpydoc !!


   .. py:method:: parse_args(args: list[str] = None) -> argparse.Namespace

      
      Parse command line arguments.

      See argparse.ArgumentParser.parse_args for more info.

      :Parameters:

          **args** : list[str], optional
              List of arguments to parse. If None, parses from command line.



      :Returns:

          argparse.Namespace
              Parsed arguments.











      ..
          !! processed by numpydoc !!


   .. py:method:: print_help()

      
      Print help string for CLI





      :Returns:

          None.
              ..











      ..
          !! processed by numpydoc !!


   .. py:method:: dispatch(args: argparse.Namespace)

      
      Dispatch command line arguments to a the right function.


      :Parameters:

          **args** : _ap.Namespace
              Output of :py:meth:`NumpyDocCLI.parse_args`.



      :Returns:

          any
              Output of dispatched function.











      ..
          !! processed by numpydoc !!


.. py:data:: cli

   
   Instance of :py:obj:`NumpyDocCLI` for generating CLI's.
















   ..
       !! processed by numpydoc !!

