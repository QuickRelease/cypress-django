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
import sys

from django.core.cache import cache

SETTINGS = f"{os.path.split(os.path.abspath('.'))[-1]}.settings.cypress"


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
            f"--indent=4 --settings={SETTINGS}",
            shell=True,
        )
        return
    if args.reset:
        cypress = import_module(SETTINGS)
        try:
            os.remove(cypress.DATABASES["default"]["NAME"])
        except FileNotFoundError:
            # Nothing to remove
            pass
        except PermissionError as e:
            # If the server is still running (or any other processes are accessing the file)
            # it will be locked
            print(
                f"{e}\nRemember to shut down any processes accessing the database file "
                "(e.g. the server or any running python shells)",
                file=sys.stderr,
            )
            return
    if args.init:
        run(
            f"python manage.py migrate --settings={SETTINGS}",
            shell=True,
        )
        run(
            f"python manage.py createcachetable --settings={SETTINGS}",
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
            f"python manage.py flush --no-input --settings={SETTINGS}",
            shell=True,
        )
    if args.data:
        # TODO: more visibility when a fixture can't be loaded
        run(
            [
                "python",
                "manage.py",
                "loaddata",
                args.data,
                f"--settings={SETTINGS}",
            ],
            shell=True,
        )
        cache.set("cypress_last_loaded_fixture", args.data, 60 * 60 * 24)
    if args.clearcache:
        cache.delete("cypress_last_loaded_fixture")


if __name__ == "__main__":
    main()
