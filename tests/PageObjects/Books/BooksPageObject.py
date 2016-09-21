# -*- coding: utf-8 -*-"
from ..BaseObjects import BasePageElement, BasePageObject
from ...Locators import locators
from ...Helpers import log, scroll_up, replace_text
from ...GlobalConstants import DEFAULT_WAIT_FOR_ELEMENT_SCROLL
from ..OpenedBook.OpenedBookPageObject import OpenedBookPageObject


# ------------------ Books page -----------------------------------
class BooksTitleElement(BasePageElement):
    def select(self):
        super(BooksTitleElement, self).select()
        return self


class BooksFavoritesElement(BasePageElement):
    def select(self):
        super(BooksFavoritesElement, self).select()
        # return BooksFavouritesPageObject(self.driver)
        return self


class BooksRecentReadElement(BasePageElement):
    def select(self):
        super(BooksRecentReadElement, self).select()
        # return BooksRecentReadPageObject(self.driver)
        return self


class BooksAllBooksElement(BasePageElement):
    def select(self):
        super(BooksAllBooksElement, self).select()
        # return BooksAllBooksPageObject(self.driver)
        return self


class BooksSearchElement(BasePageElement):
    def select(self):
        super(BooksSearchElement, self).select()
        return
#     TODO implement search page


class BooksMoreMenuElement(BasePageElement):
    def select(self):
        super(BooksMoreMenuElement, self).select()
        return
#     TODO implement search page


