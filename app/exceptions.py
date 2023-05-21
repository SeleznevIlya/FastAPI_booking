from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
	pass


class IncorrectEmailOrPasswordException(HTTPException):
	pass


class TokenExpiredException(HTTPException):
	pass


class TokenAbsentException(HTTPException):
	pass


class IncorrentTokenFormatException(HTTPException):
	pass


class UserIsNotPresentException(HTTPException):
	pass


class RoomCannotBeBooked(HTTPException):
	pass


class DateBookingException(HTTPException):
	pass


class BookingLimitExceededException(HTTPException):
	pass
