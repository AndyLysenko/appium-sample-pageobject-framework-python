# -*- coding: utf-8 -*-"
import unittest
from time import sleep
from appium import webdriver
import GlobalConstants
from Helpers import log, detect_device_type, verify_app_launched, set_device_orientation
from PageObjects.Books import BooksPageObject
from Locators import set_tablet


class OurTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method is called once before all tests execution"""
        desired_caps={}

        desired_caps['app'] = GlobalConstants.HOST_APP_LOCATION
        desired_caps['bundleId'] = GlobalConstants.BUNDLE_ID
        # desired_caps['udid'] = '3089538653865389653485634856349346348563'   #iPhone - sample
        desired_caps['udid'] = '3874653487563409857349057349053745092375903'  # iPad - sample
        desired_caps['platformVersion'] = '9.3.3'
        desired_caps['platformName'] = 'iOS'
        desired_caps['deviceName'] = "My iPhone"
        desired_caps['nativeInstrumentsLib'] = 'true'

        # desired_caps['fullReset'] = 'true'
        # desired_caps['noReset'] = 'true'
        # desired_caps['newCommandTimeout'] = '100'
        # desired_caps['launchTimeout'] = 3000
        # experimental caps
        # desired_caps['autoAcceptAlerts'] = 'true'

        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def setUp(self):
        """Method is called before each test execution"""

        # restart app
        log("Trying to close the app...")
        try:
            self.driver.close_app()
            log("App is closed!")
        except:
            log("Cant close the app!")
        sleep(3)
        log("Trying to launch the app...")
        try:
            self.driver.launch_app()
            log("App is launched!")
        except:
            log("Cant launch the app!")


        log("This is before_each setup")

        # verify the app is started correctly
        self.assertTrue(verify_app_launched(self.driver), "Application didn't start successfully! Test failed!")

        self.screenshot_folder = GlobalConstants.DEFAULT_LOCAL_RESULTS_FOLDER

        self.driver.implicitly_wait(GlobalConstants.DEFAULT_WAIT_FOR_ELEMENT)

        self.device_type = detect_device_type(self.driver)
        if self.device_type == "Tablet":
            set_tablet()

        log("Test setup finished.")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            try:
                cls.driver.quit()
                log("Driver session closed.")
            except:
                pass

# -------------------------- ready tests ----------------------------------
    def test_1_is_installed(self):
        log("Test \"" + self._testMethodName + "\" started.")

        # Checks that default page Books is open and it's elements are found
        books_page = BooksPageObject(self.driver)

        books_page.open_books_more_menu()
        books_page.close_books_more_menu()

        self.driver.save_screenshot(self.screenshot_folder + "/test1.png")

        log("Test \"" + self._testMethodName + "\" passed.")

    def test_2_navigation(self):
        log("Test \"" + self._testMethodName + "\" started.")

        # initiate main objects: books page and bottom navigation menu
        books_page = BooksPageObject(self.driver)
        bottom_menu = BottomMenuPanePageObject(self.driver, device_type=self.device_type)

        sleep(1)
        self.driver.save_screenshot(self.screenshot_folder + "/Navigation_Books.png")

        # books page
        books_page.open_recent_read()
        books_page.open_favorites()
        books_page.open_all_books()
        books_page.open_books_more_menu()
        books_page.close_books_more_menu()

        # authors page
        authors_page = bottom_menu.open_authors_page()
        sleep(1)
        self.driver.save_screenshot(self.screenshot_folder + "/Navigation_Authors.png")

        log("Test \"" + self._testMethodName + "\" passed.")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(OurTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
