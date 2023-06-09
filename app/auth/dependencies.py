from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from jose import ExpiredSignatureError, JWTError, jwt

from app.auth.dao import UserDAO
from app.auth.models import User
from app.config import settings
from app.exceptions import (
    IncorrentTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)


def get_token(request: Request):
	token = request.cookies.get("booking_access_token")
	if not token:
		raise TokenAbsentException(status_code=status.HTTP_401_UNAUTHORIZED,
								detail="Токен отсутствует",)
	return token


async def get_current_user(token: str = Depends(get_token)):
	try:
		payload = jwt.decode(
			token, settings.SECRET_KEY, settings.ALGORITHM
		)
	except ExpiredSignatureError:
		raise TokenExpiredException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок действия токена истек",)
	except JWTError:
		raise IncorrentTokenFormatException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена",)

	user_id: str = payload.get("sub")
	if not user_id:
		raise UserIsNotPresentException(status_code=status.HTTP_401_UNAUTHORIZED,)
	user = await UserDAO.find_by_id(int(user_id))
	if not user:
		raise UserIsNotPresentException(status_code=status.HTTP_401_UNAUTHORIZED,)
	return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
	# if current_user.role != "admin":
	# 	raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
	return current_user
