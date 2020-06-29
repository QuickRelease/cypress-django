# cypress-db-helper
Cypress DB Helper

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
