# cypress-django
### Cypress DB

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

#### Installation
Either install directly:

```
pip install git+https://github.com/QuickRelease/cypress-django.git
```

or add to your requirements.txt file:

```
-e git+https://github.com/QuickRelease/cypress-django.git#egg=cypress-django
```

#### Usage

```
python -m cypress_db [-h] [--init] [--reset] [--flush] [--dumpdata] [--clearcache] [data]
```

positional arguments:
```
  data          The filepath of a fixture to load (run `loaddata`)
```

optional arguments:
```
  -h, --help    show this help message and exit
  --init        Initialise the database (run `migrate` and `createcachetable`)
  --reset       Delete the database (will not work if processes have a file
                lock)
  --flush       Clear all data (run `flush`)
  --dumpdata    Produce a JSON fixture to stdout containing the data currently
                in the test database (run `dumpdata` with various flags set)
  --clearcache  Delete the fixture cache (use when a test will modify the
                database)
```

### Cypress Commands

Provides a `login` helper function:
- `cy.login()` will programmatically login using the `USERNAME` and `PASSWORD` environment
variables defined in `cypress.json` (or with `CYPRESS_` prefix if defined elsewhere)
- Recommended way to use is to put `cy.login()` in `beforeEach`
- If it is necessary to login as a different user, for example to test behaviour for users with
limited permissions, simply provide the appropriate username and password as arguments

Provides a `resetDB` helper function that expects the python package in this repo to be
installed:
- `cy.resetDB(fixture, mutable)` will flush the test database and load in a fixture
- If the test will write to the database, `mutable` should be set to `true`
- Otherwise set `mutable` to `false` to allow early exit from the script if no fixture loading
is necessary (this means repeated test runs with such tests will be significantly faster)
- The fixtures provided in the `fixture` argument should be the filename of a JSON file in
`cypress/db/fixtures/`.

#### Installation

With `npm`:
```
npm install git+https://github.com/QuickRelease/cypress-django.git --save-dev
```

and include this line in `cypress/support/index.js` or `cypress/support/commands.js`:
```
import 'cypress-django/commands'
```
