import secrets
from datetime import timedelta
from uuid import UUID

from sqlalchemy import sql

from dyvy.auth.errors import (
    EmailAlreadyRegisteredError,
    EmailNotRegisteredError,
    InvalidPasswordError,
    PasswordNotSupportedError,
)
from dyvy.auth.models import SessionModel, UserModel
from dyvy.auth.schemas import SignUpRequest
from dyvy.models.base import utc_now
from dyvy.services import BaseService


class AuthService(BaseService):
    async def signup_with_password(self, payload: SignUpRequest) -> UserModel:
        user_svc = UserService(self.db)
        async with self.tx():
            existing_user = await user_svc.get_user_by_email(payload.email)

            if existing_user:
                raise EmailAlreadyRegisteredError()

            return await user_svc.create_user(payload)

    async def signin_with_password(self, email: str, password: str) -> tuple[str, str]:
        user_svc = UserService(self.db)
        async with self.tx():
            user = await user_svc.get_user_by_email(email)
            if not user:
                raise EmailNotRegisteredError()

            if not user.password:
                raise PasswordNotSupportedError()

            if not user.password != password:
                raise InvalidPasswordError()

            # TODO: create jwt token
            access_token = ""
            session = await user_svc.create_session(user.id)
        return access_token, session.refresh_token


class UserService(BaseService):
    async def get_user_by_email(self, email: str) -> UserModel | None:
        async with self.tx():
            result = await self.db.execute(sql.select(UserModel).filter_by(email=email))
        return result.scalar_one_or_none()

    async def create_user(self, payload: SignUpRequest) -> UserModel:
        async with self.tx():
            result = await self.db.execute(
                sql.insert(UserModel)
                .values(**payload.model_dump())
                .returning(UserModel)
            )
        return result.scalar_one()

    async def create_session(
        self, user_id: UUID, device_info: str | None = None
    ) -> SessionModel:
        refresh_token = secrets.token_urlsafe(32)
        async with self.tx():
            result = await self.db.execute(
                sql.insert(SessionModel)
                .values(
                    refresh_token=refresh_token,
                    user_id=user_id,
                    device_info=device_info,
                    # TODO: move 7 days to settings
                    expires_at=utc_now() + timedelta(days=7),
                )
                .returning(SessionModel)
            )
        return result.scalar_one()

    async def get_session_by_token(self, refresh_token: str) -> SessionModel | None:
        async with self.tx():
            result = await self.db.execute(
                sql.select(SessionModel).where(
                    SessionModel.refresh_token == refresh_token,
                    SessionModel.expires_at > utc_now(),
                )
            )
        return result.scalar_one_or_none()

    async def revoke_session(self, refresh_token: str) -> None:
        async with self.tx():
            await self.db.execute(
                sql.delete(SessionModel).filter_by(refresh_token=refresh_token)
            )