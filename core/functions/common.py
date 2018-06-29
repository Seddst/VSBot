import uuid
import logging

from telegram import Update, Bot, ParseMode

from core.functions.triggers import trigger_decorator

from core.texts import *
from core.types import AdminType, Admin, admin_allowed, user_allowed, Auth
from core.utils import send_async, add_user

from config import WEB_LINK


# change adminType

LOGGER = logging.getLogger(__name__)


def error(error):
    """ Error handling """
    LOGGER.error("An error (%s) occurred: %s"
                 % (type(error), error.message))


@user_allowed
def start(bot: Bot, update: Update, session):
    add_user(update.message.from_user, session)
    if update.message.chat.type == ['private', 'group']:
        send_async(bot, chat_id=update.message.chat.id, text=MSG_START_WELCOME, parse_mode=ParseMode.HTML)
        
        
@admin_allowed(adm_type=AdminType.GROUP)
def admin_panel(bot: Bot, update: Update, session):
    if update.message.chat.type == ['private', 'group']:
        admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
        full_adm = False
        for adm in admin:
            if adm.admin_type <= AdminType.FULL.value:
                full_adm = True
        send_async(bot, chat_id=update.message.chat.id, text=MSG_ADMIN_WELCOME,
                   reply_markup=full_adm)
        
        
@user_allowed
def user_panel(bot: Bot, update: Update, session):
    if update.message.chat.type == 'private':
        admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
        is_admin = False
        for _ in admin:
            is_admin = True
            break
        send_async(bot, chat_id=update.message.chat.id, text=MSG_START_WELCOME, parse_mode=ParseMode.HTML,
                   reply_markup=is_admin)

        
@admin_allowed()
def kick(bot: Bot, update: Update):
    bot.leave_chat(update.message.chat.id)


@trigger_decorator
def help_msg(bot:Bot, update, session):
    admin_user = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
    global_adm = False
    for adm in admin_user:
        if adm.admin_type <= Admin.FULL.value:
            global_adm = True
            break
    if global_adm:
        send_async (bot, chat_id=update.message.chat.id, text=MSG_HELP_GLOBAL_ADMIN)
    elif len(admin_user) != 0:
        send_async(bot, chat_id=update.message.chat.id, text=MSG_HELP_GROUP_ADMIN)
    else:
        send_async(bot, chat_id=update.message.chat.id, text=MSG_HELP_USER)


@admin_allowed(adm_type=AdminType.GROUP)
def ping(bot: Bot, update: Update):
    send_async(bot, chat_id=update.message.chat.id, text=MSG_PING.format(update.message.from_user.username))


@admin_allowed(adm_type=AdminType.GROUP)
def delete_msg(bot: Bot, update: Update):
    bot.delete_message(update.message.reply_to_message.chat_id, update.message.reply_to_message.message_id)
    bot.delete_message(update.message.reply_to_message.chat_id, update.message.message_id)


@admin_allowed()
def delete_user(bot: Bot, update: Update):
    bot.kickChatMember(update.message.reply_to_message.chat_id, update.message.reply_to_message.from_user.id)
    bot.unbanChatMember(update.message.reply_to_message.chat_id, update.message.reply_to_message.from_user.id)


@user_allowed
def web_auth(bot: Bot, update: Update, session):
    user = add_user(update.message.from_user, session)
    auth = session.query(Auth).filter_by(user_id=user.id).first()
    if auth is None:
        auth = Auth()
        auth.id = uuid.uuid4().hex
        auth.user_id = user.id
        session.add(auth)
        session.commit()
    link = WEB_LINK.format(auth.id)
    send_async(bot, chat_id=update.message.chat.id, text=MSG_PERSONAL_SITE_LINK.format(link),
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)
