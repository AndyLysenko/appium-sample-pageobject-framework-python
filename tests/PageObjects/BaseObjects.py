# -*- coding: utf-8 -*-"
"""Module to store application base page elements"""
import unittest
from time import strftime
import datetime
from ..GlobalConstants import DEFAULT_WAIT_FOR_ELEMENT, DEFAULT_LOCAL_RESULTS_FOLDER
from ..Helpers import log, replace_text


class BasePageObject(unittest.TestCase):
    """Class represents object of application page.

    Should be used as a base class for any single page of application.
    Normally is a container for UI elements(BasePageElement),
    that's why class can be used not only for the whole page, but to represent any set of UI element as well.
    For example: context menus, alerts, panes of controls, etc.
    """

    def __init__(self):
        pass


class BasePageElement(unittest.TestCase):
    """Class represents base UI element.

    Should be used as a base class for each single element on a page: link, button, picture, slider, textbox, etc.
    Contains attributes representing element's features and methods corresponding to possible actions.

    Attributes:
        - element (WebElement): Appium(Selenium) web element itself. All actions are applied to it.
        - is_present (bool): Indicates if an element is present on current page.
        - screen_width (int): Measured actual screen widths of device.
        - screen_height (int): Measured actual screen height of device.
        - scroll_top_coordinate (int): Calculated top coordinate on page to swipe from/to.
        - scroll_bottom_coordinate (int): Calculated top coordinate on page to swipe from/to.
        - scroll_x_coordinate (int): Calculated value for "width" coordinate on page to swipe along.
    """

    def __get__(self, obj, cls=None):
        pass

    def __delete__(self, obj):
        pass

    def __init__(self, driver, strategy="ios uiautomation", locator="", time_to_wait=DEFAULT_WAIT_FOR_ELEMENT,
                 screenshot_location=DEFAULT_LOCAL_RESULTS_FOLDER, element_name="", index=0,
                 count_similar_elements=False, pages_to_search=1, search_direction='down', fail_if_not_found=True):
        """Creates element class object.

        :Args:
            - driver (WebDriver): Web driver object.
            - strategy (str): location strategy used to find element on the screen.
                Allowed values: "xpath", "class_name", "ios uiautomation". Default: "ios uiautomation".
            - locator (str): String used with strategy to find element on a screen.
            - time_to_wait (int): Max time in seconds to look for element on a screen.
            - screenshot_location (str): Folder to save screenshots to in case of failed search.
            - element_name (str): Name of the element. Just an informational attribute.
            - index (int): In case of multiple elements found on the screen, index in the elements array.
            - count_similar_elements (bool): If true, number of similar elements will be counted.
                Works only if index != 0. Default: False.
            - pages_to_search (int): In element is not found on the screen, page will be scrolled this number of times.
                1 is default.
            - search_direction (str): In element is not found on the screen, page will be scrolled in this direction.
                Allowed values: "up', "down". Default: "down".
            - fail_if_not_found (bool): If true and element not found test fails, otherwise returns None.

        :Usage:
            BasePageElement(driver=self.driver,
                            strategy='ios uiautomation',
                            locator="target.frontMostApp().mainWindow().buttons()[\"More\"]",
                            element_name="MoreElement",
                            index=1,
                            count_similar_elements=True,
                            time_to_wait= 15,
                            pages_to_search= 3,
                            search_direction='down',
                            fail_if_not_found= True,
                            screenshot_location='/Users/User1/Dev/Screenshots')
        """
        self.driver = driver
        self.strategy = strategy
        self.locator = locator
        self.time_to_wait = time_to_wait
        self.screenshot_location = screenshot_location
        self.element_name = element_name
        self.index = index
        self.count_similar_elements = count_similar_elements
        self.pages_to_search = pages_to_search
        self.search_direction = search_direction
        self.fail_if_not_found = fail_if_not_found

        if pages_to_search != 1:
            self.screen_width = self.driver.get_window_size().__getitem__('width')
            self.screen_height = self.driver.get_window_size().__getitem__('height')
            self.scroll_top_coordinate = round(0.3 * self.screen_height, 0)
            self.scroll_bottom_coordinate = round(0.8 * self.screen_height, 0)
            self.scroll_x_coordinate = round(0.5 * self.screen_width, 0)

        self.is_present = False

        self.element = self.find_element()

    def find_element(self):
        """Finds element by attributes specified in __init__ method.

        Method uses strategy and locator values to find element on a screen. Timeout specified by time_to_wait value.
        If search fails, screenshot is saved in screenshot_location. If pages_to_search > 1 and element is not found on
        the screen page will be swiped pages_to_search times up or down depending on search_direction value.
        If multiple elements with specified values are found, they all are presented as an array and element with
        specified index will be returned.

        :Returns:
            WebElement: If it is has been found on the screen.
            None: If element not found and fail_if_not_found is False
            Assert: If element not found and fail_if_not_found is True
        """
        log("Trying to find element \"" + self.element_name + "\"...")

        # set time limit to look for element
        self.driver.implicitly_wait(self.time_to_wait)

        # allowed locator strategies
        location_strategies = ["xpath", "class_name", "ios uiautomation"]

        # check if strategy is relevant
        if self.strategy not in location_strategies:
            log("Failed to find element \"" + self.element_name + "\". Wrong location strategy \"" + self.strategy +
                "\". Supported strategies: \"xpath\", \"class_name\".")
            self.fail("Wrong location strategy. Supported strategies: \"xpath\", \"class_name\", \"ios uiautomation\".")

        # save the time when search for element started
        self.time = datetime.datetime.now()

        # finding element
        # counter of scrolled pages
        i = 1
        while i <= self.pages_to_search:
            try:
                if self.strategy == "ios uiautomation":
                    elements_array = self.driver.find_elements_by_ios_uiautomation(self.locator)
                    if self.count_similar_elements:
                        log("Number of element with same locator= " + str(len(elements_array)) + ".")
                    element = elements_array[self.index]
                elif self.strategy == "xpath":
                    elements_array = self.driver.find_elements_by_xpath(self.locator)
                    if self.count_similar_elements:
                        log("Number of element with same locator= " + str(len(elements_array)) + ".")
                    element = elements_array[self.index]
                elif self.strategy == "class_name":
                    elements_array = self.driver.find_elements_by_class_name(self.locator)
                    if self.count_similar_elements:
                        log("Number of element with same locator= " + str(len(elements_array)) + ".")
                    element = elements_array[self.index]
                else:
                    element = None
                log("Element \"" + self.element_name + "\" found on page " + str(i) + ".")
                self.driver.implicitly_wait(DEFAULT_WAIT_FOR_ELEMENT)

                # print the time taken to find element
                log("Time taken to find element= " + str(datetime.datetime.now() - self.time))

                self.is_present = True

                return element
            except:
                # saving screenshot and logging error for scrolled page
                screenshot_file = "/Find_fail_" + \
                                  replace_text(replace_text(self.element_name, old="'", new=""), old="\"", new="") + \
                                  "_page_" + str(i) + strftime("_%H-%M-%S") + ".png"
                screenshot_file_full = self.screenshot_location + screenshot_file
                log("Saving screenshot " + screenshot_file_full)

                # if not found exception is caught and test is not failed
                if not self.fail_if_not_found:
                    self.driver.save_screenshot(screenshot_file_full)

                # saving final screenshot and logging error
                log("Failed to find element \"" +
                    replace_text(replace_text(self.element_name, old="'", new=""), old="\"", new="") + "\" on page " +
                    str(i) + ": location strategy= \"" + self.strategy + "\"; locator= \"" + self.locator +
                    "\"; index= \"" + str(self.index) + "\"; time to wait= \"" + str(self.time_to_wait) +
                    "\"; screenshot file= \"" + screenshot_file + "\"")

            # if not last page, swipe the scree
            if i != self.pages_to_search:
                if self.search_direction == 'down':
                    log("Swiping down...")
                    try:
                        self.driver.execute_script("mobile: scroll", {"direction": "down"})
                        log("Successfully swiped down.")
                    except:
                        log("Failed to swipe.")
                elif self.search_direction == 'up':
                    log("Swiping up...")
                    try:
                        self.driver.execute_script("mobile: scroll", {"direction": "up"})
                        log("Successfully swiped up.")
                    except:
                        log("Failed to swipe.")
                else:
                    self.fail("Unrecognized swipe direction. Test failed.")

            i += 1

        # after the search set back location delay value
        self.driver.implicitly_wait(DEFAULT_WAIT_FOR_ELEMENT)

        # fail test if required
        if self.fail_if_not_found:
            self.fail("Test failed! Element \"" + self.element_name + "\" not found on the screen.")
        else:
            log("Element \"" + self.element_name + "\" not found on the screen.")
            # if not, return None object
            return None

    def select(self):
        """Tap on element."""
        log("Trying to tap element \"" + self.element_name + "\"...")

        try:
            self.element.click()
            log("Element \"" + self.element_name + "\" tapped.")
        except:
            # log("Failed to tap element \"" + self.element_name + "\".")
            self.fail("Failed to tap element \"" + self.element_name + "\".")

    def input_text(self, text, clean=True):
        """Type text into element.

        :Args:
            - text (str): Text to type.
            - clean (bool): If True, element is cleaned before typing.

        :Usage:
            element.input_text('Hello World!!!', clean=False)
        """
        self.text = text
        log("Typing " + self.text + " into \"" + self.element_name + "\" textbox...")
        if clean:
            try:
                self.element.clear()
                log("Element cleared")
            except:
                log("Failed to clear element")
        try:
            self.element.send_keys(text)
            log(text + " was successfully typed.")
        except:
            log("Failed to send \"" + text + "\" keys")

    def input_text_one_by_one(self, text, clean=True):
        """Type text into element one by one.

        Sometimes it's necessary to input one by one

        :Args:
            - text (str): Text to type.
            - clean (bool): If True, element is cleaned before typing.

        :Usage:
            element.input_text('Hello World!!!', clean=False)
        """
        self.text = text
        log("Typing " + self.text + " into \"" + self.element_name + "\" textbox one by one...")
        if clean:
            try:
                self.element.clear()
                log("Element cleared")
            except:
                log("Failed to clear element")
        try:
            for character in text:
                self.element.send_keys(character)
            log(text + " was successfully typed.")
        except:
            log("Failed to send \"" + text + "\" keys")

    def get_text(self):
        """Get text value of the element

        :Returns:
            str: Element text. If nothing is typed, "" will be returned.

        :Usage:
            element.get_text()
        """
        return self.element.text

    def is_displayed(self, fail_test_if_not=False):
        """Checks if element is currently displayed on the screen.

        :Args:
            - fail_test_if_not (bool): To fail a test or not in case element is not displayed.

        :Returns:
            bool: Current value. True if displayed, False otherwise.
            Assert: If fail_test_if_not if False and element is not displayed.

        :Usage:
            element.is_displayed(fail_test_if_not=True)
        """
        log("Checking if element is displayed on the screen...")
        self.time = datetime.datetime.now()
        is_displayed = self.element.is_displayed()
        log("Time taken to check= " + str(datetime.datetime.now() - self.time))

        if fail_test_if_not and not is_displayed:
            self.fail("Test failed! Element " + self.element_name + " is not displayed!")
        else:
            log("Element displayed=" + str(is_displayed))
            return is_displayed

    def is_enabled(self, fail_test_if_not=False):
        """Checks if element is currently present on the screen.

        Element might be not visible, but present.

        :Args:
            - fail_test_if_not (bool): To fail a test or not in case element is not present.

        :Returns:
            bool: Current value. True if present, False otherwise.
            Assert: If fail_test_if_not if False and element is not present.

        :Usage:
            element.is_enabled()
        """
        log("Checking if element is present somewhere on the screen...")
        self.time = datetime.datetime.now()
        is_enabled = self.element.is_enabled()
        log("Time taken to check= " + str(datetime.datetime.now() - self.time))

        if fail_test_if_not and not is_enabled:
            self.fail("Test failed! Element " + self.element_name + " is not displayed!")
        else:
            log("Element displayed=" + str(is_enabled))
            return is_enabled

