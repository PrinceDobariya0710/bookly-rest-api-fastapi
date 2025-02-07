from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel, UserLoginModel, UserModel
from src.auth.service import UserService
from src.db.main import get_session
from src.auth.utils import create_access_token, decode_token, verify_password
from datetime import timedelta

REFRESH_TOKEN_EXPIRY = 2

auth_router = APIRouter()
user_service = UserService()

@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,
                            session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email=email,session=session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email : {email} already exists")
    new_user = await user_service.create_user(user_data,session)
    return new_user

@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession=Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email=email,session=session)
    if user:
        password_valid = verify_password(password,user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email' : email,
                    'user_uid' : str(user.uid)
                }
            )
            refresh_token = create_access_token(
                user_data={
                    'email' : email,
                    'user_uid' : str(user.uid)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )
            return JSONResponse(
                content={
                    "message" : "Login Successful",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "user" : {
                        "email" : user.email,
                        "uid" : str(user.uid)
                    }
                }
            )
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Email or Password")
