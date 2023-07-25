from enum import Enum

from tests.helpers import helpers
from tests.pages.base_page import BasePage
from tests.pages.sorry_page import SorryPage


# Base class for questionary pages with grid
class BaseGridPage(BasePage):
    STEP_XPATH = "//div[@id='StepBodyId']"

    GRID_ELEMENTS_XPATH = "//div[@id='StepBodyId']//div[contains(@class, 'defaultGrid')]/div"

    NOTIFICATION_TEXT_XPATH = "//div[contains(@class, 'text-center')]"

    YES_NO_ELEMENT_INDEX = 0

    NOTIFICATION_TEXT = "Base notification text"

    YES_BUTTON_XPATH = "//button[@data-autotest-button-submit-yes]"
    NO_BUTTON_XPATH = "//button[@data-autotest-button-button-no]"

    def __init__(self, driver):
        super().__init__(driver)
        self.current_element_index = 0

    def select(self, enum: Enum):
        grid_elements = helpers.find_elements(self.driver, self.GRID_ELEMENTS_XPATH)
        self.current_element_index = enum.value
        grid_elements[enum.value].click()

        return self

    def press_next(self):
        if self.current_element_index == self.YES_NO_ELEMENT_INDEX:
            helpers.click(self.driver, self.YES_BUTTON_XPATH)
        else:
            helpers.click(self.driver, self.NEXT_BUTTON_XPATH)

        helpers.wait_while_element_has_attribute_value(self.driver, self.STEP_XPATH, "class", "step-prev", timeout=10)

        return self.NEXT_PAGE_CLASS(self.driver)

    def press_no(self) -> SorryPage:
        helpers.click(self.driver, self.NO_BUTTON_XPATH)

        return SorryPage(self.driver)
