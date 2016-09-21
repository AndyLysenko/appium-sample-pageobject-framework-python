# -*- coding: utf-8 -*-"
from ..BaseObjects import BasePageElement, BasePageObject
from ...Locators import locators
from ...Helpers import log


class AuthorsPageObject(BasePageObject):
    """Page object represents Books page of the app"""
    def __init__(self, driver):
        log("Opening Authors page...")
        self.driver = driver
        self.title = AuthorsTitleElement(driver=self.driver,
                                         locator=locators["authors_page.authors_title"],
                                         strategy='ios uiautomation',
                                         element_name="AuthorsTitleElement")
        log("Authors page opened.")


class AuthorsTitleElement(BasePageElement):
    pass
