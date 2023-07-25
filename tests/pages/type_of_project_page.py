from tests.helpers import helpers
from tests.pages.base_grid_page import BaseGridPage
from tests.pages.type_of_siding_page import TypeOfSidingPage


# Class for Type of Project question page
class TypeOfProjectPage(BaseGridPage):
    IS_AT_TEXT = "What type of project is this?"

    YES_NO_ELEMENT_INDEX = 2
    NOTIFICATION_TEXT = "Some contractors will only repair/replace siding for a minimum of one full side of a house. " \
                        "Would you like to continue?"

    NEXT_PAGE_CLASS = TypeOfSidingPage
