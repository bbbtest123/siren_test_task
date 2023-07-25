from tests.helpers import helpers
from tests.pages.is_homeowner_page import IsHomeownerPage
from tests.pages.base_grid_page import BaseGridPage


# Class for stories count question pages
class StoriesCountPage(BaseGridPage):
    IS_AT_TEXT = "How many stories is your house?"

    YES_NO_ELEMENT_INDEX = 3

    NOTIFICATION_TEXT = "Unfortunately our contractors don’t work on homes taller than three stories. " \
                        "Would you like to continue?"

    NEXT_PAGE_CLASS = IsHomeownerPage

    def select(self, count: int):
        grid = helpers.find_elements(self.driver, self.GRID_ELEMENTS_XPATH)
        self.current_element_index = count
        grid[count].click()

        return self
