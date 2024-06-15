import allure
import pytest
from datetime import date

from pydantic import ValidationError

from traveling_sso.shared.schemas.protocol import CreatePassportRfResponseSchema


@allure.title("Valid Passport Data")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation of a passport with valid data.")
def test_valid_passport():
    passport_data = {
        "series": "1234",
        "number": "123456",
        "first_name": "Иван",
        "last_name": "Иванов",
        "second_name": "Иванович",
        "birth_date": date(1990, 1, 1),
        "birth_place": "Москва",
        "gender": "М",
        "issued_by": "ОВД Москвы",
        "division_code": "123-456",
        "issue_date": date(2010, 1, 1),
        "registration_address": "Москва, ул. Пушкина, д. 1"
    }

    passport = CreatePassportRfResponseSchema(**passport_data)
    assert passport.series == "1234"
    assert passport.number == "123456"
    assert passport.first_name == "Иван"
    assert passport.last_name == "Иванов"
    assert passport.second_name == "Иванович"
    assert passport.birth_date == date(1990, 1, 1)
    assert passport.birth_place == "Москва"
    assert passport.gender == "М"
    assert passport.issued_by == "ОВД Москвы"
    assert passport.division_code == "123-456"
    assert passport.issue_date == date(2010, 1, 1)
    assert passport.registration_address == "Москва, ул. Пушкина, д. 1"


@allure.title("Missing Optional Field")
@allure.feature("Passport Management")
@allure.description("This test verifies that a passport can be created without the optional field 'second_name'.")
def test_missing_optional_field():
    passport_data = {
        "series": "1234",
        "number": "123456",
        "first_name": "Иван",
        "last_name": "Иванов",
        "birth_date": date(1990, 1, 1),
        "birth_place": "Москва",
        "gender": "М",
        "issued_by": "ОВД Москвы",
        "division_code": "123-456",
        "issue_date": date(2010, 1, 1),
        "registration_address": "Москва, ул. Пушкина, д. 1"
    }

    passport = CreatePassportRfResponseSchema(**passport_data)
    assert passport.second_name is None


@allure.title("Invalid Series Length")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the series length is invalid.")
def test_invalid_series_length():
    with pytest.raises(ValidationError):
        CreatePassportRfResponseSchema(
            series="12345",
            number="123456",
            first_name="Иван",
            last_name="Иванов",
            birth_date=date(1990, 1, 1),
            birth_place="Москва",
            gender="М",
            issued_by="ОВД Москвы",
            division_code="123-456",
            issue_date=date(2010, 1, 1),
            registration_address="Москва, ул. Пушкина, д. 1"
        )


@allure.title("Invalid Number Length")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the number length is invalid.")
def test_invalid_number_length():
    with pytest.raises(ValidationError):
        CreatePassportRfResponseSchema(
            series="1234",
            number="12345",
            first_name="Иван",
            last_name="Иванов",
            birth_date=date(1990, 1, 1),
            birth_place="Москва",
            gender="М",
            issued_by="ОВД Москвы",
            division_code="123-456",
            issue_date=date(2010, 1, 1),
            registration_address="Москва, ул. Пушкина, д. 1"
        )


@allure.title("Invalid Gender Value")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the gender value is invalid.")
def test_invalid_gender():
    with pytest.raises(ValidationError):
        CreatePassportRfResponseSchema(
            series="1234",
            number="123456",
            first_name="Иван",
            last_name="Иванов",
            birth_date=date(1990, 1, 1),
            birth_place="Москва",
            gender="X",
            issued_by="ОВД Москвы",
            division_code="123-456",
            issue_date=date(2010, 1, 1),
            registration_address="Москва, ул. Пушкина, д. 1"
        )


@allure.title("Invalid Birth Date Format")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the birth date format is invalid.")
def test_invalid_birth_date():
    with pytest.raises(ValidationError):
        CreatePassportRfResponseSchema(
            series="1234",
            number="123456",
            first_name="Иван",
            last_name="Иванов",
            birth_date="invalid-date",
            birth_place="Москва",
            gender="М",
            issued_by="ОВД Москвы",
            division_code="123-456",
            issue_date=date(2010, 1, 1),
            registration_address="Москва, ул. Пушкина, д. 1"
        )


@allure.title("Invalid Issue Date Format")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the issue date format is invalid.")
def test_invalid_issue_date():
    with pytest.raises(ValidationError):
        CreatePassportRfResponseSchema(
            series="1234",
            number="123456",
            first_name="Иван",
            last_name="Иванов",
            birth_date=date(1990, 1, 1),
            birth_place="Москва",
            gender="М",
            issued_by="ОВД Москвы",
            division_code="123-456",
            issue_date="invalid-date",
            registration_address="Москва, ул. Пушкина, д. 1"
        )