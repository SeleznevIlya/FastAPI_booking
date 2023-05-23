from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.auth.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.auth.dao import UserDAO
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.schemas import SUserAuth
from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException

router = APIRouter(
	prefix='/auth',
	tags=["Auth & пользователи"]
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
	existing_user = await UserDAO.find_one_or_none(email=user_data.email)
	if existing_user:
		raise UserAlreadyExistsException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует",)
	hashed_password = get_password_hash(user_data.password)
	await UserDAO.add(email= user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
	user = await authenticate_user(user_data.email, user_data.password)
	if not user:
		raise IncorrectEmailOrPasswordException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль",)
	access_token = create_access_token({"sub": str(user.id)})
	response.set_cookie("booking_access_token", access_token, httponly=True)
	return {'success': 'success auth'}


@router.post('/logout')
async def logout_user(response: Response):
	response.delete_cookie("booking_access_token")
	return {"status": "Logout"}


@router.get('/me')
async def read_users_me(current_user: User = Depends(get_current_user)):
	return current_user

