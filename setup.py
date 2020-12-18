from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cypress-django',
    version='0.0.3',
    author='David Vaughan',
    author_email='david.vaughan@quickrelease.co.uk',
    description='Cypress DB helper command line script',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/QuickRelease/cypress-django.git',
    packages=find_packages(),
    install_requires=['Django>=2.2.13'],
)
