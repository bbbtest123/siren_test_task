import pytest
import random
import string

from tests.helpers.enums import Expected, TypeOfProject, TypeOfSiding
from tests.pages.area_page import AreaPage
from tests.pages.confirm_phone_page import ConfirmPhonePage
from tests.pages.is_homeowner_page import IsHomeownerPage
from tests.pages.name_email_page import NameEmailPage
from tests.pages.no_contractors_page import NoContractorsPage
from tests.pages.phone_email_already_exist_page import PhoneEmailAlreadyExistPage
from tests.pages.phone_number_page import PhoneNumberPage
from tests.pages.siding_home_page import SidingHomePage
from tests.pages.sorry_page import SorryPage
from tests.pages.stories_count_page import StoriesCountPage
from tests.pages.thank_you_page import ThankYouPage
from tests.pages.type_of_project_page import TypeOfProjectPage
from tests.pages.type_of_siding_page import TypeOfSidingPage

CORRECT_ZIP_CODE = "09090"


def random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_email(recipient_length: int, domain_length: int) -> str:
    recipient = random_string(recipient_length)
    domain = random_string(domain_length)
    return recipient + "@" + domain + ".com"


def random_phone_number() -> str:
    return str(random.randrange(2000000000, 9999999999))


@pytest.mark.usefixtures("before_and_after")
class TestSidingQuestionary:
    @pytest.mark.parametrize("zip_code,expected", [(CORRECT_ZIP_CODE, Expected.CORRECT), ("", Expected.EMPTY),
                                                   ("0", Expected.INVALID), ("11111", Expected.WRONG_ZIP_CODE),
                                                   ("1234567890", Expected.INVALID), ("a", Expected.INVALID),
                                                   ("-09090", Expected.INVALID), ("0909.0", Expected.INVALID)])
    def test_zip_code(self, zip_code, expected):
        siding_home_page = SidingHomePage(pytest.driver)
        siding_home_page = siding_home_page.enter_zip_code(zip_code)

        if expected is Expected.CORRECT:
            siding_home_page.assert_zip_code_correct()

        siding_home_page.press_next()

        if expected is Expected.CORRECT:
            TypeOfProjectPage.assert_at(pytest.driver)
        elif expected is Expected.WRONG_ZIP_CODE:
            NoContractorsPage.assert_at(pytest.driver)
        elif expected is Expected.EMPTY:
            siding_home_page.assert_zip_code_empty()
        elif expected is Expected.INVALID:
            siding_home_page.assert_zip_code_invalid()

    @pytest.mark.parametrize("type_of_project,choose_no",
                             [(TypeOfProject.REPLACE, False), (TypeOfProject.NEW_ADDITION, False),
                              (TypeOfProject.REPAIR, False), (TypeOfProject.REPAIR, True),
                              (TypeOfProject.NEW_HOME, False), (TypeOfProject.NOT_SURE, False)])
    def test_type_of_project(self, type_of_project, choose_no):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        type_of_project_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE).press_next()

        type_of_project_page.assert_next_button_disabled()

        type_of_project_page = type_of_project_page.select(type_of_project)

        if choose_no:
            type_of_project_page.press_no()
            SorryPage.assert_at(pytest.driver)
        else:
            type_of_project_page.press_next()
            TypeOfSidingPage.assert_at(pytest.driver)

    @pytest.mark.parametrize("type_of_siding",
                             [TypeOfSiding.VINYL, TypeOfSiding.CEMENT, TypeOfSiding.WOOD, TypeOfSiding.OTHER,
                              TypeOfSiding.NOT_SURE])
    def test_type_of_siding(self, type_of_siding):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        type_of_siding_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE)\
            .press_next().select(TypeOfProject.REPLACE).press_next()

        type_of_siding_page.assert_next_button_disabled()

        type_of_siding_page.select(type_of_siding).press_next()

        AreaPage.assert_at(pytest.driver)

    @pytest.mark.parametrize("area,not_sure,expected", [("1", False, Expected.CORRECT),
                                                        ("999999999", False, Expected.CORRECT),
                                                        ("0", False, Expected.STARTS_WITH_ZERO),
                                                        ("01", False, Expected.STARTS_WITH_ZERO),
                                                        ("1.1", False, Expected.INVALID),
                                                        ("1,1", False, Expected.INVALID),
                                                        ("-1", False, Expected.INVALID),
                                                        ("1aaaa", False, Expected.INVALID),
                                                        ("", True, Expected.CORRECT),
                                                        ("1", True, Expected.CORRECT),
                                                        ("01", True, Expected.STARTS_WITH_ZERO),
                                                        ("1aaaa", True, Expected.INVALID)])
    def test_area(self, area, not_sure, expected):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        area_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE).press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next()

        area_page.assert_next_button_disabled()

        area_page = area_page.enter_area(area, not_sure)
        if expected is Expected.CORRECT:
            area_page.press_next()
            StoriesCountPage.assert_at(pytest.driver)
        elif expected is Expected.STARTS_WITH_ZERO:
            area_page.assert_next_button_disabled()
            area_page.assert_area_starts_with_zero()
        elif expected is Expected.INVALID:
            area_page.assert_next_button_disabled()
            area_page.assert_area_invalid()

    @pytest.mark.parametrize("stories_count,choose_no", [(0, False), (1, False), (2, False), (3, False), (3, True)])
    def test_stories_count(self, stories_count, choose_no):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        stories_count_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE) \
            .press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next()

        stories_count_page.assert_next_button_disabled()

        stories_count_page.select(stories_count)

        if choose_no:
            stories_count_page.press_no()
            SorryPage.assert_at(pytest.driver)
        else:
            stories_count_page.press_next()
            IsHomeownerPage.assert_at(pytest.driver)

    @pytest.mark.parametrize("is_homeowner,choose_no", [(True, False), (False, False), (False, True)])
    def test_is_homeowner(self, is_homeowner, choose_no):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        is_homeowner_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE) \
            .press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1) \
            .press_next().select(1).press_next()

        is_homeowner_page.assert_next_button_disabled()

        is_homeowner_page.select(is_homeowner)

        if choose_no:
            is_homeowner_page.press_no()
            SorryPage.assert_at(pytest.driver)
        else:
            is_homeowner_page.press_next()
            NameEmailPage.assert_at(pytest.driver)

    @pytest.mark.parametrize("full_name,expected", [("a a", Expected.CORRECT), ("a a a", Expected.CORRECT),
                                                    ("a a abc-abc", Expected.CORRECT), ("", Expected.EMPTY),
                                                    ("a ", Expected.INVALID), (" a", Expected.INVALID),
                                                    (". a", Expected.INVALID), ("a !", Expected.INVALID),
                                                    ("1a a", Expected.INVALID), ("a a2", Expected.INVALID),
                                                    ("a", Expected.INCOMPLETE), ("abc", Expected.INCOMPLETE)])
    def test_name(self, full_name, expected):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        name_email_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE).press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next() \
            .select(True).press_next().enter_full_name(full_name).press_next()

        if expected is Expected.CORRECT:
            name_email_page.assert_no_full_name_message()
        elif expected is Expected.EMPTY:
            name_email_page.assert_full_name_empty()
        elif expected is Expected.INCOMPLETE:
            name_email_page.assert_full_name_incomplete()
        elif expected is Expected.INVALID:
            name_email_page.assert_full_name_invalid()

    @pytest.mark.parametrize("email,expected", [("abc@mail.com", Expected.CORRECT),
                                                ("abc-def1@mail.com", Expected.CORRECT),
                                                ("abc.def@mail.com", Expected.CORRECT),
                                                ("abc_def2@mail.com", Expected.CORRECT),
                                                ("abc.def@mail.cc", Expected.CORRECT),
                                                ("abc.def@mail-archive.com", Expected.CORRECT),
                                                ("abc.def@mail3-archive.com", Expected.CORRECT),
                                                (random_email(64, 253), Expected.CORRECT),
                                                ("", Expected.EMPTY),
                                                ("abc-@mail.com", Expected.INVALID),
                                                ("abc..def@mail.com", Expected.INVALID),
                                                (".abc@mail.com", Expected.INVALID),
                                                ("abc.def@mail#archive.com", Expected.INVALID),
                                                ("abc.def@mail", Expected.INVALID),
                                                ("abc.def@mail..com", Expected.INVALID),
                                                (random_email(65, 254), Expected.INVALID)])
    def test_email(self, email, expected):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        name_email_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE).press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next() \
            .select(True).press_next().enter_email(email).press_next()

        if expected is Expected.CORRECT:
            name_email_page.assert_no_email_message()
        elif expected is Expected.EMPTY:
            name_email_page.assert_email_empty()
        elif expected is Expected.INVALID:
            name_email_page.assert_email_invalid()

    @pytest.mark.parametrize("full_name,email,expected_full_name,expected_email",
                             [("a a", "abc@mail.com", Expected.CORRECT, Expected.CORRECT),
                              ("a a", "", Expected.CORRECT, Expected.EMPTY),
                              ("a a", "abc", Expected.CORRECT, Expected.INVALID),
                              ("", "abc@mail.com", Expected.EMPTY, Expected.CORRECT),
                              ("", "", Expected.EMPTY, Expected.EMPTY),
                              ("", "abc", Expected.EMPTY, Expected.INVALID),
                              ("a ", "abc@mail.com", Expected.INVALID, Expected.CORRECT),
                              (" a", "", Expected.INVALID, Expected.EMPTY),
                              ("a ", "abc", Expected.INVALID, Expected.INVALID),
                              ("a", "abc@mail.com", Expected.INCOMPLETE, Expected.CORRECT),
                              ("a", "", Expected.INCOMPLETE, Expected.EMPTY),
                              ("a", "abc", Expected.INCOMPLETE, Expected.INVALID)])
    def test_full_name_email(self, full_name, email, expected_full_name, expected_email):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        name_email_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE).press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next() \
            .select(True).press_next().enter_full_name(full_name).enter_email(email)

        name_email_page.press_next()

        if expected_full_name is Expected.CORRECT and expected_email is Expected.CORRECT:
            PhoneNumberPage.assert_at(pytest.driver)
        else:
            if expected_full_name is Expected.CORRECT:
                name_email_page.assert_no_full_name_message()
            elif expected_full_name is Expected.EMPTY:
                name_email_page.assert_full_name_empty()
            elif expected_full_name is Expected.INCOMPLETE:
                name_email_page.assert_full_name_incomplete()
            elif expected_full_name is Expected.INVALID:
                name_email_page.assert_full_name_invalid()

            if expected_email is Expected.CORRECT:
                name_email_page.assert_no_email_message()
            elif expected_email is Expected.EMPTY:
                name_email_page.assert_email_empty()
            elif expected_email is Expected.INVALID:
                name_email_page.assert_email_invalid()

    @pytest.mark.parametrize("phone_number,expected",
                             [("2234123123", Expected.CORRECT), ("1111111111", Expected.CORRECT),
                              ("", Expected.EMPTY), ("222", Expected.INVALID)])
    def test_phone_number(self, phone_number, expected):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        phone_number_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE) \
            .press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next() \
            .select(True).press_next().enter_full_name("a a").enter_email(random_email(10, 10)) \
            .press_next().enter_phone_number(phone_number)

        phone_number_page.press_next()

        if expected is Expected.CORRECT:
            if ConfirmPhonePage.is_at(pytest.driver):
                ConfirmPhonePage.assert_at(pytest.driver)
            elif PhoneEmailAlreadyExistPage.is_at(pytest.driver):
                PhoneEmailAlreadyExistPage.assert_at(pytest.driver)
            else:
                assert False, "Expected to reach Confirm Phone Page or Phone Email Already Exist Page"
        elif expected is Expected.EMPTY:
            phone_number_page.assert_phone_number_empty()
        elif expected is Expected.INVALID:
            phone_number_page.assert_phone_number_invalid()

    @pytest.mark.parametrize("change,phone_number,email,expected_phone,expected_email",
                             [(False, "", "", Expected.ALREADY_EXISTS, Expected.ALREADY_EXISTS),
                              (True, "", "abc@mail.com", Expected.EMPTY, Expected.CORRECT),
                              (True, "", "", Expected.EMPTY, Expected.EMPTY),
                              (True, "", "abc", Expected.EMPTY, Expected.INVALID),
                              (True, "", "rand", Expected.EMPTY, Expected.CORRECT),
                              (True, "222", "abc@mail.com", Expected.INVALID, Expected.CORRECT),
                              (True, "222", "", Expected.INVALID, Expected.EMPTY),
                              (True, "222", "abc", Expected.INVALID, Expected.INVALID),
                              (True, "222", "rand", Expected.INVALID, Expected.CORRECT),
                              (True, "rand", "rand", Expected.CORRECT, Expected.CORRECT),
                              (True, "rand", "", Expected.CORRECT, Expected.EMPTY),
                              (True, "rand", "abc", Expected.CORRECT, Expected.INVALID),
                              (True, "a", "abc@mail.com", Expected.INCOMPLETE, Expected.CORRECT)])
    def test_phone_email_already_exist(self, change, phone_number, email, expected_phone, expected_email):
        siding_home_page = SidingHomePage(pytest.driver)
        # Reaching destination page
        phone_email_already_exist_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE) \
            .press_next().select(TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next() \
            .select(True).press_next().enter_full_name("a a").enter_email("abc@abc.abc") \
            .press_next().enter_phone_number("2234123123").press_next()

        # If phone/email combination doesn't exist - creating it
        if not PhoneEmailAlreadyExistPage.is_at(pytest.driver):
            # If at Confirm Phone Page - confirming phone/email combination
            if ConfirmPhonePage.is_at(pytest.driver):
                phone_email_already_exist_page.press_next()
            # Restarting the browser and reaching Phone/Email Already Exist Page
            pytest.driver.get("https://hb-eta.stage.sirenltd.dev/siding")
            siding_home_page = SidingHomePage(pytest.driver)
            phone_email_already_exist_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE) \
                .press_next().select(TypeOfProject.REPLACE) \
                .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next()\
                .select(True).press_next().enter_full_name("a a").enter_email("abc@abc.abc") \
                .press_next().enter_phone_number("2234123123").press_next()

        if change:
            if phone_number == "rand":
                phone_email_already_exist_page.enter_phone_number(random_phone_number())
            else:
                phone_email_already_exist_page.enter_phone_number(phone_number)

            if email == "rand":
                phone_email_already_exist_page.enter_email(random_email(10, 10))
            else:
                phone_email_already_exist_page.enter_email(email)

        phone_email_already_exist_page.press_next()

        if expected_phone is Expected.CORRECT and expected_email is Expected.CORRECT:
            # If our randomly generated phone/email already exist in a database - rewriting it
            while not phone_email_already_exist_page.no_phone_message() \
                    and not phone_email_already_exist_page.no_email_message():
                phone_email_already_exist_page.enter_phone_number(random_phone_number())
                phone_email_already_exist_page.enter_email(random_email(10, 10))
                phone_email_already_exist_page.press_next()
            if ThankYouPage.is_at(pytest.driver):
                ThankYouPage.assert_at(pytest.driver)
            elif ConfirmPhonePage.is_at(pytest.driver):
                ConfirmPhonePage.assert_at(pytest.driver)
        else:
            if expected_phone is Expected.CORRECT:
                phone_email_already_exist_page.assert_no_phone_message()
            elif expected_phone is Expected.ALREADY_EXISTS:
                phone_email_already_exist_page.assert_phone_number_exists()
            elif expected_phone is Expected.EMPTY:
                phone_email_already_exist_page.assert_phone_number_empty()
            elif expected_phone is Expected.INVALID:
                phone_email_already_exist_page.assert_phone_number_invalid()

            if expected_email is Expected.CORRECT:
                phone_email_already_exist_page.assert_no_email_message()
            elif expected_email is Expected.ALREADY_EXISTS:
                phone_email_already_exist_page.assert_email_exists()
            elif expected_email is Expected.EMPTY:
                phone_email_already_exist_page.assert_email_empty()
            elif expected_email is Expected.INVALID:
                phone_email_already_exist_page.assert_email_invalid()

    @pytest.mark.parametrize("edit,phone_number,expected", [(True, "rand", Expected.CORRECT),
                                                            (True, "1111111111", Expected.CORRECT),
                                                            (True, "", Expected.EMPTY),
                                                            (True, "222", Expected.INVALID),
                                                            (False, "", Expected.CORRECT)])
    def test_confirm_phone_number(self, edit, phone_number, expected):
        siding_home_page = SidingHomePage(pytest.driver)
        confirm_phone_page = siding_home_page.enter_zip_code(CORRECT_ZIP_CODE).press_next().select(
            TypeOfProject.REPLACE) \
            .press_next().select(TypeOfSiding.VINYL).press_next().enter_area(1).press_next().select(1).press_next() \
            .select(True).press_next().enter_full_name("a b").enter_email(random_email(10, 10)) \
            .press_next().enter_phone_number("2222222222").press_next()

        # If phone/email combination already exist - rewriting it
        while PhoneEmailAlreadyExistPage.is_at(pytest.driver):
            phone_email_already_exist_page = confirm_phone_page
            phone_email_already_exist_page.enter_email(random_email(10, 10))
            confirm_phone_page = phone_email_already_exist_page.press_next()

        if edit:
            if phone_number == "rand":
                confirm_phone_page.press_edit().enter_phone_number(random_phone_number())
            else:
                confirm_phone_page.press_edit().enter_phone_number(phone_number)

        confirm_phone_page.press_next()

        if expected is Expected.CORRECT:
            if ThankYouPage.is_at(pytest.driver):
                ThankYouPage.assert_at(pytest.driver)
            elif PhoneEmailAlreadyExistPage.is_at(pytest.driver):
                PhoneEmailAlreadyExistPage.assert_at(pytest.driver)
            else:
                assert False, "Expected to reach Thank You Page or Phone Email Already Exist Page"
        elif expected is Expected.EMPTY:
            confirm_phone_page.assert_phone_number_empty()
        elif expected is Expected.INVALID:
            confirm_phone_page.assert_phone_number_invalid()
