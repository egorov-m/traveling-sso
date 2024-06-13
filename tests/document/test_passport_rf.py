import uuid
from datetime import date

import pytest
import allure
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.database.models import PassportRf, User
from traveling_sso.managers import create_passport_rf_new, create_or_update_passport_rf, update_passport_rf
from traveling_sso.shared.schemas.protocol import CreatePassportRfResponseSchema, UpdatePassportRfResponseSchema


@pytest.mark.asyncio
@allure.title("Create new Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation of a new Passport RF document.")
async def test_create_passport_rf_new(session: AsyncSession, user: User):
    passport_data = CreatePassportRfResponseSchema(
        series="1234",
        number="567890",
        first_name="John",
        last_name="Doe",
        second_name="Smith",
        birth_date=date(1990, 1, 1),
        birth_place="Moscow",
        gender="М",
        issued_by="Government",
        division_code="123-456",
        issue_date=date(2010, 1, 1),
        registration_address="Moscow, Red Square"
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
async def test_create_or_update_passport_rf(session: AsyncSession, user: User):
    passport_data = CreatePassportRfResponseSchema(
        series="1234",
        number="567890",
        first_name="John",
        last_name="Doe",
        second_name="Smith",
        birth_date=date(1990, 1, 1),
        birth_place="Moscow",
        gender="М",
        issued_by="Government",
        division_code="123-456",
        issue_date=date(2010, 1, 1),
        registration_address="Moscow, Red Square"
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
async def test_update_passport_rf(session: AsyncSession, user: User):
    create_passport_data = CreatePassportRfResponseSchema(
        series="1234",
        number="567890",
        first_name="John",
        last_name="Doe",
        second_name="Smith",
        birth_date=date(1990, 1, 1),
        birth_place="Moscow",
        gender="М",
        issued_by="Government",
        division_code="123-456",
        issue_date=date(2010, 1, 1),
        registration_address="Moscow, Red Square"
    )
    await create_passport_rf_new(session=session, passport_data=create_passport_data, user_id=str(user.id))

    update_passport_data = UpdatePassportRfResponseSchema(
        first_name="Jane",
        last_name="Doe"
    )

    passport = await update_passport_rf(session=session, user_id=str(user.id), passport_data=update_passport_data)

    assert passport.first_name == update_passport_data.first_name