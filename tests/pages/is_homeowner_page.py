from tests.helpers import helpers
from tests.pages.name_email_page import NameEmailPage
from tests.pages.base_grid_page import BaseGridPage


# Class for Is Homeowner question pages
class IsHomeownerPage(BaseGridPage):
    IS_AT_TEXT = "Are you the homeowner or authorized to make property changes?"

    IS_HOMEOWNER_BUTTON_XPATH = "//div[input[@data-autotest-radio-internalowner-1]]"
    IS_NOT_HOMEOWNER_BUTTON_XPATH = "//div[input[@data-autotest-radio-internalowner-0]]"

    YES_NO_ELEMENT_INDEX = 1

    NOTIFICATION_TEXT = "Our contractors require the homeowner or someone authorized to make property changes be " \
                        "present during the estimate. Would you like to continue?"

    NEXT_PAGE_CLASS = NameEmailPage

    def select(self, is_homeowner: bool):
        if is_homeowner:
            self.current_element_index = 0
            helpers.click(self.driver, self.IS_HOMEOWNER_BUTTON_XPATH)
        else:
            self.current_element_index = 1
            helpers.click(self.driver, self.IS_NOT_HOMEOWNER_BUTTON_XPATH)

        return self
