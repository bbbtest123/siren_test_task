from tests.helpers import helpers


# Base class for questionary pages
class BasePage:
    STEP_XPATH = "//div[@id='StepBodyId']"

    IS_AT_XPATH = "//div[@id='StepBodyId']//h4"
    IS_AT_TEXT = "Base question text"

    INPUT_GROUP_XPATH = "div[div[@class='customInput__group'] and contains(@class, 'customInput')]"

    NEXT_BUTTON_XPATH = "//button[@data-autotest-button-submit-next]"

    NEXT_PAGE_CLASS = None

    def __init__(self, driver):
        self.driver = driver

    # Class method for the assertion that we are on this page currently
    @classmethod
    def assert_at(cls, driver):
        assert helpers.text(driver, cls.IS_AT_XPATH, timeout=10) == cls.IS_AT_TEXT, \
            f"Expected header to be '{cls.IS_AT_TEXT}', found '{helpers.text(driver, cls.IS_AT_XPATH)}' instead"

    # Class method for checking that we are on this page currently
    @classmethod
    def is_at(cls, driver) -> bool:
        if helpers.element_exists(driver, cls.IS_AT_XPATH, timeout=10):
            return helpers.text(driver, cls.IS_AT_XPATH, timeout=10) == cls.IS_AT_TEXT
        else:
            return False

    # Assertion that 'Next' button is currently enabled
    def assert_next_button_enabled(self):
        assert helpers.is_enabled(self.driver, self.NEXT_BUTTON_XPATH), "Expected Next button to be enabled"

    # Assertion that 'Next' button is currently disabled
    def assert_next_button_disabled(self):
        assert not helpers.is_enabled(self.driver, self.NEXT_BUTTON_XPATH), "Expected Next button to be disabled"

    # Press 'Next' button
    def press_next(self):
        helpers.click(self.driver, self.NEXT_BUTTON_XPATH)

        # Wait while 'Next' button in the 'processing' state
        if helpers.element_exists(self.driver, self.NEXT_BUTTON_XPATH):
            helpers.wait_while_element_has_attribute_value(self.driver, self.NEXT_BUTTON_XPATH, "data-state",
                                                           "processing", timeout=10)

        # Wait while Questionary step element is in the 'step-prev' state
        if helpers.element_exists(self.driver, self.STEP_XPATH):
            helpers.wait_while_element_has_attribute_value(self.driver, self.STEP_XPATH, "class", "step-prev",
                                                           timeout=10)

        if self.NEXT_PAGE_CLASS.is_at(self.driver):
            return self.NEXT_PAGE_CLASS(self.driver)
        else:
            return self
