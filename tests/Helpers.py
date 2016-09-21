# -*- coding: utf-8 -*-"
"""Module contains different functions created to simplify UI automation of iOS applications with Appium"""
import exceptions
import subprocess
import time
from GlobalConstants import DEFAULT_SCROLL_DELAY


def convert_text_to_xpath(text):
    """Converts a string to xpath locator.

     Returns a locator ready to be used as an argument in find_elements_by_xpath method (by exact text).

    :Usage:
        convert_text_to_xpath('OK')

    :Examples:
        # >>> convert_text_to_xpath("OK")
        # "//*[@text='OK']"
    """
    return "//*[@text='" + text + "']"


def scroll_up(driver, number_of_pages=1):
    """Swipe page up specified number of times.

    iOS only function.

    :Args:
        - driver (WebDriver): Web driver object
        - number_of_pages (int): How many pages to swipe, default 1.

    :Usage:
        scroll_up(self.driver, 3)
    """
    log("Scrolling up " + str(number_of_pages) + " pages.")

    i = 1
    while i <= number_of_pages:
        log("Swiping up page " + str(i) + "...")
        try:
            driver.execute_script("mobile: scroll", {"direction": "up"})
            log("Successfully swiped up page " + str(i) + ".")
        except:
            log("Failed to swipe up page " + str(i) + ".")
        i += 1


def scroll_down(driver, number_of_pages=1):
    """Swipe page down specified number of times.

    iOS only function.

    :Args:
        - driver (WebDriver): Web driver object
        - number_of_pages (int): How many pages to swipe, default 1.

    :Usage:
        scroll_up(self.driver, 3)
    """
    log("Scrolling down " + str(number_of_pages) + " pages.")

    i = 1
    while i <= number_of_pages:
        log("Swiping down page " + str(i) + "...")
        try:
            driver.execute_script("mobile: scroll", {"direction": "down"})
            log("Successfully swiped down page " + str(i) + ".")
        except:
            log("Failed to swipe down page " + str(i) + ".")
        i += 1


def detect_device_type(driver):
    """Detects if iOS device is tablet of mobile.

    iOS only function. Screen size and device orientation are used to determine device type.

    :Args:
        - driver (WebDriver): Web driver object

    :Returns:
        str: 'Tablet' or 'Phone'

    :Usage:
        detect_device_type(self.driver)
    """
    # TODO rename to Tablet and Mobile

    screen_sixe = driver.get_window_size()
    orientation = driver.orientation
    log("Device orientation= %s" % orientation)
    log("Screen size= %s" % screen_sixe)
    device_type = "Phone"
    if orientation == "PORTRAIT":
        if screen_sixe.__getitem__('width') >= 768:
            device_type = "Tablet"
    else:
        if screen_sixe.__getitem__('height') >= 768:
            device_type = "Tablet"
    log("Detected device type= %s" %device_type)

    return device_type


def set_device_orientation(driver, orientation):
    """Sets device orientation.

    Allowed values are 'PORTRAIT' and 'LANDSCAPE'.

    :Args:
        - driver (WebDriver): Web driver object
        - orientation (str): 'PORTRAIT' or 'LANDSCAPE'.

    :Usage:
        - set_device_orientation(self.driver, 'LANDSCAPE')
    """
    driver.orientation = orientation


def replace_text(string="", old="", new=""):
    """Replaces text within string.

    :Args:
        string (str): Input string
        old (str): Text fragment to be replaced
        new (str): New text fragment to replace with

    :Returns:
        str: New string with replaced text.

    :Usage:
        replace_text("target.frontMostApp().mainWindow().buttons()[\"button_name\"]", "button_name", "Create New")

    :Examples:
        # >>> replace_text("target.frontMostApp().mainWindow().buttons()[\"button_name\"]", "button_name", "Create New")
        # 'target.frontMostApp().mainWindow().buttons()["Create New"]'
    """
    return string.replace(old, new)


