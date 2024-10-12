from urllib.parse import unquote, parse_qsl
import json
import hmac
import hashlib
from json import JSONDecodeError
import dataclasses
import typing
import logging

from fastapi import Request, Depends

from app.config import tgbot_config
from app.infrastructure.database.repo.requests import RequestsRepo
from app.webhook.utils import get_repo

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
    repo: RequestsRepo = Depends(get_repo),
) -> TelegramUser:
    init_data = request.headers.get("initData")
    if not init_data:
        logger.error("Init data is missing")
        raise NoInitDataError("Init data is missing")
    user = telegram_authenticator.verify_token(init_data)
    
    # Register or update user in the database
    db_user = await repo.users.get_or_create_user(
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
    
    logger.info(f"User {db_user.user_id} ({db_user.username or 'No username'}) logged in/registered")
    
    return user
