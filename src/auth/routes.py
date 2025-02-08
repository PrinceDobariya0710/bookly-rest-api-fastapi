from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel, UserLoginModel, UserModel
from src.auth.service import UserService
from src.db.main import get_session
from src.auth.utils import create_access_token, decode_token, verify_password
from datetime import timedelta, datetime
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.constants import ALLOWED_ROLES

REFRESH_TOKEN_EXPIRY = 2

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=ALLOWED_ROLES)

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
                    'user_uid' : str(user.uid),
                    'role' : user.role
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

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(
            content={
                "access_token" : new_access_token
            },
            status_code=status.HTTP_202_ACCEPTED
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or Expired token")

@auth_router.get('/me')
async def get_curr_user(user = Depends(get_current_user), _:bool=Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )