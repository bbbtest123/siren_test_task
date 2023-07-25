import pytest

from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")


def pytest_generate_tests(metafunc):
    browser = metafunc.config.option.browser
    if "browser" in metafunc.fixturenames and browser is not None:
        metafunc.parametrize("browser", [browser])


@pytest.fixture(scope="function")
def before_and_after(browser):
    if browser == "chrome":
        pytest.driver = webdriver.Chrome()
    if browser == "firefox":
        pytest.driver = webdriver.Firefox()

    pytest.driver.get("https://hb-eta.stage.sirenltd.dev/siding")

    yield pytest.driver

    pytest.driver.quit()
