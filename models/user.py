from sqlalchemy import Column, Integer, String, Boolean, DateTime

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)

    salt = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)

    active = Column(Boolean, nullable=False, default=True)
    last_login = Column(DateTime, nullable=True)

    def __str__(self):
        return "User({id}) <{email}>".format(self.id, self.email)