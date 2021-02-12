import os
import sys

cd = os.path.abspath('.')
if cd not in sys.path:
    # Add the current directory to sys.path so that `python -m`
    # is not required to run the helper script
    sys.path.insert(0, cd)

SETTINGS = os.environ.get(
    "CYPRESS_SETTINGS",
    default=f"{os.path.split(cd)[-1]}.settings.cypress",
)
# Set environment variable so the correct settings are used when loading test data
# Note: Must set this before importing the settings, otherwise
# the wrong settings will be imported
os.environ["DJANGO_SETTINGS_MODULE"] = SETTINGS

from django.conf import settings

DEFAULT_SETUP_TEST_DATA_MODULE = "cypress.db.setup_test_data"
DEFAULT_CACHE_KEY = "cypress_last_func"
DEFAULT_CACHE_TIMEOUT = 60 * 60 * 24

SETUP_TEST_DATA_MODULE = getattr(settings, "CYPRESS_SETUP_TEST_DATA_MODULE", DEFAULT_SETUP_TEST_DATA_MODULE)
CACHE_KEY = getattr(settings, "CYPRESS_CACHE_KEY", DEFAULT_CACHE_KEY)
CACHE_TIMEOUT = getattr(settings, "CYPRESS_CACHE_TIMEOUT", DEFAULT_CACHE_TIMEOUT)
