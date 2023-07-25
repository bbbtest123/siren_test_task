from tests.helpers import helpers
from tests.pages.confirm_phone_page import ConfirmPhonePage
from tests.pages.phone_number_page import PhoneNumberPage
from tests.pages.base_page import BasePage


# Class for full name and email input pages
class NameEmailPage(BasePage):
    IS_AT_TEXT = "Who should I prepare this estimate for?"

    INPUT_GROUP_XPATH = "div[div[@class='customInput__group'] and contains(@class, 'customInput')]"

    FULL_NAME_INPUT_XPATH = "//input[@id='fullName']"
    FULL_NAME_INPUT_GROUP_XPATH = FULL_NAME_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    FULL_NAME_INPUT_MESSAGE_XPATH = FULL_NAME_INPUT_GROUP_XPATH + "/div[@class='customInput__message']"
    FULL_NAME_EMPTY_TEXT = "Enter your full name"
    FULL_NAME_INCOMPLETE_TEXT = "Your full name should contain both first and last name"
    FULL_NAME_INVALID_TEXT = "Full name can consist only of latin letters and dashes"

    EMAIL_INPUT_XPATH = "//input[@id='email']"
    EMAIL_INPUT_GROUP_XPATH = EMAIL_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    EMAIL_INPUT_MESSAGE_XPATH = EMAIL_INPUT_GROUP_XPATH + "/div[@class='customInput__message']"
    EMAIL_EMPTY_TEXT = "Enter your email address"
    EMAIL_INVALID_TEXT = "Wrong email"

    NEXT_PAGE_CLASS = PhoneNumberPage

    def enter_full_name(self, value: str):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.FULL_NAME_INPUT_XPATH, value)

        return self

    def enter_email(self, value: str):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.EMAIL_INPUT_XPATH, value)

        return self

    def assert_no_full_name_message(self):
        assert helpers.get_attribute_value(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH, "data-visibility") \
               == "hidden", "Expected no full name input message to not be shown"

    def assert_no_email_message(self):
        assert helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH, "data-visibility") \
               == "hidden", "Expected no email input message to not be shown"

    def assert_full_name_empty(self):
        assert helpers.get_attribute_value(self.driver, self.FULL_NAME_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected full name input to have 'invalid' state"
        return helpers.text(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH) == self.FULL_NAME_EMPTY_TEXT, \
            f"Expected phone input message to be '{self.FULL_NAME_EMPTY_TEXT}', " \
            f"found '{helpers.text(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH)}' instead"

    def assert_full_name_incomplete(self):
        assert helpers.get_attribute_value(self.driver, self.FULL_NAME_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected full name input to have 'invalid' state"
        return helpers.text(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH) == self.FULL_NAME_INCOMPLETE_TEXT, \
            f"Expected phone input message to be '{self.FULL_NAME_INCOMPLETE_TEXT}', " \
            f"found '{helpers.text(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH)}' instead"

    def assert_full_name_invalid(self):
        assert helpers.get_attribute_value(self.driver, self.FULL_NAME_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected full name input to have 'invalid' state"
        return helpers.text(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH) == self.FULL_NAME_INVALID_TEXT, \
            f"Expected phone input message to be '{self.FULL_NAME_INVALID_TEXT}', " \
            f"found '{helpers.text(self.driver, self.FULL_NAME_INPUT_MESSAGE_XPATH)}' instead"

    def assert_email_empty(self):
        assert helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected email input to have 'invalid' state"
        return helpers.text(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH) == self.EMAIL_EMPTY_TEXT, \
            f"Expected phone input message to be '{self.EMAIL_EMPTY_TEXT}', " \
            f"found '{helpers.text(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH)}' instead"

    def assert_email_invalid(self):
        assert helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected email input to have 'invalid' state"
        return helpers.text(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH) == self.EMAIL_INVALID_TEXT, \
            f"Expected phone input message to be '{self.EMAIL_INVALID_TEXT}', " \
            f"found '{helpers.text(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH)}' instead"
