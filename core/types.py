# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
import logging

from sqlalchemy import (
    create_engine,
    Column, Integer, DateTime, Boolean, ForeignKey, UnicodeText, BigInteger, Text
)
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

from telegram import Bot

from config import DB

class AdminType(Enum):
    SUPER = 0
    FULL = 1
    GROUP = 2
    
    NOT_ADMIN = 100

class MessageType(Enum):
    TEXT = 0
    VOICE = 1
    DOCUMENT = 2
    STICKER = 3
    CONTACT = 4
    VIDEO = 5
    VIDEO_NOTE = 6
    LOCATION = 7
    AUDIO = 8
    PHOTO = 9


ENGINE = create_engine(DB,
                       echo=False,
                       pool_size=200,
                       max_overflow=50,
                       isolation_level="READ UNCOMMITTED")

# FIX: имена констант(constant names)?
LOGGER = logging.getLogger('sqlalchemy.engine')
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=ENGINE))


class Group(Base):
    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)  # FIX: invalid name
    username = Column(UnicodeText(250))
    title = Column(UnicodeText(250))
    welcome_enabled = Column(Boolean, default=False)
    allow_trigger_all = Column(Boolean, default=False)
    allow_pin_all = Column(Boolean, default=False)
    bot_in_group = Column(Boolean, default=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(UnicodeText(250))
    first_name = Column(UnicodeText(250))
    last_name = Column(UnicodeText(250))
    date_added = Column(DateTime, default=datetime.now())


class WelcomeMsg(Base):
    __tablename__ = 'welcomes'

    chat_id = Column(BigInteger, primary_key=True)
    message = Column(UnicodeText(2500))


class Wellcomed(Base):
    __tablename__ = 'wellcomed'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    chat_id = Column(BigInteger, ForeignKey(WelcomeMsg.chat_id), primary_key=True)


class Trigger(Base):
    __tablename__ = 'triggers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trigger = Column(UnicodeText(2500))
    message = Column(UnicodeText(2500))
    message_type = Column(Integer, default=0)


class Admin(Base):
    __tablename__ = 'admins'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    admin_type = Column(Integer)
    admin_group = Column(BigInteger, primary_key=True, default=0)


class LocalTrigger(Base):
    __tablename__ = 'local_triggers'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    chat_id = Column(BigInteger, ForeignKey(Group.id))
    trigger = Column(UnicodeText(2500))
    message = Column(UnicodeText(2500))
    message_type = Column(Integer, default=0)


class Ban(Base):
    __tablename__ = 'banned_users'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    reason = Column(UnicodeText(2500))
    from_date = Column(DATETIME(fsp=6))
    to_date = Column(DATETIME(fsp=6))


class Log(Base):
    __tablename__ = 'log'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(User.id))
    chat_id = Column(BigInteger)
    date = Column(DATETIME(fsp=6))
    func_name = Column(UnicodeText(2500))
    args = Column(UnicodeText(2500))


class Auth(Base):
    __tablename__ = 'auth'

    id = Column(Text(length=32))
    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)


def check_admin(update, session, adm_type, allowed_types=()):
    allowed = False
    if adm_type == AdminType.NOT_ADMIN:
        allowed = True
    else:
        admins = session.query(Admin).filter_by(user_id= update.message.from_user.id).all()
        for adm in admins:
            if (AdminType(adm.admin_type) in allowed_types or adm.admin_type <= adm_type.value) and \
                    (adm.admin_group in [0, update.message.chat.id] or
                     update.message.chat.id == update.message.from_user.id):
                if adm.admin_group != 0:
                    group = session.query(Group).filter_by(id=adm.admin_group).first()
                    if group and group.bot_in_group:
                        allowed = True
                        break
                else:
                    allowed = True
                    break
    return allowed


def check_ban(update, session):
    ban = session.query(Ban).filter_by(user_id=update.message.from_user.id
                                       if update.message else update.callback_query.from_user.id).first()
    if ban is None or ban.to_date < datetime.now():
        return True
    else:
        return False


def log(session, user_id, chat_id, func_name, args):
    if user_id:
        log_item = Log()
        log_item.date = datetime.now()
        log_item.user_id = user_id
        log_item.chat_id = chat_id
        log_item.func_name = func_name
        log_item.args = args
        session.add(log_item)
        session.commit()


def admin_allowed(adm_type=AdminType.FULL, ban_enable=True, allowed_types=()):
    def decorate(func):
        def wrapper(bot: Bot, update, *args, **kwargs):
            session = Session()
            try:
                allowed = check_admin(update, session, adm_type, allowed_types)
                if ban_enable:
                    allowed &= check_ban(update, session)
                    if allowed:
                        if func. __name__ not in ['manage_all', 'trigger_show', 'user_panel', 'wrapper','welcome']:
                            log(session, update.effective_user.id, update.effective_chat.id, func.__name__,
                                update.message.text if update.message else None)
                        func(bot, update, session, *args, **kwargs)
            except SQLAlchemyError as err:
                bot.logger.error(str(err))
                session.rollback()
        return wrapper
    return decorate


def user_allowed(ban_enable=True):
    if callable(ban_enable):
        return admin_allowed(AdminType.NOT_ADMIN)(ban_enable)
    else:
        def wrap(func):
            return admin_allowed(AdminType.NOT_ADMIN, ban_enable)(func)
    return wrap


Base.metadata.create_all(ENGINE)
