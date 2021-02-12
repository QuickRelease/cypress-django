"""
Issue commands to operate on the project's Cypress test database.

Expects `CYPRESS_SETTINGS` (default: `settings/cypress.py`) to exist for the Django
settings.
Expects `CYPRESS_SETUP_TEST_DATA_MODULE` (default: `cypress/db/setup_test_data.py`)
to exist to house the functions for loading in test data.

This script can be used in Cypress tests to load data into the test database,
as well as be run on the command line as a shortcut for various operations on the
test database.

It caches the last loaded test data function and exits early if the same function
is loaded again - for tests that do not alter the database, it is not necessary to
reload the data, so we can save time here.

Implemented as a standalone script rather than a management command to avoid the
overhead of `manage.py` when exiting early, since we want tests to be as fast as
possible.
"""
import argparse
from importlib import import_module
from subprocess import run

import django
from django.core.cache import cache

from .settings import CACHE_KEY, CACHE_TIMEOUT, SETUP_TEST_DATA_MODULE, SETTINGS


def main():
    parser = argparse.ArgumentParser(description="Cypress test DB operations")

    parser.add_argument(
        "func",
        nargs="?",
        type=str,
        help="Setup test data function to run",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        default=False,
        help="Initialise the database (run `migrate` and `createcachetable`)",
    )
    parser.add_argument(
        "--flush",
        action="store_true",
        default=False,
        help="Clear all data (run `flush`)",
    )
    parser.add_argument(
        "--clearcache",
        action="store_true",
        default=False,
        help="Delete the test data cache (use when a test will modify the database)",
    )

    args = parser.parse_args()

    if args.init:
        run(f"python manage.py migrate --settings={SETTINGS}", shell=True)
        run(f"python manage.py createcachetable --settings={SETTINGS}", shell=True)
    if args.func:
        # Exit early if we don't need to load test data
        if cache.get(CACHE_KEY) == args.func:
            if args.clearcache:
                cache.delete(CACHE_KEY)
            return
    if args.flush:
        run(f"python manage.py flush --no-input --settings={SETTINGS}", shell=True)
    if args.func:
        # Setup Django so that apps are registered and settings configured
        # Note: we do this here to avoid the overhead when it is not necessary
        django.setup()
        # Load the test data module
        setup_test_data = import_module(SETUP_TEST_DATA_MODULE)
        # Look up the function and call
        getattr(setup_test_data, args.func)()
        # Remember this function was the last called
        cache.set(CACHE_KEY, args.func, CACHE_TIMEOUT)
    if args.clearcache:
        cache.delete(CACHE_KEY)
