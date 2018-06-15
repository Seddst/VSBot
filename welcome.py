from telegram import Update, Bot
from VSBot.core.types import Wellcomed, WelcomeMsg, admin_allowed, Admin, user_allowed
from VSBot.core.template import fill_template
from time import time
from VSBot.core.utils import send_async, add_user, update_group
from VSBot.core.functions.newbies import newbie
from VSBot.core.texts import *
from VSBot.config import Venture_CHAT_ID, ACADEM_CHAT_ID

# Admintype needs to be replaced academ chat too?

last_welcome = 0


@user_allowed(False)
def welcome(bot: Bot, update: Update, session):
    newbie(bot, update)
    global last_welcome
    print('welcome')
    if update.message.chat.type in ['group']:
        group = update_group(update.message.chat, session)
        for new_chat_member in update.message.new_chat_members:
            user = add_user(new_chat_member, session)
            print(user)
            print(update.message.chat.id)
            print(Venture_CHAT_ID == update.message.chat.id)
            if str(update.message.chat.id) == Venture_CHAT_ID or str(update.message.chat.id) == ACADEM_CHAT_ID:
                print('equal')
                if group.welcome_enabled:
                    print('enable_welcome')
                    welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
                    send_async(bot, chat_id=update.message.chat.id, text=fill_template(welcome_msg.message, user))

            else:
                if group.welcome_enabled:
                    welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
                    if welcome_msg is None:
                        welcome_msg = WelcomeMsg(chat_id=group.id, message=MSG_WELCOME_DEFAULT)
                        session.add(welcome_msg)

                    welcomed = session.query(Wellcomed).filter_by(user_id=new_chat_member.id,
                                                                  chat_id=update.message.chat.id).first()
                    if welcomed is None:
                        if time() - last_welcome > 30:
                            send_async(bot, chat_id=update.message.chat.id,
                                       text=fill_template(welcome_msg.message, user))
                            last_welcome = time()
                        welcomed = Wellcomed(user_id=new_chat_member.id, chat_id=update.message.chat.id)
                        session.add(welcomed)
                    session.commit()


@admin_allowed(adm_type=Admin.GROUP)
def set_welcome(bot: Bot, update: Update, session):
    if update.message.chat.type in ['group']:
        group = update_group(update.message.chat, session)
        welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
        if welcome_msg is None:
            welcome_msg = WelcomeMsg(chat_id=group.id, message=update.message.text.split(' ', 1)[1])
        else:
            welcome_msg.message = update.message.text.split(' ', 1)[1]
        session.add(welcome_msg)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_WELCOME_SET)


@admin_allowed(adm_type=Admin.GROUP)
def enable_welcome(bot: Bot, update: Update, session):
    if update.message.chat.type in ['group']:
        group = update_group(update.message.chat, session)
        group.welcome_enabled = True
        session.add(group)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_WELCOME_ENABLED)


@admin_allowed(adm_type=Admin.GROUP)
def disable_welcome(bot: Bot, update: Update, session):
    if update.message.chat.type in ['group']:
        group = update_group(update.message.chat, session)
        group.welcome_enabled = False
        session.add(group)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_WELCOME_DISABLED)


@admin_allowed(adm_type=Admin.GROUP)
def show_welcome(bot: Bot, update, session):
    if update.message.chat.type in ['group']:
        group = update_group(update.message.chat, session)
        welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
        if welcome_msg is None:
            welcome_msg = WelcomeMsg(chat_id=group.id, message=MSG_WELCOME_DEFAULT)
            session.add(welcome_msg)
            session.commit()
        send_async(bot, chat_id=group.id, text=welcome_msg.message)
