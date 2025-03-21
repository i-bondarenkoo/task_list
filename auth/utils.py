import jwt
from database import auth_jwt
import bcrypt
from datetime import timedelta, datetime


# функция создания токена
def encode_jwt(
    # полезная нагрузка, данные которые будут зашифрованы в токене
    # например имя пользователя и почта
    payload: dict,
    # путь к закрытому ключу
    private_key: str = auth_jwt.private_key_path.read_text(),
    # алгоритм шифрования
    algorithm: str = auth_jwt.algorithm,
    # время жизни токена
    expire_minutes: int = auth_jwt.access_token_exp_minutes,
    # время истечения токена
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    # токен подписывается закрытым ключом
    # и далее отправляется клиенту
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


# проверка токена
def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


# хэшируем пароль
# bcrypt хэширует пароль и добавляет соль
# этот хэш сохраняется в бд (словаре)
def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


# простая проверка
def validate_password(
    # пароль который введет пользователь
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
