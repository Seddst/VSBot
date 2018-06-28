from telegram import Update, Bot

# from core.texts import *
from core.texts import (
    MSG_USER_UNKNOWN, MSG_NEW_GROUP_ADMIN, MSG_DEL_GROUP_ADMIN,
    MSG_NEW_GROUP_ADMIN_EXISTS, MSG_DEL_GROUP_ADMIN_NOT_EXIST,
    MSG_LIST_ADMINS_HEADER, MSG_LIST_ADMINS_FORMAT,
    MSG_EMPTY, MSG_LIST_ADMINS_USER_FORMAT,
    )
from core.types import User, Admin, admin_allowed, user_allowed
from core.utils import send_async


@admin_allowed()
def set_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    msg = msg.replace('@', '')
    if msg != '':
        user = session.query(User).filter_by(username=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            adm = session.query(Admin).filter_by(user_id=user.id,
                                                 admin_group=update.message.chat.id).first()

            if adm is None:
                new_group_admin = Admin(user_id=user.id,
                                        admin_type=Admin.GROUP.value,
                                        admin_group=update.message.chat.id)

                session.add(new_group_admin)
                session.commit()
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_NEW_GROUP_ADMIN.format(user.username))

            else:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_NEW_GROUP_ADMIN_EXISTS.format(user.username))


# i believe del_adm is only for squad admin or "group admin" delete if that is the case'


def del_adm(bot, chat_id, user, session):
    adm = session.query(Admin).filter_by(user_id=user.id,
                                         admin_group=chat_id).first()

    if adm is None:
        send_async(bot,
                   chat_id=chat_id,
                   text=MSG_DEL_GROUP_ADMIN_NOT_EXIST.format(user.username))

    else:
        session.delete(adm)
        session.commit()
        send_async(bot,
                   chat_id=chat_id,
                   text=MSG_DEL_GROUP_ADMIN.format(user.username))


@admin_allowed()
def del_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    if msg.find('@') != -1:
        msg = msg.replace('@', '')
        if msg != '':
            user = session.query(User).filter_by(username=msg).first()
            if user is None:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_USER_UNKNOWN)

            else:
                del_adm(bot, update.message.chat.id, user, session)
    else:
        user = session.query(User).filter_by(id=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            del_adm(bot, update.message.chat.id, user, session)


@admin_allowed()
def list_admins(bot: Bot, update: Update, session):
    admins = session.query(Admin).filter(Admin.admin_group == update.message.chat.id).all()
    users = []
    for admin_user in admins:
        users.append(session.query(User).filter_by(id=admin_user.user_id).first())
    msg = MSG_LIST_ADMINS_HEADER
    for user in users:
        msg += MSG_LIST_ADMINS_FORMAT.format(user.id,
                                             user.username,
                                             user.first_name,
                                             user.last_name)

    send_async(bot, chat_id=update.message.chat.id, text=msg)


@user_allowed
def admins_for_users(bot: Bot, update: Update, session):
    admins = session.query(Admin).filter(Admin.admin_group == update.message.chat.id).all()
    users = []
    for admin_user in admins:
        users.append(session.query(User).filter_by(id=admin_user.user_id).first())
    msg = MSG_LIST_ADMINS_HEADER
    if users is None:
        msg += MSG_EMPTY
    else:
        for user in users:
            msg += MSG_LIST_ADMINS_USER_FORMAT.format(user.username or '',
                                                      user.first_name or '',
                                                      user.last_name or '')

    send_async(bot, chat_id=update.message.chat.id, text=msg)