class BooksPageObject(BasePageObject):
    """Page object represents Books page of the app"""
    def __init__(self, driver, device_type="Phone"):
        log("Opening Books page")
        self.driver = driver
        self.device_type = device_type

        if not hasattr(self, 'all_books'):
            log("Dont have attribute all_books. Initiating...")

            self.all_books = BooksAllBooksElement(driver=self.driver,
                                                  locator=locators["books_page.all"],
                                                  strategy='ios uiautomation',
                                                  element_name="AllBooksButton")

        log("Books page opened.")

    def open_all_books(self):
        if not hasattr(self, "all_books"):
            log("Dont have attribute 'all_books'. Initiating...")

            self.all_books = BooksAllBooksElement(driver=self.driver,
                                                  locator=locators["books_page.all"],
                                                  strategy='ios uiautomation',
                                                  element_name="AllBooksButton")
        return self.all_books.select()

    def open_favorites(self):
        if not hasattr(self, "favourites"):
            log("Dont have attribute 'favourites'. Initiating...")

            self.favourites = BooksFavoritesElement(driver=self.driver,
                                                    locator=locators["books_page.favorites"],
                                                    strategy='ios uiautomation',
                                                    element_name="FavoritesButton")
        return self.favourites.select()

    def open_recent_read(self):
        if not hasattr(self, "recent_read"):
            log("Dont have attribute 'recent_read'. Initiating...")

            self.recent_read = BooksRecentReadElement(driver=self.driver,
                                                      locator=locators["books_page.recent"],
                                                      strategy='ios uiautomation',
                                                      element_name="RecentReadButton")
        return self.recent_read.select()

    def open_search(self):
        self.search_icon = BooksSearchElement(driver=self.driver,
                                              locator=locators["books_page.search_button"],
                                              strategy='ios uiautomation',
                                              element_name="BooksSearchIcon")
        return self.search_icon.select()

    def open_books_more_menu(self):
        if self.device_type == "Phone":
            if not hasattr(self, "more_menu_icon"):
                log("Dont have attribute 'more_menu_icon'. Initiating...")

                self.more_menu_icon = BooksMoreMenuElement(driver=self.driver,
                                                           locator=locators["books_page.more_menu_button"],
                                                           strategy='ios uiautomation',
                                                           element_name="BooksMoreMenuIcon")
            return self.more_menu_icon.select()

    def close_books_more_menu(self):
        self.open_books_more_menu()

    def is_book_present_on_list_by_name(self, book_name, pages_to_search=1, time_to_wait=5):

        # build locator
        self.title_locator = replace_text(string=locators["books_page.book_locator_by_name"], old="book_name", new=book_name)

        return BasePageElement(driver=self.driver,
                               locator=self.title_locator,
                               strategy='ios uiautomation',
                               element_name=book_name,
                               pages_to_search=pages_to_search,
                               fail_if_not_found=False,
                               time_to_wait=time_to_wait).is_present

    def is_book_present_on_list_by_format(self, book_format, pages_to_search=1, time_to_wait=5):

        # build locator
        self.format_locator = "target.frontMostApp().mainWindow().collectionViews()[0].cells().firstWithPredicate(\"ANY staticTexts.name LIKE '" + book_format + "'\").staticTexts().firstWithPredicate(\"value like '" + book_format + "'\")"

        return BasePageElement(driver=self.driver,
                               locator=self.format_locator,
                               strategy='ios uiautomation',
                               element_name=book_format,
                               pages_to_search=pages_to_search,
                               fail_if_not_found=False,
                               time_to_wait=time_to_wait).is_present

    def is_any_book_present(self, pages_to_search=1, time_to_wait=5):
        return BasePageElement(driver=self.driver,
                               locator=locators["book.toggle_favourite"],
                               strategy='ios uiautomation',
                               pages_to_search=pages_to_search,
                               fail_if_not_found=False,
                               time_to_wait=time_to_wait).is_present

    def make_top_pane_visible(self):
        """Method makes top and bottom panes visible after they have been hidden by scrolling down."""
        if self.all_books:
            if not self.all_books.is_displayed():
                scroll_up(self.driver, 1)

    def get_to_top_of_page(self):
        if not hasattr(self, "top_book"):
            log("Dont have attribute 'top_book'. Initiating...")
            self.top_book = BasePageElement(driver=self.driver,
                                            locator=locators["books_page.top_book"],
                                            strategy='ios uiautomation',
                                            element_name="BooksTopBookCell",
                                            pages_to_search=1)
        while not self.top_book.is_displayed():
            scroll_up(self.driver, 1)

    def clean_favourites(self, get_back_to_all_books_page=True):
        self.open_favorites()
        log("Started cleaning favorites...")
        self.favorites_locator = locators["book.toggle_favourite"]
        while len(self.driver.find_elements_by_ios_uiautomation(self.favorites_locator)) > 0:
            self.driver.find_elements_by_ios_uiautomation(self.favorites_locator)[0].click()
            log("Removed book from favorites.")
        log("Favorites cleaned.")

        if self.is_any_book_present():
            self.fail("Some books are still favorite!")

        if get_back_to_all_books_page:
            self.open_all_books()

    def switch_to_list_view(self, is_all_books_current=True, check_current=True):
        # if all books is not a current page than open it. otherwise skip.
        if not is_all_books_current:
            self.open_all_books()

        log("Trying to switch to list view...")

        if check_current:
            self.top_item_toggle_favorite = BasePageElement(driver=self.driver,
                                                            locator=locators["book.toggle_favourite"],
                                                            strategy='ios uiautomation',
                                                            element_name="BooksTopItemFavorite",
                                                            time_to_wait=3,
                                                            pages_to_search=1,
                                                            fail_if_not_found=False)

        # if len(self.driver.find_elements_by_ios_uiautomation(locators["book.toggle_favourite"])) == 0:
        if not check_current or self.top_item_toggle_favorite.element is None:
            if self.device_type == "Phone":
                self.open_books_more_menu()
                self.list_icon = BasePageElement(driver=self.driver,
                                                 locator=locators["books_more_menu.list_button"],
                                                 strategy='ios uiautomation',
                                                 element_name="BooksListViewButton",
                                                 time_to_wait=5)
                self.list_icon.select()
            else:
                self.mode_list_button = BasePageElement(driver=self.driver,
                                                        locator=locators["books_page.mode_list"],
                                                        strategy='ios uiautomation',
                                                        element_name="BooksListModeButton")
                self.mode_list_button.select()
            log("Switched to list view.")
        else:
            log("Current view is List.")

    def toggle_favorites_by_title(self, book_title):
        # build locator
        self.favorite_element_locator = self.title_locator = "target.frontMostApp().mainWindow().collectionViews()[0].cells()[\"" + book_title + "\"].buttons()[\"favorites\"]"

        log("Trying to add book \"" + book_title + "\" to favorites...")

        self.favorites_element = BasePageElement(driver=self.driver,
                                                 locator=self.favorite_element_locator,
                                                 strategy='ios uiautomation',
                                                 element_name="BooksToggleFavoritesButton")
        self.favorites_element.select()

        log("Book \"" + book_title + "\" favorites toggled.")

    def toggle_favorites_by_format(self, book_format):
        # build locator
        self.favorite_element_locator = self.title_locator = "target.frontMostApp().mainWindow().collectionViews()[0].cells().firstWithPredicate(\"ANY staticTexts.name LIKE '" + book_format + "'\").buttons()[\"favorites\"]"

        log("Trying to add book with format \"" + book_format + "\" to favorites...")

        self.favorites_element = BasePageElement(driver=self.driver,
                                                 locator=self.favorite_element_locator,
                                                 strategy='ios uiautomation',
                                                 element_name="BooksToggleFavoritesButton")
        self.favorites_element.select()

        log("Book with format \"" + book_format + "\" favorites toggled.")

    def toggle_favorites_by_author(self, author):
        # build locator
        self.favorite_element_locator = self.title_locator = "target.frontMostApp().mainWindow().collectionViews()[0].cells().firstWithPredicate(\"ANY staticTexts.name LIKE '" + author + "'\").buttons()[\"favorites\"]"

        log("Trying to add book by author \"" + author + "\" to favorites...")

        self.favorites_element = BasePageElement(driver=self.driver,
                                                 locator=self.favorite_element_locator,
                                                 strategy='ios uiautomation',
                                                 element_name="BooksToggleFavoritesButton")
        self.favorites_element.select()

        log("Book by author \"" + author + "\" favorites toggled.")

    def find_book_by_format(self, book_format, pages_to_search=1, search_direction='down'):
        self.pages_to_search = pages_to_search
        return BookListObject(self.driver, book_format=book_format, pages_to_search=self.pages_to_search, search_direction=search_direction, device_type=self.device_type)

    def find_book_by_title(self, book_title, pages_to_search=1, search_direction='down'):
        self.pages_to_search = pages_to_search
        return BookListObject(self.driver, book_title=book_title, pages_to_search=self.pages_to_search, search_direction=search_direction, device_type=self.device_type)


