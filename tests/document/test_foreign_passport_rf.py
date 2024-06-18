import pytest
import allure
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.database.models import User
from traveling_sso.managers.documents import create_foreign_passport_rf_new, create_or_update_foreign_passport_rf, \
    update_foreign_passport_rf, CreateForeignPassportRfResponseSchema, UpdateForeignPassportRfResponseSchema


@pytest.mark.asyncio
@allure.title("Create new Foreign Passport RF")
@allure.feature("Passport Management")
@allure.description("This test verifies the creation of a new Foreign Passport RF document.")
async def test_create_foreign_passport_rf_new(session: AsyncSession, user: User, foreign_passport_rf):
    passport_instance = await foreign_passport_rf

    passport_data = CreateForeignPassportRfResponseSchema(
        number=passport_instance.number,
        first_name=passport_instance.first_name,
        first_name_latin=passport_instance.first_name_latin,
        last_name=passport_instance.last_name,
        last_name_latin=passport_instance.last_name_latin,
        second_name=passport_instance.second_name,
        citizenship=passport_instance.citizenship,
        citizenship_latin=passport_instance.citizenship_latin,
        birth_date=passport_instance.birth_date,
        birth_place=passport_instance.birth_place,
        birth_place_latin=passport_instance.birth_place_latin,
        gender=passport_instance.gender,
        issued_by=passport_instance.issued_by,
        issue_date=passport_instance.issue_date,
        expiry_date=passport_instance.expiry_date
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
async def test_create_or_update_foreign_passport_rf(session: AsyncSession, user: User, foreign_passport_rf):
    passport_instance = await foreign_passport_rf

    passport_data = CreateForeignPassportRfResponseSchema(
        number=passport_instance.number,
        first_name=passport_instance.first_name,
        first_name_latin=passport_instance.first_name_latin,
        last_name=passport_instance.last_name,
        last_name_latin=passport_instance.last_name_latin,
        second_name=passport_instance.second_name,
        citizenship=passport_instance.citizenship,
        citizenship_latin=passport_instance.citizenship_latin,
        birth_date=passport_instance.birth_date,
        birth_place=passport_instance.birth_place,
        birth_place_latin=passport_instance.birth_place_latin,
        gender=passport_instance.gender,
        issued_by=passport_instance.issued_by,
        issue_date=passport_instance.issue_date,
        expiry_date=passport_instance.expiry_date
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
async def test_update_foreign_passport_rf(session: AsyncSession, user: User, foreign_passport_rf):
    passport_instance = await foreign_passport_rf

    create_passport_data = CreateForeignPassportRfResponseSchema(
        number=passport_instance.number,
        first_name=passport_instance.first_name,
        first_name_latin=passport_instance.first_name_latin,
        last_name=passport_instance.last_name,
        last_name_latin=passport_instance.last_name_latin,
        second_name=passport_instance.second_name,
        citizenship=passport_instance.citizenship,
        citizenship_latin=passport_instance.citizenship_latin,
        birth_date=passport_instance.birth_date,
        birth_place=passport_instance.birth_place,
        birth_place_latin=passport_instance.birth_place_latin,
        gender=passport_instance.gender,
        issued_by=passport_instance.issued_by,
        issue_date=passport_instance.issue_date,
        expiry_date=passport_instance.expiry_date
    )
    await create_foreign_passport_rf_new(session=session, passport_data=create_passport_data, user_id=str(user.id))

    update_passport_data = UpdateForeignPassportRfResponseSchema(
        first_name="Jane",
        last_name="Doe"
    )

    passport = await update_foreign_passport_rf(session=session, user_id=str(user.id), passport_data=update_passport_data)

    assert passport.first_name == update_passport_data.first_name
    assert passport.last_name == update_passport_data.last_name