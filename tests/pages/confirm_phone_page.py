from tests.helpers import helpers
from tests.pages.base_page import BasePage
from tests.pages.thank_you_page import ThankYouPage


# Class for phone number confirmation pages
class ConfirmPhonePage(BasePage):
    IS_AT_TEXT = "Please confirm your phone number."

    INPUT_GROUP_XPATH = "div[div[@class='customInput__group'] and contains(@class, 'customInput')]"
    PHONE_INPUT_XPATH = "//input[@id='phoneNumber']"
    PHONE_INPUT_GROUP_XPATH = PHONE_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    PHONE_INPUT_MESSAGE_XPATH = PHONE_INPUT_GROUP_XPATH + "/div[@class='customInput__message']"

    PHONE_EMPTY_TEXT = "Please enter your phone number"

    PHONE_INVALID_TEXT = "Invalid Phone number"

    PHONE_EDIT_BUTTON_XPATH = "//button[@data-autotest-button-button-edit-phone-number]"
    NEXT_BUTTON_XPATH = "//button[@data-autotest-button-submit-phone-number-is-correct]"

    NEXT_PAGE_CLASS = ThankYouPage

    def press_edit(self):
        helpers.click(self.driver, self.PHONE_EDIT_BUTTON_XPATH)

        return self

    def enter_phone_number(self, value: str):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.PHONE_INPUT_XPATH, value)
        else:
            helpers.clear_value(self.driver, self.PHONE_INPUT_XPATH)

        return self

    def assert_phone_number_empty(self):
        assert helpers.get_attribute_value(self.driver, self.PHONE_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected phone input to have 'invalid' state"
        assert helpers.text(self.driver, self.PHONE_INPUT_MESSAGE_XPATH) == self.PHONE_EMPTY_TEXT, \
            f"Expected phone input message to be '{self.PHONE_EMPTY_TEXT}', " \
            f"found '{helpers.text(self.driver, self.PHONE_INPUT_MESSAGE_XPATH)}' instead"

    def assert_phone_number_invalid(self):
        assert helpers.get_attribute_value(self.driver, self.PHONE_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected phone input to have 'invalid' state"
        assert helpers.text(self.driver, self.PHONE_INPUT_MESSAGE_XPATH) == self.PHONE_INVALID_TEXT, \
            f"Expected phone input message to be '{self.PHONE_INVALID_TEXT}', " \
            f"found '{helpers.text(self.driver, self.PHONE_INPUT_MESSAGE_XPATH)}' instead"
