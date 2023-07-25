from tests.helpers import helpers
from tests.pages.base_page import BasePage


class ThankYouPage(BasePage):
    IS_AT_XPATH = "//h4[contains(@class, 'text-center')]"

    @classmethod
    def assert_at(cls, driver):
        text = helpers.text(driver, cls.IS_AT_XPATH, timeout=10)
        assert helpers.text(driver, cls.IS_AT_XPATH, timeout=10).__contains__("Thank you"), \
               f"Expected header to contain 'Thank you', found '{helpers.text(driver, cls.IS_AT_XPATH)}' instead"

    @classmethod
    def is_at(cls, driver) -> bool:
        text = helpers.text(driver, cls.IS_AT_XPATH, timeout=10)

        if helpers.find_element_single(driver, cls.IS_AT_XPATH, timeout=10):
            return helpers.text(driver, cls.IS_AT_XPATH, timeout=10).__contains__("Thank you")
        else:
            return False