def verify_app_launched(driver):
    """Checks if the app launched successfully.

    Current application specific function. Checks if specific element, showing "In progress" status,
    is present on the screen.

    :Args:
        - driver (WebDriver): Web driver object

    :Usage:
        verify_app_launched(self.driver)
    """
    driver.implicitly_wait(2)
    log("Checking if app successfully started...")
    is_started = False
    time.sleep(3)

    try:
        driver.find_element_by_ios_uiautomation("target.frontMostApp().mainWindow().activityIndicators()[\"In progress\"]")
        log("\"In progress\" indicator found.")
        log("Application didn't start successfully!")
    except:
        log("App is successfully launched.")
        is_started = True

    return is_started


def hide_keyboard(driver, key_name=None):
    """Specific function to hide keyboard by tapping on key meaning 'Done.'

    iOS only function.

    :Args:
        - driver (WebDriver): Web driver object
        - key_name (str): Name of the key on keyboard meaning 'Done'.

    :Usage:
        hide_keyboard(self.driver, 'Weiter')
    """
    log("Trying to hide keyboard...")
    try:
        driver.hide_keyboard(key_name=key_name)
        log("Hide keyboard action was sent")
    except:
        log("Failed to hide keyboard")
    # self.driver.execute_script("mobile: hideKeyboard")


def make_unicode(input_text):
    """Converts a string to Unicode

    :Usage:
        make_unicode("abc")

    :Examples:
        # >>> make_unicode("abc")
        # u'abc'
        # >>> make_unicode("абв")
        # u'\u0430\u0431\u0432'
    """
    if type(input_text) != unicode:
        if type(input_text) != str:
            input_text = str(input_text)
        input_text = input_text.decode('utf-8')
        return input_text
    else:
        return input_text


def log(msg):
    """Logs a message with current time

    :Usage:
        log("Test started.")

    :Examples:
        # >>> log("Test started.")
        # 20:02:02: Test started.
    """
    print (time.strftime("%H:%M:%S") + ": " + make_unicode(msg))


def navigate_back(driver):
    """Navigate an app back.

     Android only function

    :Usage:
        navigate_back(self.driver)
    """
    try:
        driver.back()
        print "Back button clicked."
    except:
        print "Failed to navigate back!"


def swipe_coordinates(driver, x_start, y_start, x_end, y_end, swipe_delay=DEFAULT_SCROLL_DELAY):
    """Swipe from one point to another point, for an optional duration.

    :Args:
        - driver (WebDriver): Web driver object.
        - x_start (int): x-coordinate at which to start
        - y_start (int): y-coordinate at which to start
        - x_end (int): x-coordinate at which to stop
        - y_end (int): y-coordinate at which to stop
        - swipe_delay (int): (optional) time to take the swipe, in ms.

    :Usage:
        driver.swipe(100, 100, 100, 400)
    """
    log('Trying to swipe from (' + str(x_start) + '; ' + str(y_start) + ') to (' + str(x_end) + '; ' + str(y_end) + ')')

    try:
        driver.swipe(x_start, y_start, x_end, y_end, swipe_delay)
        log("Swiped successfully!")
    except exceptions.Exception as e:
        log("Failed to swipe")


def swipe_center_down(driver, swipe_speed=DEFAULT_SCROLL_DELAY):
    """Swipe form screen center to the top with specified speed.

    :Args:
        - driver (WebDriver): Web driver object
        - swipe_speed (int): Scroll speed, in ms.

    :Usage:
        swipe_center_down(self.driver, 1500)
    """
    # calculate scroll coordinates
    screen_width = driver.get_window_size().__getitem__('width')
    screen_height = driver.get_window_size().__getitem__('height')
    swipe_centre_coordinate_x = round(0.5 * screen_width, 0)
    swipe_centre_coordinate_y = round(0.5 * screen_height, 0)
    swipe_down_coordinate_x = round(0.5 * screen_width, 0)
    swipe_down_coordinate_y = round(0.8 * screen_height, 0)
    log("Swiping from %s, %s to %s %s with delay %s" % (swipe_centre_coordinate_x, swipe_centre_coordinate_y,
                                                          swipe_down_coordinate_x, swipe_down_coordinate_y, swipe_speed))
    try:
        driver.swipe(swipe_centre_coordinate_x, swipe_centre_coordinate_y, swipe_down_coordinate_x,
                     swipe_down_coordinate_y, swipe_speed)
        # driver.flick(swipe_centre_coordinate_x, swipe_centre_coordinate_y, swipe_down_coordinate_x,
        #              swipe_down_coordinate_y)
    except exceptions.Exception as e:
        log("Failed to swipe")
        log(e.message)


