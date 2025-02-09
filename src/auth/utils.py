from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
import jwt
import uuid
from src.config import Config
import logging

password_context = CryptContext(
    schemes=['bcrypt']
)
ACCESS_TOKEN_EXPIRY = 60

def generate_password_hash(password:str)->str:
    hash_pswd = password_context.hash(password)
    return hash_pswd

def verify_password(password:str, hash:str)->bool:
    return password_context.verify(secret=password,hash=hash)

def create_access_token(user_data: dict,expiry: timedelta = None, refresh: bool=False):
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_token(token:str)->dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET_KEY, salt="email-configuration"
)
def create_url_safe_token(data: dict) -> str:
    """
    Create a URL-safe token with an expiration time.
    """
    return serializer.dumps(data)

def decode_url_safe_token(token: str, max_age=3600) -> dict:
    """
    Decode a URL-safe token and check for expiration.
    """
    try:
        # Deserialize the token and check if it's expired
        data = serializer.loads(token, max_age=max_age)
        return data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")