from sqladmin import ModelView

from app.auth.models import User
from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email] + [User.booking]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [Booking.user]
    name = "Бронь"
    name_plural = "Бронь"
    icon = "fa-solid fa-book"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.room]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