def navigate_to_home_page(driver):
    """Navigates to application home page.

    Current application specific function.

    :Args:
        - driver (WebDriver): Web driver object

    :Usage:
        navigate_to_home_page(self.driver)
    """
    try:
        log("Trying to navigate to Books page...")
        driver.find_element_by_ios_uiautomation("target.frontMostApp().tabBar().buttons()[\"Books\"]").click()
        log("Books page opened.")
    except:
        log("Faild to navigate to Books button!")


# # #------------------------------------------ Local functions --------------------------------------------

def print_to_file(file_path, text_data):
    """Prints text to file.

    All existing text is erased before writing.

    :Args:
        file_path (str): File path
        text_data (str): Data to print to file.

    :Usage:
        print_to_file('/Users/Andrii/Downloads/Application_autotest_requirements.txt', 'Test passe.')
    """
    with open(file_path, 'w') as f:
        f.write(text_data)


def print_unicode_to_file(file_path, text_data):
    """Prints text to file.

    Encodes input text to unicode first.
    All existing text is erased before writing.

    :Args:
        file_path (str): File path
        text_data (str): Data to print to file.

    :Usage:
        print_unicode_to_file('/Users/Andrii/Downloads/Application_autotest_requirements.txt', 'Test passe.')
    """
    with open(file_path, 'w') as f:
        f.write(text_data.encode('utf8'))


def append_file(file_path, text_data):
    """Adds text to the end of file.

    All existing text remains.


    :Args:
        file_path (str): File path
        text_data (str): Data to print to file.

    :Usage:
        append_file('/Users/Andrii/Downloads/Application_autotest_requirements.txt', 'Test passe.')
    """
    with open(file_path, 'a') as f:
        f.write(text_data)
        f.write("\n")


def read_from_file(file_path):
    """Reads text from file.

    :Args:
        file_path (str): File path

    :Returns:
        str: File content as a string.

    :Usage:
        read_from_file('/Users/Andrii/Downloads/Application_autotest_requirements.txt')

    :Examples:
        # read_from_file('/Users/Andrii/Downloads/Application_autotest_requirements.xml')
        # Test document.
    """
    with open(file_path, 'r') as f:
        return f.read()


def clean_folder(folder_name):
    """Removes all files and folders from path recursively.

    :Args:
        folder_name (str): Folder path.

    :Usage:
        clean_folder('/Users/Andrii/Downloads/')
    """
    try:
        subprocess.call("rm -Rf " + folder_name + "*", shell=True)
        log("Successfully removed all files from " + folder_name)
    except:
        log("Failed to remove files from " + folder_name)


def move_folder_content(source_folder, destination_folder):
    """Moves folder content to destination path recursively.

    :Args:
        source_folder (str): Source path.
        destination_folder (str): Destination path.

    :Usage:
        move_folder_content(''/Users/Andrii/Downloads/'', ''/Users/Andrii/Desktop/'')
    """
    try:
        subprocess.call("mv -f -v " + source_folder + "* " + destination_folder, shell=True)
        log("All files were successfully moved from " + source_folder + " to " + destination_folder + " folder")
    except:
        log("Failed to move files from " + source_folder + " to " + destination_folder + " folder")



