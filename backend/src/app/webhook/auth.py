import dataclasses
import hashlib
import hmac
import json
import logging
import typing
from json import JSONDecodeError
from urllib.parse import parse_qsl, unquote

from fastapi import Depends, Request

from app.config import tgbot_config
from app.schemas.users import UserSchema
from app.services.requests import RequestsService
from app.webhook.dependencies.service import get_services

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TelegramUser:
    """Represents a Telegram user.

    Links:
        https://core.telegram.org/bots/webapps#webappuser
    """

    id: int
    first_name: str
    is_bot: typing.Optional[bool] = None
    last_name: typing.Optional[str] = None
    username: typing.Optional[str] = None
    language_code: typing.Optional[str] = None
    is_premium: typing.Optional[bool] = None
    added_to_attachment_menu: typing.Optional[bool] = None
    allows_write_to_pm: typing.Optional[bool] = None
    photo_url: typing.Optional[str] = None


def generate_secret_key(token: str) -> bytes:
    """Generates a secret key from a Telegram token.

    Links:
        https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

    Args:
        token: Telegram Bot Token

    Returns:
        bytes: secret key
    """
    base = "WebAppData".encode("utf-8")
    token_enc = token.encode("utf-8")
    return hmac.digest(base, token_enc, hashlib.sha256)


class TelegramAuthenticator:
    def __init__(self, secret: bytes):
        self._secret = secret

    @staticmethod
    def _parse_init_data(data: str) -> dict:
        """Convert init_data string into dictionary.

        Args:
            data: the query string passed by the webapp
        """
        if not data:
            raise InvalidInitDataError("Init Data cannot be empty")

        return dict(parse_qsl(data))

    @staticmethod
    def _parse_user_data(data: str) -> dict:
        """Convert user value from WebAppInitData to Python dictionary.

        Links:
            https://core.telegram.org/bots/webapps#webappinitdata

        Raises:
            InvalidInitDataError
        """
        try:
            return json.loads(unquote(data))
        except JSONDecodeError:
            raise InvalidInitDataError("Cannot decode init data")

    def _validate(self, hash_: str, token: str) -> bool:
        """Validates the data received from the Telegram web app, using the method from Telegram documentation.

        Links:
            https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

        Args:
            hash_: hash from init data
            token: init data from webapp

        Returns:
            bool: Validation result
        """
        token_bytes = token.encode("utf-8")
        client_hash = hmac.new(self._secret, token_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(client_hash, hash_)

    def verify_token(self, token: str) -> TelegramUser:
        """Verifies the data using the method from documentation. Returns Telegram user if data is valid.

        Links:
            https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

        Args:
            hash_: hash from init data
            token: init data from webapp

        Returns:
            TelegramUser: Telegram user if token is valid

        Raises:
            InvalidInitDataError: if the token is invalid
        """
        init_data = self._parse_init_data(token)
        token = "\n".join(
            f"{key}={val}" for key, val in sorted(init_data.items(), key=lambda item: item[0]) if key != "hash"
        )
        token = unquote(token)
        hash_ = init_data.get("hash")
        if not hash_:
            raise InvalidInitDataError("Init data does not contain hash")

        hash_ = hash_.strip()

        if not self._validate(hash_, token):
            raise InvalidInitDataError("Invalid token")

        user_data = init_data.get("user")
        if not user_data:
            raise InvalidInitDataError("Init data does not contain user")

        user_data = unquote(user_data)
        user_data = self._parse_user_data(user_data)
        return TelegramUser(**user_data)


class NoInitDataError(Exception):
    pass


class InvalidInitDataError(Exception):
    pass


def get_telegram_authenticator() -> TelegramAuthenticator:
    secret_key = generate_secret_key(tgbot_config.token)
    return TelegramAuthenticator(secret_key)


async def get_twa_user(
    request: Request,
    telegram_authenticator: TelegramAuthenticator = Depends(get_telegram_authenticator),
    services: RequestsService = Depends(get_services),
) -> UserSchema:
    init_data = request.headers.get("initData")

    # DEBUG ONLY
    if not init_data:
        logger.error("Init data is missing")
        if tgbot_config.debug:
            user_db = await services.users.get_user_by_username(tgbot_config.debug_username)
            return UserSchema.model_validate(user_db)
        raise NoInitDataError("Init data is missing")

    user = telegram_authenticator.verify_token(init_data)
    # Register or update user in the database
    db_user = await services.users.get_or_create_user(
        UserSchema(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_bot=user.is_bot,
            language_code=user.language_code,
            is_premium=user.is_premium,
            added_to_attachment_menu=user.added_to_attachment_menu,
            allows_write_to_pm=user.allows_write_to_pm,
            photo_url=user.photo_url,
        )
    )
    logger.info(f"User {db_user.user_id} ({db_user.username or 'No username'}) logged in/registered")

    # TODO: catch WebAppChat
    # Extract WebAppChat info from init data
    # # parse init data
    # init_data = telegram_authenticator._parse_init_data(init_data)
    # logger.info(f"Init data: {init_data}")
    # webapp_chat_info = init_data.get("chat")
    # if webapp_chat_info:
    #     webapp_chat_info = json.loads(webapp_chat_info)
    #     logger.info(f"WebAppChat info: {webapp_chat_info}")
    #     logger.info(f"WebAppChat info: {telegram_authenticator._parse_user_data(webapp_chat_info)}")

    return UserSchema.model_validate(db_user)
