from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Helpers methods for WebElement search and manipulations
class element_has_no_attribute_value(object):
    """An expectation for checking that an element has different value to provided for provided attribute.

    locator - used to find the element
    attribute_key - attribute key
    attribute_value - attribute value
    returns the True if an element has different value to provided for provided class, else False.
    """

    def __init__(self, locator: tuple[str, str], attribute_key: str, attribute_value: str):
        self.locator = locator
        self.attribute_key = attribute_key
        self.attribute_value = attribute_value

    def __call__(self, driver):
        if element_exists(driver, self.locator[1], self.locator[0]):
            element = find_element(driver, self.locator[1], self.locator[0])

            if element.get_attribute(self.attribute_key) == self.attribute_value:
                return False
            else:
                return True
        else:
            return True


class single_element_exists(object):
    """An expectation for checking that only one element exists on a page.

    locator - used to find the element
    timeout - wait timeout
    returns the True if only one element exists on a page, else False.
    """

    def __init__(self, locator: tuple[str, str], timeout: int):
        self.locator = locator
        self.timeout = timeout

    def __call__(self, driver):
        if len(find_elements(driver, self.locator[1], self.locator[0], self.timeout)) == 1:
            return True
        else:
            return False


def element_exists(driver, by_value: str, by: str = By.XPATH, timeout: int = 0) -> bool:
    """Check if element exists on a page.

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns True if the element exists in DOM, else False
    """
    if find_element(driver, by_value, by, timeout) is None:
        return False
    else:
        return True


def find_element(driver, by_value: str, by: str = By.XPATH, timeout: int = 0) -> WebElement:
    """Find an element on a page.

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns WebElement if the element exists in DOM, else None
    """
    try:
        if timeout > 0:
            return WebDriverWait(driver, timeout=timeout).until(EC.presence_of_element_located((by, by_value)))
        else:
            return driver.find_element(by, by_value)
    except (TimeoutException, NoSuchElementException):
        return None


def find_elements(driver, by_value: str, by: str = By.XPATH, timeout: int = 0) -> list[WebElement]:
    """Find elements list on a page.

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns list[WebElement]
    """
    if timeout > 0:
        return WebDriverWait(driver, timeout=timeout).until(EC.presence_of_all_elements_located((by, by_value)))
    else:
        return driver.find_elements(by, by_value)


def find_element_single(driver, by_value: str, by: str = By.XPATH, timeout: int = 0) -> WebElement:
    """Find an element on a page and return it only if a single element found.

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns WebElement it only if a single element found, else None
    """
    try:
        if timeout > 0:
            return WebDriverWait(driver, timeout=timeout).until(single_element_exists((by, by_value), timeout))
        else:
            return driver.find_element(by, by_value)
    except (TimeoutException, NoSuchElementException):
        return None


def wait_while_element_has_attribute_value(driver, by_value: str, attribute_key: str, attribute_value: str,
                                           by: str = By.XPATH, timeout: int = 0):
    """Wait while an element have specified value for specified attribute.

    driver - Selenium WebDriver instance
    by_value - search value for an element
    attribute_key - an attribute for checking value
    attribute_value - an attribute value
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    """
    WebDriverWait(driver, timeout=timeout).until(element_has_no_attribute_value((by, by_value),
                                                                                attribute_key,
                                                                                attribute_value))


def enter_value(driver, by_value: str, value: str, by: str = By.XPATH, timeout: int = 0):
    """Enter specified value to specified element

    driver - Selenium WebDriver instance
    by_value - search value for an element
    value - value to enter
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    """
    element = find_element(driver, by_value, by, timeout)

    if element.get_attribute("value") != str(value):
        clear_value(driver, by_value, by, timeout)
        element.send_keys(str(value))


def clear_value(driver, by_value: str, by: str = By.XPATH, timeout: int = 0):
    """Clear value of specified element

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    """
    element = find_element(driver, by_value, by, timeout)

    element.clear()

    while element.get_attribute("value") != "" and element.get_attribute("value") != "+1(___)___-____":
        element.send_keys(Keys.BACK_SPACE)


def click(driver, by_value: str, by: str = By.XPATH, timeout: int = 0):
    """Click on specified element

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    """
    element = find_element(driver, by_value, by, timeout)
    element.click()


def get_attribute_value(driver, by_value: str, attribute_key: str, by: str = By.XPATH, timeout: int = 0) -> str:
    """Get value of specified element's attribute

    driver - Selenium WebDriver instance
    by_value - search value for an element
    attribute_key - attribute to get the value of
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns the value of specified attribute if element is found, else returns empty string
    """
    element = find_element(driver, by_value, by, timeout)
    if element is not None:
        return find_element(driver, by_value, by, timeout).get_attribute(attribute_key)
    else:
        return ""


def text(driver, by_value: str, by: str = By.XPATH, timeout: int = 0) -> str:
    """Get text of specified element

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns text of specified element
    """
    return find_element(driver, by_value, by, timeout).text


def is_enabled(driver, by_value: str, by: str = By.XPATH, timeout: int = 0) -> bool:
    """Check if specified element is enabled

    driver - Selenium WebDriver instance
    by_value - search value for an element
    by - Selenium locator strategy
    timeout - timeout in seconds for selenium waits
    returns True if specified element is enabled, else False
    """
    return find_element(driver, by_value, by, timeout).is_enabled()
