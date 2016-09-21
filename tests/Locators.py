# -*- coding: utf-8 -*-"
""" Locators for page elements"""

locators = {}

# page1 English phone
locators["page1.title"] = "target.frontMostApp().mainWindow().staticTexts().firstWithPredicate(\"value like 'Books'\")"
locators["page1.ok_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Ok\"]"
locators["page1.cancel_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Cancel\"]"

# page2 English phone
locators["page2.title"] = "target.frontMostApp().mainWindow().staticTexts().firstWithPredicate(\"value like 'Books'\")"
locators["page2.ok_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Ok\"]"
locators["page2.cancel_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Cancel\"]"


# set locators for german localization. can be called on test initialization
def set_german():
    # page1 English phone
    locators["page1.title"] = "target.frontMostApp().mainWindow().staticTexts().firstWithPredicate(\"value like 'Bücher'\")"
    locators["page1.ok_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Kürzlich\"]"
    locators["page1.cancel_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Anmelden\"]"


# set locators for tablet interface in case it differs from phone's
def set_tablet():
    # page2 English tablet
    locators["page2.title"] = "target.frontMostApp().mainWindow().staticTexts().firstWithPredicate(\"value like 'Books'\")"
    locators["page2.ok_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Ok\"]"
    locators["page2.cancel_button"] = "target.frontMostApp().mainWindow().segmentedControls()[0].buttons()[\"Cancel\"]"

    print "Locators has been set for Tablet device type."
