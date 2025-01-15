import base64
import secrets
from collections.abc import AsyncGenerator
from datetime import timedelta
from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import sql
from sqlalchemy.ext.asyncio import AsyncSession

from dyvy.auth.models import SessionModel, UserModel
from dyvy.conf import settings
from dyvy.models.base import utc_now


@pytest.fixture
async def user_session(
    db_session: AsyncSession, alice: UserModel
) -> AsyncGenerator[SessionModel]:
    session = SessionModel()
    async with db_session.begin():
        result = await db_session.execute(
            sql.insert(SessionModel)
            .values(
                user_id=alice.id,
                refresh_token=secrets.token_bytes(64),
                device_info="Test Device",
                ip_address="127.0.0.1",
                expires_at=utc_now()
                + timedelta(minutes=settings.JWT.access_token_expire_minutes),
            )
            .returning(SessionModel)
        )
        await db_session.commit()
        session = result.scalar_one()
    yield session

    async with db_session.begin():
        await db_session.execute(sql.delete(SessionModel).filter_by(id=session.id))


async def test_signup_success(client: TestClient) -> None:
    response = client.post(
        "/auth/signup",
        json={
            "email": "alice.testcase@example.com",
            "password": "password123",
            "username": "alice.testcase",
            "fullname": "Alice Testcase",
        },
    )

    assert response.status_code == 201, response.json()
    data = response.json()
    assert data == {
        "id": ANY,
        "email": "alice.testcase@example.com",
        "username": "alice.testcase",
        "fullname": "Alice Testcase",
    }


async def test_signup_email_already_exists(
    alice: UserModel, client: TestClient
) -> None:
    response = client.post(
        "/auth/signup",
        json={
            "email": "alice@example.com",
            "password": "password123",
            "username": "bob.testcase",
            "fullname": "Bob Testcase",
        },
    )

    assert response.status_code == 409, response.json()
    assert response.json() == {"detail": "Email already registered"}


async def test_signin_success(client: TestClient, alice: UserModel) -> None:
    response = client.post(
        "/auth/signin", json={"email": "alice@example.com", "password": "password123"}
    )

    assert response.status_code == 200, response.json()
    data = response.json()
    assert "token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

    cookies = response.cookies
    assert "refresh_token" in cookies
    assert "HttpOnly" in response.headers["Set-Cookie"]


async def test_signin_invalid_credentials(client: TestClient, alice: UserModel) -> None:
    response = client.post(
        "/auth/signin",
        json={"email": "alice@example.com", "password": "wrong_password"},
    )

    assert response.status_code == 401, response.json()
    assert response.json() == {"detail": "Incorrect email or password"}
    assert "WWW-Authenticate" in response.headers


async def test_refresh_token(client: TestClient, user_session: SessionModel) -> None:
    response = client.post(
        "/auth/refresh-token",
        json={
            "token": user_session.refresh_token,
        },
    )

    assert response.status_code == 200, response.json()
    data = response.json()
    assert "token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


async def test_refresh_token_invalid(client: TestClient) -> None:
    response = client.post(
        "/auth/refresh-token",
        json={
            "token": base64.urlsafe_b64encode(secrets.token_bytes(64)).decode("utf-8"),
        },
    )

    assert response.status_code == 401, response.json()
    assert response.json() == {"detail": "Invalid or expired refresh token"}


async def test_success_signout(client: TestClient, user_session: SessionModel) -> None:
    response = client.post(
        "/auth/signout",
        json={
            "token": user_session.refresh_token,
        },
    )

    assert response.status_code == 204