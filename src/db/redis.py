from redis import asyncio as aioredis3
from src.config import Config

JTI_EXPIRE =3600

token_blocklist = aioredis3.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRE
    )

async def token_in_blocklist(jti:str)->bool:
    jti = await token_blocklist.get(jti)
    return jti is not None