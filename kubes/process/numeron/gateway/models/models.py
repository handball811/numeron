from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType
from .connection_base import mysql_handler_factory
import uuid

db_handler = mysql_handler_factory()

Base = declarative_base()
Base.query = db_handler.get_session().query_property()


class Service(Base):
	__tablename__ = "service"
	uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
	name = Column(String(64), unique=True)

class User(Base):
	__tablename__ = "user"
	__table_args__ = (UniqueConstraint("service_id","service_user_id"),{})
	uuid = Column(String(36), primary_key=True, default=uuid.uuid4)
	name = Column(String(64))
	service_id = Column(String(36), ForeignKey("service.uuid"))
	service = relationship(
		Service,
		backref=backref("users",
						uselist=True,
						cascade="delete,all"))
	service_user_id = Column(String(128))
	create_at = Column(DateTime, default=func.now())