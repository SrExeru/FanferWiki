from config import JWT_SECRET, JWT_ALGORITHM
from jwt import encode, decode

def encode_jwt(payload: dict[str, str]) -> str:
    return encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def decode_jwt(encoded_jwt: str) -> dict[str, str]:
    return decode(
        encoded_jwt,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM]
    )