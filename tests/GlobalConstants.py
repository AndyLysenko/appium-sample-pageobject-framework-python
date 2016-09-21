import os

DEFAULT_WAIT_FOR_ELEMENT = 10
DEFAULT_WAIT_FOR_ELEMENT_SCROLL = 5
DEFAULT_SCROLL_PAGES = 6
DEFAULT_SCROLL_DELAY = 1000
ALLOWED_IMAGE_DIFFERENCE_PERCENT = 3.0

TEST_ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../tests_local/"
HOST_APP_LOCATION = TEST_ROOT_DIR + '/../application/SampleApp.ipa'
TEST_RESULTS_HOME_FOLDER = TEST_ROOT_DIR + 'Results/'
DEFAULT_LOCAL_RESULTS_FOLDER = (os.getenv('SCREENSHOT_PATH', '') or (TEST_ROOT_DIR + "screenshots/")) + '/'
REF_SCREENSHOTS_ROOT_FOLDER = TEST_ROOT_DIR + "reference_screenshots/"
DEFAULT_IMAGE_DIFFERENCE_FILE = REF_SCREENSHOTS_ROOT_FOLDER + "temp/difference.png"
BUNDLE_ID = 'com.sample.app'    # your app bundle id

# TEMP_DIR = os.environ['TMPDIR']

# Additional data
