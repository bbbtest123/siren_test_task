from tests.helpers import helpers
from tests.pages.base_page import BasePage
from tests.pages.stories_count_page import StoriesCountPage


# Class for area question pages
class AreaPage(BasePage):
    IS_AT_TEXT = "Approximately how many square feet will be covered with new siding?"

    INPUT_GROUP_XPATH = "div[div[@class='customInput__group'] and contains(@class, 'customInput')]"
    AREA_INPUT_XPATH = "//input[@id='squareFeet']"
    AREA_INPUT_GROUP_XPATH = AREA_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    AREA_INPUT_MESSAGE_XPATH = AREA_INPUT_GROUP_XPATH + "//div[@class='customInput__message']"
    NOT_SURE_CHECKBOX_XPATH = "//div[input[@name='notSure']]"

    AREA_INVALID_TEXT = "Please use numbers only"
    AREA_STARTS_WITH_ZERO_TEXT = "Number can’t start with 0"

    NEXT_PAGE_CLASS = StoriesCountPage

    def enter_area(self, value: str, not_sure: bool = False):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.AREA_INPUT_XPATH, value)

        if not_sure:
            helpers.click(self.driver, self.NOT_SURE_CHECKBOX_XPATH)

        return self

    def assert_area_invalid(self):
        assert helpers.get_attribute_value(self.driver, self.AREA_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected area input to have 'invalid' state"
        assert helpers.text(self.driver, self.AREA_INPUT_MESSAGE_XPATH) == self.AREA_INVALID_TEXT, \
            f"Expected area input message to be '{self.AREA_INVALID_TEXT}', " \
            f"found '{helpers.text(self.driver, self.AREA_INPUT_MESSAGE_XPATH)}' instead"

    def assert_area_starts_with_zero(self):
        assert helpers.get_attribute_value(self.driver, self.AREA_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected area input to have 'invalid' state"
        assert helpers.text(self.driver, self.AREA_INPUT_MESSAGE_XPATH) == self.AREA_STARTS_WITH_ZERO_TEXT, \
            f"Expected area input message to be '{self.AREA_STARTS_WITH_ZERO_TEXT}', " \
            f"found '{helpers.text(self.driver, self.AREA_INPUT_MESSAGE_XPATH)}' instead"
