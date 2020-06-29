"""
Issue commands to operate on the project's Cypress test database.

Expects `settings/cypress.py` to exist.

This script can be used in Cypress tests to load fixtures into the test database,
as well as be run on the command line as a shortcut for various operations on the
test database.

It caches the last loaded fixture (by filepath) and exits early if the same fixture
is loaded again - for tests that do not alter the database, it is not necessary to
reload the data, so we can save time here.

Implemented as a standalone script rather than a management command to avoid the
overhead of `manage.py` when exiting early, since we want tests to be as fast as
possible.

"""

import argparse
from importlib import import_module
import os
from subprocess import run

from django.core.cache import cache

# TODO: needs to become an environment variable?
#  - and if not set, produce an error
PROJECT_NAME = os.path.split(os.path.abspath("."))[-1]


def main():
    parser = argparse.ArgumentParser(description="Cypress test DB operations")

    parser.add_argument(
        "data",
        nargs="?",
        type=str,
        help="The filepath of a fixture to load (run `loaddata`)",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        default=False,
        help="Initialise the database (run `migrate` and `createcachetable`)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        default=False,
        help="Delete the database (will not work if processes have a file lock)",
    )
    parser.add_argument(
        "--flush",
        action="store_true",
        default=False,
        help="Clear all data (run `flush`)",
    )
    parser.add_argument(
        "--dumpdata",
        action="store_true",
        default=False,
        help=(
            "Produce a JSON fixture to stdout containing the data currently "
            "in the test database (run `dumpdata` with various flags set)"
        ),
    )
    parser.add_argument(
        "--clearcache",
        action="store_true",
        default=False,
        help="Delete the fixture cache (use when a test will modify the database)",
    )

    args = parser.parse_args()

    if args.dumpdata:
        run(
            "python manage.py dumpdata --natural-primary --natural-foreign "
            "-e contenttypes -e admin.logentry -e sessions.session -e auth.Permission "
            f"--indent=4 --settings={PROJECT_NAME}.settings.cypress",
            shell=True,
        )
        return
    # TODO: remove this option?
    if args.reset:
        cypress = import_module(f"{PROJECT_NAME}.settings.cypress")
        try:
            os.remove(cypress.DATABASES["default"]["NAME"])
        except FileNotFoundError:
            # Nothing to remove
            pass
        except PermissionError:
            # If the server is still running (or any other processes are accessing the file)
            # it will be locked
            raise
    if args.init:
        run(
            f"python manage.py migrate --settings={PROJECT_NAME}.settings.cypress",
            shell=True,
        )
        run(
            f"python manage.py createcachetable --settings={PROJECT_NAME}.settings.cypress",
            shell=True,
        )
    if args.data:
        last_fixture = cache.get("cypress_last_loaded_fixture")
        if last_fixture == args.data:
            if args.clearcache:
                cache.delete("cypress_last_loaded_fixture")
            return
    if args.flush:
        run(
            f"python manage.py flush --no-input --settings={PROJECT_NAME}.settings.cypress",
            shell=True,
        )
    if args.data:
        run(
            [
                "python",
                "manage.py",
                "loaddata",
                args.data,
                f"--settings={PROJECT_NAME}.settings.cypress",
            ],
            shell=True,
        )
        cache.set("cypress_last_loaded_fixture", args.data, 60 * 60 * 24)
    if args.clearcache:
        cache.delete("cypress_last_loaded_fixture")


if __name__ == "__main__":
    main()
