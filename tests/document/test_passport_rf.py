import uuid
from datetime import date

import pytest
import allure
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.database.models import User
from traveling_sso.managers import create_passport_rf_new, create_or_update_passport_rf, update_passport_rf
from traveling_sso.shared.schemas.protocol import CreatePassportRfResponseSchema, UpdatePassportRfResponseSchema


@pytest.mark.asyncio
@allure.title("Create new Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation of a new Passport RF document.")
async def test_create_passport_rf_new(session: AsyncSession, user: User, passport_rf):
    passport_instance = await passport_rf

    passport_data = CreatePassportRfResponseSchema(
        series=passport_instance.series,
        number=passport_instance.number,
        first_name=passport_instance.first_name,
        last_name=passport_instance.last_name,
        second_name=passport_instance.second_name,
        birth_date=passport_instance.birth_date,
        birth_place=passport_instance.birth_place,
        gender=passport_instance.gender,
        issued_by=passport_instance.issued_by,
        division_code=passport_instance.division_code,
        issue_date=passport_instance.issue_date,
        registration_address=passport_instance.registration_address
    )

    passport = await create_passport_rf_new(session=session, passport_data=passport_data, user_id=str(user.id))

    assert passport.series == passport_data.series
    assert passport.number == passport_data.number
    assert passport.first_name == passport_data.first_name
    assert passport.last_name == passport_data.last_name
    assert passport.is_verified is True


@pytest.mark.asyncio
@allure.title("Create or update Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation or update of a Passport RF document.")
async def test_create_or_update_passport_rf(session: AsyncSession, user: User, passport_rf):
    passport_instance = await passport_rf

    passport_data = CreatePassportRfResponseSchema(
        series=passport_instance.series,
        number=passport_instance.number,
        first_name=passport_instance.first_name,
        last_name=passport_instance.last_name,
        second_name=passport_instance.second_name,
        birth_date=passport_instance.birth_date,
        birth_place=passport_instance.birth_place,
        gender=passport_instance.gender,
        issued_by=passport_instance.issued_by,
        division_code=passport_instance.division_code,
        issue_date=passport_instance.issue_date,
        registration_address=passport_instance.registration_address
    )

    passport = await create_or_update_passport_rf(session=session, passport_data=passport_data, user_id=str(user.id))

    assert passport.series == passport_data.series
    assert passport.number == passport_data.number
    assert passport.first_name == passport_data.first_name
    assert passport.last_name == passport_data.last_name
    assert passport.is_verified is False


@pytest.mark.asyncio
@allure.title("Update Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the update of a Passport RF document.")
async def test_update_passport_rf(session: AsyncSession, user: User, passport_rf):
    passport_instance = await passport_rf  # await the async fixture to get the actual instance

    create_passport_data = CreatePassportRfResponseSchema(
        series=passport_instance.series,
        number=passport_instance.number,
        first_name=passport_instance.first_name,
        last_name=passport_instance.last_name,
        second_name=passport_instance.second_name,
        birth_date=passport_instance.birth_date,
        birth_place=passport_instance.birth_place,
        gender=passport_instance.gender,
        issued_by=passport_instance.issued_by,
        division_code=passport_instance.division_code,
        issue_date=passport_instance.issue_date,
        registration_address=passport_instance.registration_address
    )
    await create_passport_rf_new(session=session, passport_data=create_passport_data, user_id=str(user.id))

    update_passport_data = UpdatePassportRfResponseSchema(
        first_name="Jane",
        last_name="Doe"
    )

    passport = await update_passport_rf(session=session, user_id=str(user.id), passport_data=update_passport_data)

    assert passport.first_name == update_passport_data.first_name
    assert passport.last_name == update_passport_data.last_name
