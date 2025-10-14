from sqlalchemy import create_engine, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
import bcrypt
from datetime import datetime
import json
import os

# 使用 SQLite 避免连接问题
engine = create_engine('sqlite:///restaurant.db')
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)


class Users(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    contact: Mapped[str] = mapped_column(String(50))
    fullAddress: Mapped[str] = mapped_column(String(50))

    role: Mapped["Role"] = relationship("Role")
    reservations = relationship("Reservation", foreign_keys="Reservation.user_id", back_populates="user")
    orders = relationship("Orders", foreign_keys="Orders.user_id", back_populates="user")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    weight: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column()
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    file_name: Mapped[str] = mapped_column(String)


class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    time_start: Mapped[datetime] = mapped_column(DateTime)
    type_table: Mapped[str] = mapped_column(String(20))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship("Users", foreign_keys="Reservation.user_id", back_populates="reservations")


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_list: Mapped[str] = mapped_column(Text)  # 存储 JSON 字符串
    order_time: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship("Users", foreign_keys="Orders.user_id", back_populates="orders")

    def set_order_list(self, order_dict):
        self.order_list = json.dumps(order_dict)

    def get_order_list(self):
        if self.order_list:
            return json.loads(self.order_list)
        return {}


# 创建表
Base.metadata.create_all(engine)