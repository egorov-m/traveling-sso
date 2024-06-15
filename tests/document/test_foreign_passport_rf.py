import uuid
from datetime import date

import pytest
import allure
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.database.models import User
from traveling_sso.managers.documents import create_foreign_passport_rf_new, create_or_update_foreign_passport_rf, \
    update_foreign_passport_rf
from traveling_sso.shared.schemas.protocol import CreatePassportRfResponseSchema, UpdatePassportRfResponseSchema, \
    CreateForeignPassportRfResponseSchema, UpdateForeignPassportRfResponseSchema


@pytest.mark.asyncio
@allure.title("Create new Foreign Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation of a new Foreign Passport RF document.")
async def test_create_foreign_passport_rf_new(session: AsyncSession, user: User):
    passport_data = CreateForeignPassportRfResponseSchema(
        number="A12345678",
        first_name="John",
        first_name_latin="John",
        last_name="Doe",
        last_name_latin="Doe",
        second_name="Smith",
        citizenship="Russia",
        citizenship_latin="Russia",
        birth_date=date(1990, 1, 1),
        birth_place="Moscow",
        birth_place_latin="Moscow",
        gender="М",
        issued_by="Government",
        issue_date=date(2010, 1, 1),
        expiry_date=date(2020, 1, 1)
    )

    passport = await create_foreign_passport_rf_new(session=session, passport_data=passport_data, user_id=str(user.id))

    assert passport.number == passport_data.number
    assert passport.first_name == passport_data.first_name
    assert passport.last_name == passport_data.last_name
    assert passport.is_verified is True


@pytest.mark.asyncio
@allure.title("Create or update Foreign Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation or update of a Foreign Passport RF document.")
async def test_create_or_update_foreign_passport_rf(session: AsyncSession, user: User):
    passport_data = CreateForeignPassportRfResponseSchema(
        number="A12345678",
        first_name="John",
        first_name_latin="John",
        last_name="Doe",
        last_name_latin="Doe",
        second_name="Smith",
        citizenship="Russia",
        citizenship_latin="Russia",
        birth_date=date(1990, 1, 1),
        birth_place="Moscow",
        birth_place_latin="Moscow",
        gender="М",
        issued_by="Government",
        issue_date=date(2010, 1, 1),
        expiry_date=date(2020, 1, 1)
    )

    passport = await create_or_update_foreign_passport_rf(session=session, passport_data=passport_data,
                                                          user_id=str(user.id))

    assert passport.number == passport_data.number
    assert passport.first_name == passport_data.first_name
    assert passport.last_name == passport_data.last_name
    assert passport.is_verified is False


@pytest.mark.asyncio
@allure.title("Update Foreign Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the update of a Foreign Passport RF document.")
async def test_update_foreign_passport_rf(session: AsyncSession, user: User):
    create_passport_data = CreateForeignPassportRfResponseSchema(
        number="1234567890",
        first_name="John",
        first_name_latin="John",
        last_name="Doe",
        last_name_latin="Doe",
        second_name="Smith",
        citizenship="Russia",
        citizenship_latin="Russia",
        birth_date=date(1990, 1, 1),
        birth_place="Moscow",
        birth_place_latin="Moscow",
        gender="М",
        issued_by="Government",
        issue_date=date(2010, 1, 1),
        expiry_date=date(2020, 1, 1)
    )
    await create_foreign_passport_rf_new(session=session, passport_data=create_passport_data, user_id=str(user.id))

    update_passport_data = UpdateForeignPassportRfResponseSchema(
        first_name="Jane",
        last_name="Doe"
    )

    passport = await update_foreign_passport_rf(session=session, user_id=str(user.id), passport_data=update_passport_data)

    assert passport.first_name == update_passport_data.first_name
    assert passport.last_name == update_passport_data.last_name