import allure
import pytest
from datetime import date

from pydantic import ValidationError

from traveling_sso.shared.schemas.protocol import CreatePassportRfResponseSchema


@pytest.mark.asyncio
@allure.title("Valid Passport Data")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation of a passport with valid data.")
async def test_valid_passport(passport_rf):
    passport_instance = await passport_rf

    passport_data = {
        "series": passport_instance.series,
        "number": passport_instance.number,
        "first_name": passport_instance.first_name,
        "last_name": passport_instance.last_name,
        "second_name": passport_instance.second_name,
        "birth_date": passport_instance.birth_date,
        "birth_place": passport_instance.birth_place,
        "gender": passport_instance.gender,
        "issued_by": passport_instance.issued_by,
        "division_code": passport_instance.division_code,
        "issue_date": passport_instance.issue_date,
        "registration_address": passport_instance.registration_address
    }

    passport = CreatePassportRfResponseSchema(**passport_data)
    assert passport.series == passport_instance.series
    assert passport.number == passport_instance.number
    assert passport.first_name == passport_instance.first_name
    assert passport.last_name == passport_instance.last_name
    assert passport.second_name == passport_instance.second_name
    assert passport.birth_date == passport_instance.birth_date
    assert passport.birth_place == passport_instance.birth_place
    assert passport.gender == passport_instance.gender
    assert passport.issued_by == passport_instance.issued_by
    assert passport.division_code == passport_instance.division_code
    assert passport.issue_date == passport_instance.issue_date
    assert passport.registration_address == passport_instance.registration_address


@pytest.mark.asyncio
@allure.title("Missing Optional Field")
@allure.feature("Passport Management")
@allure.description("This test verifies that a passport can be created without the optional field 'second_name'.")
async def test_missing_optional_field(passport_rf):
    passport_instance = await passport_rf

    passport_data = {
        "series": passport_instance.series,
        "number": passport_instance.number,
        "first_name": passport_instance.first_name,
        "last_name": passport_instance.last_name,
        "birth_date": passport_instance.birth_date,
        "birth_place": passport_instance.birth_place,
        "gender": passport_instance.gender,
        "issued_by": passport_instance.issued_by,
        "division_code": passport_instance.division_code,
        "issue_date": passport_instance.issue_date,
        "registration_address": passport_instance.registration_address
    }

    passport = CreatePassportRfResponseSchema(**passport_data)
    assert passport.second_name is None


@pytest.mark.asyncio
@allure.title("Invalid Series Length")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the series length is invalid.")
async def test_invalid_series_length(passport_rf):
    with pytest.raises(ValidationError):
        passport_instance = await passport_rf

        CreatePassportRfResponseSchema(
            series="12345",
            number=passport_instance.number,
            first_name=passport_instance.first_name,
            last_name=passport_instance.last_name,
            birth_date=passport_instance.birth_date,
            birth_place=passport_instance.birth_place,
            gender=passport_instance.gender,
            issued_by=passport_instance.issued_by,
            division_code=passport_instance.division_code,
            issue_date=passport_instance.issue_date,
            registration_address=passport_instance.registration_address
        )


@pytest.mark.asyncio
@allure.title("Invalid Number Length")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the number length is invalid.")
async def test_invalid_number_length(passport_rf):
    with pytest.raises(ValidationError):
        passport_instance = await passport_rf

        CreatePassportRfResponseSchema(
            series=passport_instance.series,
            number="12345",
            first_name=passport_instance.first_name,
            last_name=passport_instance.last_name,
            birth_date=passport_instance.birth_date,
            birth_place=passport_instance.birth_place,
            gender=passport_instance.gender,
            issued_by=passport_instance.issued_by,
            division_code=passport_instance.division_code,
            issue_date=passport_instance.issue_date,
            registration_address=passport_instance.registration_address
        )


@pytest.mark.asyncio
@allure.title("Invalid Gender Value")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the gender value is invalid.")
async def test_invalid_gender(passport_rf):
    with pytest.raises(ValidationError):
        passport_instance = await passport_rf

        CreatePassportRfResponseSchema(
            series=passport_instance.series,
            number=passport_instance.number,
            first_name=passport_instance.first_name,
            last_name=passport_instance.last_name,
            birth_date=passport_instance.birth_date,
            birth_place=passport_instance.birth_place,
            gender="X",
            issued_by=passport_instance.issued_by,
            division_code=passport_instance.division_code,
            issue_date=passport_instance.issue_date,
            registration_address=passport_instance.registration_address
        )


@pytest.mark.asyncio
@allure.title("Invalid Birth Date Format")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the birth date format is invalid.")
async def test_invalid_birth_date(passport_rf):
    with pytest.raises(ValidationError):
        passport_instance = await passport_rf

        CreatePassportRfResponseSchema(
            series=passport_instance.series,
            number=passport_instance.number,
            first_name=passport_instance.first_name,
            last_name=passport_instance.last_name,
            birth_date="invalid-date",
            birth_place=passport_instance.birth_place,
            gender=passport_instance.gender,
            issued_by=passport_instance.issued_by,
            division_code=passport_instance.division_code,
            issue_date=passport_instance.issue_date,
            registration_address=passport_instance.registration_address
        )


@pytest.mark.asyncio
@allure.title("Invalid Issue Date Format")
@allure.feature("Passport Management")
@allure.description("This test checks for validation error when the issue date format is invalid.")
async def test_invalid_issue_date(passport_rf):
    with pytest.raises(ValidationError):
        passport_instance = await passport_rf

        CreatePassportRfResponseSchema(
            series=passport_instance.series,
            number=passport_instance.number,
            first_name=passport_instance.first_name,
            last_name=passport_instance.last_name,
            birth_date=passport_instance.birth_date,
            birth_place=passport_instance.birth_place,
            gender=passport_instance.gender,
            issued_by=passport_instance.issued_by,
            division_code=passport_instance.division_code,
            issue_date="invalid-date",
            registration_address=passport_instance.registration_address
        )