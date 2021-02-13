from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cypress-django',
    version='0.1.0',
    author='David Vaughan',
    author_email='david.vaughan@quickrelease.co.uk',
    maintainer="Quick Release (Automotive) Ltd.",
    description='Cypress DB helper command line script',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/QuickRelease/cypress-django.git',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords="cypress django test",
    packages=find_packages(),
    install_requires=['Django>=1.11'],
    license="MIT",
    entry_points={
        'console_scripts': [
            'cypress_db = cypress_db.cmd:main',
        ]
    }
)
