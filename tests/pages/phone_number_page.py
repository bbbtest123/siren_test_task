from tests.helpers import helpers
from tests.pages.confirm_phone_page import ConfirmPhonePage
from tests.pages.base_page import BasePage
from tests.pages.phone_email_already_exist_page import PhoneEmailAlreadyExistPage


# Class for phone number input pages
class PhoneNumberPage(BasePage):
    IS_AT_TEXT = "What is your phone number?"

    INPUT_GROUP_XPATH = "div[div[@class='customInput__group'] and contains(@class, 'customInput')]"

    PHONE_INPUT_XPATH = "//input[@id='phoneNumber']"
    PHONE_INPUT_GROUP_XPATH = PHONE_INPUT_XPATH + "//ancestor::" + INPUT_GROUP_XPATH
    PHONE_INPUT_MESSAGE_XPATH = PHONE_INPUT_GROUP_XPATH + "/div[@class='customInput__message']"

    PHONE_EMPTY_TEXT = "Please enter your phone number"

    PHONE_INVALID_TEXT = "Invalid Phone number"

    NEXT_BUTTON_XPATH = "//button[@data-autotest-button-submit-submit-my-request]"

    NEXT_PAGE_CLASS = ConfirmPhonePage

    def enter_phone_number(self, value: str):
        if value is not None and value != "":
            helpers.enter_value(self.driver, self.PHONE_INPUT_XPATH, value)

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

    def press_next(self):
        helpers.click(self.driver, self.NEXT_BUTTON_XPATH)

        if helpers.element_exists(self.driver, self.NEXT_BUTTON_XPATH):
            helpers.wait_while_element_has_attribute_value(self.driver, self.NEXT_BUTTON_XPATH, "data-state",
                                                       "processing", timeout=10)

        if helpers.element_exists(self.driver, self.STEP_XPATH):
            helpers.wait_while_element_has_attribute_value(self.driver, self.STEP_XPATH, "class", "step-prev",
                                                           timeout=10)

        if self.NEXT_PAGE_CLASS.is_at(self.driver):
            return self.NEXT_PAGE_CLASS(self.driver)
        elif PhoneEmailAlreadyExistPage.is_at(self.driver):
            return PhoneEmailAlreadyExistPage(self.driver)
        else:
            return self
