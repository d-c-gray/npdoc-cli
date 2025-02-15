from setuptools import setup,find_packages

setup(name='npdoc-cli',
      version='0.0.2',
      description='Tool for creating command line interfaces derived from numpy style doc strings.',
      author='Cole Gray',
      author_email='cole.gray14@gmail.com',
      packages=find_packages('src'),
      package_dir = {'':'src'}
     )