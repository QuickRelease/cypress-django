from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cypress-db-helper',
    version='0.0.1',
    author='David Vaughan',
    author_email='david.vaughan@quickrelease.co.uk',
    description='Cypress DB Helper command line script',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/QuickRelease/cypress-db-helper.git',
    packages=find_packages(),
    scripts=['bin/cypress_db_helper.py'],
)