# ------------------ Favourites Books page -----------------------------------
class BooksAllBooksPageObject(BooksPageObject):
    pass


# ------------------ All Books page -----------------------------------
class BooksRecentReadPageObject(BooksPageObject):
    pass


# ------------------ All Books page -----------------------------------
class BooksFavouritesPageObject(BooksPageObject):
    pass


# ------------------- Book object on the list----------------------
class BookListObject(BasePageObject):
    """Page object represents Books page of the app"""
    def __init__(self, driver, book_title=None, book_format=None, pages_to_search=1, search_direction='down', device_type="Phone"):
        self.driver = driver
        self.book_format = book_format
        self.book_title = book_title
        self.pages_to_search = pages_to_search
        self.device_type = device_type

        if self.book_format is not None:
            log("Trying to find book in " + book_format + " format...")
            self.format_locator = "target.frontMostApp().mainWindow().collectionViews()[0].cells().firstWithPredicate(\"ANY staticTexts.name LIKE '" + book_format + "' and isVisible == 1\").staticTexts().firstWithPredicate(\"value like '" + book_format +"'\")"
            self.format_el = BookFormatElement(driver=self.driver,
                                               strategy='ios uiautomation',
                                               locator=self.format_locator,
                                               time_to_wait=DEFAULT_WAIT_FOR_ELEMENT_SCROLL,
                                               pages_to_search=self.pages_to_search,
                                               search_direction=search_direction,
                                               element_name="Book format - " + self.book_format)
            log("Book in " + book_format + " format found.")
            self.element_to_open_book = self.format_el

        if self.book_title is not None:
            log("Trying to find book with title " + self.book_title + "...")
            self.title_locator = "target.frontMostApp().mainWindow().collectionViews()[0].cells()[\"" + self.book_title + "\"]"
            self.title_el = BookTitleElement(driver=self.driver,
                                             strategy='ios uiautomation',
                                             locator=self.title_locator,
                                             time_to_wait=DEFAULT_WAIT_FOR_ELEMENT_SCROLL,
                                             pages_to_search=self.pages_to_search,
                                             search_direction=search_direction,
                                             element_name="Book - " + self.book_title)
            log("Book with " + self.book_title + " title found.")
            self.element_to_open_book = self.title_el

    def open_book(self):
        self.element_to_open_book.select()
        return OpenedBookPageObject(self.driver, device_type=self.device_type, book_title=self.book_title)


class BookTitleElement(BasePageElement):
    pass


class BookFormatElement(BasePageElement):
    pass
