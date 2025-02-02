from setuptools import setup,find_packages

setup(name='npdoc-cli',
      version='1.0',
      description='Tool for creating command line interfaces derviced from numpy doc strings.',
      author='Cole Gray',
      author_email='cole.gray.writing@gmail.com',
      packages=find_packages('src'),
      package_dir = {'':'src'}
     )