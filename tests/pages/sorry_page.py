from tests.pages.base_page import BasePage


# Class for Sorry page
class SorryPage(BasePage):
    IS_AT_XPATH = "//h3[contains(@class, 'text-center')]"
    IS_AT_TEXT = "Sorry to see you go!"

    HOME_PAGE_BUTTON_XPATH = "//div[@id='StepBodyId']//button"
