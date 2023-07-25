from tests.helpers import helpers
from tests.pages.area_page import AreaPage
from tests.pages.base_grid_page import BaseGridPage


# Class for Type of Project question page
class TypeOfSidingPage(BaseGridPage):
    IS_AT_TEXT = "What kind of siding do you want?"

    YES_NO_ELEMENT_INDEX = 5

    NEXT_PAGE_CLASS = AreaPage
