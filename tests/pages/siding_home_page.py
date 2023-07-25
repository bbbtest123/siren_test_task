from tests.helpers import helpers
from tests.pages.base_page import BasePage
from tests.pages.no_contractors_page import NoContractorsPage
from tests.pages.type_of_project_page import TypeOfProjectPage


# Class for home page
class SidingHomePage(BasePage):
    IS_AT_XPATH = "//h1"
    IS_AT_TEXT = "How Much Does Siding Cost"

    ZIP_CODE_INPUT_XPATH = "//input[@id='zipCode']"

    ZIP_CODE_RIGHT_ICON_XPATH = "//form[@id='zip_header']//div[@class='rightIcon']"

    ZIP_CODE_CAPTION_XPATH = "//form[@id='zip_header']//div[@class='zip--caption']"
    ZIP_CODE_CAPTION_INVALID_TEXT = "Unknown ZIP Code"
    ZIP_CODE_CAPTION_EMPTY_TEXT = "Enter your ZIP Code"

    NEXT_BUTTON_XPATH = "//form[@id='zip_header']//button[@type='submit']"

    NEXT_PAGE_CLASS = TypeOfProjectPage

    def enter_zip_code(self, value: str):
        helpers.enter_value(self.driver, self.ZIP_CODE_INPUT_XPATH, value)

        return self

    def assert_zip_code_correct(self):
        assert helpers.get_attribute_value(self.driver, self.ZIP_CODE_RIGHT_ICON_XPATH, "style") \
            == "visibility: visible;", f"Expected correct mark on zip code input to be visible"

    def assert_zip_code_empty(self):
        assert helpers.text(self.driver, self.ZIP_CODE_CAPTION_XPATH) == self.ZIP_CODE_CAPTION_EMPTY_TEXT, \
            f"Expected input message to be '{self.ZIP_CODE_CAPTION_EMPTY_TEXT}', " \
            f"found '{helpers.text(self.driver, self.ZIP_CODE_CAPTION_XPATH)}' instead"

    def assert_zip_code_invalid(self):
        assert helpers.text(self.driver, self.ZIP_CODE_CAPTION_XPATH) == self.ZIP_CODE_CAPTION_INVALID_TEXT, \
            f"Expected input message to be '{self.ZIP_CODE_CAPTION_INVALID_TEXT}', " \
            f"found '{helpers.text(self.driver, self.ZIP_CODE_CAPTION_XPATH)}' instead"

    def press_next(self):
        helpers.click(self.driver, self.NEXT_BUTTON_XPATH)

        helpers.wait_while_element_has_attribute_value(self.driver, self.NEXT_BUTTON_XPATH, "data-state",
                                                       "processing", timeout=10)

        if helpers.element_exists(self.driver, self.STEP_XPATH):
            helpers.wait_while_element_has_attribute_value(self.driver, self.STEP_XPATH, "class", "step-prev",
                                                           timeout=10)

        # If input is invalid returning self
        if helpers.element_exists(self.driver, self.ZIP_CODE_CAPTION_XPATH) \
                and helpers.text(self.driver, self.ZIP_CODE_CAPTION_XPATH) == self.ZIP_CODE_CAPTION_INVALID_TEXT:
            return self
        # If on the next page - returning it
        elif self.NEXT_PAGE_CLASS.is_at(self.driver):
            return self.NEXT_PAGE_CLASS(self.driver)
        # If on No Contractors Page - returning it
        elif NoContractorsPage.is_at(self.driver):
            return NoContractorsPage(self.driver)
        else:
            return self
