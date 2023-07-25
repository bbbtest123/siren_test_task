from tests.helpers import helpers
from tests.pages.base_page import BasePage
from tests.pages.thank_you_page import ThankYouPage


class PhoneEmailAlreadyExistPage(BasePage):
    IS_AT_TEXT = "This phone number and email already exist in our database."

    INPUT_GROUP_XPATH = "div[div[@class='customInput__group'] and contains(@class, 'customInput')]"

    PHONE_INPUT_XPATH = "//input[@id='phoneNumber']"
    PHONE_INPUT_GROUP_XPATH = PHONE_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    PHONE_INPUT_MESSAGE_XPATH = PHONE_INPUT_GROUP_XPATH + "/div[@class='customInput__message']"
    PHONE_EMPTY_TEXT = "Please enter your phone number"
    PHONE_INVALID_TEXT = "Invalid Phone number"
    PHONE_EXISTS_TEXT = "Change phone number"

    EMAIL_INPUT_XPATH = "//input[@id='email']"
    EMAIL_INPUT_GROUP_XPATH = EMAIL_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    EMAIL_INPUT_MESSAGE_XPATH = EMAIL_INPUT_GROUP_XPATH + "/div[@class='customInput__message']"
    EMAIL_EMPTY_TEXT = "Enter your email address"
    EMAIL_INVALID_TEXT = "Wrong email"
    EMAIL_EXISTS_TEXT = "Change Email address"

    NEXT_PAGE_CLASS = ThankYouPage

    def enter_phone_number(self, value: str):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.PHONE_INPUT_XPATH, value)
        else:
            helpers.clear_value(self.driver, self.PHONE_INPUT_XPATH)

        return self

    def enter_email(self, value: str):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.EMAIL_INPUT_XPATH, value)
        else:
            helpers.clear_value(self.driver, self.EMAIL_INPUT_XPATH)

        return self

    def assert_no_phone_message(self):
        assert helpers.get_attribute_value(self.driver, self.PHONE_INPUT_MESSAGE_XPATH, "data-visibility") \
               == "hidden", "Expected no phone input message to not be shown"

    def no_phone_message(self) -> bool:
        return helpers.get_attribute_value(self.driver, self.PHONE_INPUT_MESSAGE_XPATH, "data-visibility") \
               == "hidden"

    def assert_no_email_message(self):
        assert helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH, "data-visibility") \
               == "hidden", "Expected no email input message to not be shown"

    def no_email_message(self) -> bool:
        return helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH, "data-visibility") \
               == "hidden"

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

    def assert_phone_number_exists(self):
        assert helpers.get_attribute_value(self.driver, self.PHONE_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected phone input to have 'invalid' state"
        assert helpers.text(self.driver, self.PHONE_INPUT_MESSAGE_XPATH) == self.PHONE_EXISTS_TEXT, \
            f"Expected phone input message to be '{self.PHONE_EXISTS_TEXT}', " \
            f"found '{helpers.text(self.driver, self.PHONE_INPUT_MESSAGE_XPATH)}' instead"

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

    def assert_email_exists(self):
        assert helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_GROUP_XPATH, "data-status") == "invalid", \
            f"Expected phone input to have 'invalid' state"
        assert helpers.text(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH) == self.EMAIL_EXISTS_TEXT, \
            f"Expected email input message to be '{self.PHONE_EXISTS_TEXT}', " \
            f"found '{helpers.text(self.driver, self.EMAIL_INPUT_MESSAGE_XPATH)}' instead"

    def press_next(self):
        helpers.click(self.driver, self.NEXT_BUTTON_XPATH)

        helpers.wait_while_element_has_attribute_value(self.driver, self.NEXT_BUTTON_XPATH, "data-state",
                                                       "processing", timeout=10)

        if helpers.element_exists(self.driver, self.STEP_XPATH):
            helpers.wait_while_element_has_attribute_value(self.driver, self.STEP_XPATH, "class", "step-prev",
                                                           timeout=10)

        if helpers.get_attribute_value(self.driver, self.EMAIL_INPUT_GROUP_XPATH, "data-status") == "invalid" \
                or helpers.get_attribute_value(self.driver, self.PHONE_INPUT_GROUP_XPATH, "data-status") == "invalid":
            return self
        elif self.NEXT_PAGE_CLASS.is_at(self.driver):
            return self.NEXT_PAGE_CLASS(self.driver)
        else:
            return self
