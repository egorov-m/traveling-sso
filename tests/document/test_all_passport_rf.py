from datetime import date

import pytest
import allure
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.database.models import User, PassportRf, ForeignPassportRf
from traveling_sso.managers import get_all_documents_by_user_id, create_passport_rf_new
from traveling_sso.managers.documents import create_foreign_passport_rf_new, get_passport_rf_by_user_id, \
    get_foreign_passport_rf_by_user_id
from traveling_sso.shared.schemas.protocol import CreatePassportRfResponseSchema, CreateForeignPassportRfResponseSchema, \
    PassportRfSchema, ForeignPassportRfSchema


@pytest.fixture
async def passport_rf(session: AsyncSession, user: User) -> PassportRfSchema:
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
    return await create_passport_rf_new(session=session, passport_data=passport_data, user_id=str(user.id))


@pytest.fixture
async def foreign_passport_rf(session: AsyncSession, user: User) -> ForeignPassportRfSchema:
    passport_data = CreateForeignPassportRfResponseSchema(
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
    return await create_foreign_passport_rf_new(session=session, passport_data=passport_data, user_id=str(user.id))


@pytest.mark.asyncio
@allure.title("Get all documents by user ID")
@allure.feature("Passport Management")
@allure.description("This test verifies the retrieval of all documents by user ID.")
async def test_get_all_documents_by_user_id(session: AsyncSession, user: User, passport_rf: PassportRf, foreign_passport_rf: ForeignPassportRf):
    documents = await get_all_documents_by_user_id(session=session, user_id=str(user.id))

    assert documents["passport_rf"] is not None
    assert documents["foreign_passport_rf"] is not None


@pytest.mark.asyncio
@allure.title("Get Passport RF by user ID")
@allure.feature("Passport Management")
@allure.description("This test verifies the retrieval of a Passport RF document by user ID.")
async def test_get_passport_rf_by_user_id(session: AsyncSession, user: User, passport_rf: PassportRf):
    passport = await get_passport_rf_by_user_id(session=session, user_id=str(user.id))

    assert passport.series == passport_rf.series
    assert passport.number == passport_rf.number
    assert passport.first_name == passport_rf.first_name
    assert passport.last_name == passport_rf.last_name


@pytest.mark.asyncio
@allure.title("Get Foreign Passport RF by user ID")
@allure.feature("Passport Management")
@allure.description("This test verifies the retrieval of a Foreign Passport RF document by user ID.")
async def test_get_foreign_passport_rf_by_user_id(session: AsyncSession, user: User, foreign_passport_rf: ForeignPassportRf):
    passport = await get_foreign_passport_rf_by_user_id(session=session, user_id=str(user.id))

    assert passport.number == foreign_passport_rf.number
    assert passport.first_name == foreign_passport_rf.first_name
    assert passport.last_name == foreign_passport_rf.last_name