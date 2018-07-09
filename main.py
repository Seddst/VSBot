# -*- coding: utf-8 -*-

import logging

from telegram import (
    Bot, Update
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters
)
from telegram.ext.dispatcher import run_async
from telegram.error import TelegramError

from config import TOKEN
from core.chat_commands import CC_SET_WELCOME, CC_HELP, CC_SHOW_WELCOME, CC_TURN_ON_WELCOME, \
    CC_TURN_OFF_WELCOME, CC_SET_TRIGGER, CC_UNSET_TRIGGER, CC_TRIGGER_LIST, CC_ADMIN_LIST, CC_PING, \
    CC_ALLOW_TRIGGER_ALL, CC_DISALLOW_TRIGGER_ALL, CC_ADMINS, \
    CC_ALLOW_PIN_ALL, CC_DISALLOW_PIN_ALL, \
    CC_PIN, CC_SILENT_PIN, CC_DELETE, CC_KICK

from core.functions.admins import (
    list_admins, admins_for_users, set_admin, del_admin, set_global_admin,
    set_super_admin, del_global_admin

)
from core.functions.ban import unban, ban


from core.functions.common import (
    help_msg, ping, error, kick, admin_panel,
    delete_msg, delete_user, user_panel)


from core.functions.pin import pin, not_pin_all, pin_all, silent_pin

from core.functions.triggers import (
    set_trigger, add_trigger, del_trigger, list_triggers, enable_trigger_all,
    disable_trigger_all, trigger_show,
    set_global_trigger, add_global_trigger, del_global_trigger
)
from core.functions.welcome import (
    welcome, set_welcome, show_welcome, enable_welcome, disable_welcome
)


from core.types import Admin, user_allowed
from core.utils import add_user

# -----constants----
VSMAIN_ID = 591505188
TRADEBOT_ID = 0
# 278525885
# -------------------

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def del_msg(bot, job):
    try:
        bot.delete_message(job.context[0], job.context[1])
    except TelegramError:
        pass


@run_async
@user_allowed
def manage_all(bot: Bot, update: Update, session):
    add_user(update.message.from_user, session)
    
    if update.message.chat.type in ['group', 'supergroup', 'channel']:

        if not update.message.text:
            return

        text = update.message.text.lower()

        if text.startswith(CC_SET_WELCOME):
            set_welcome(bot, update)
        elif text == CC_HELP:
            help_msg(bot, update)

        elif text == CC_SHOW_WELCOME:
            show_welcome(bot, update)
        elif text == CC_TURN_ON_WELCOME:
            enable_welcome(bot, update)
        elif text == CC_TURN_OFF_WELCOME:
            disable_welcome(bot, update)
        elif text.startswith(CC_SET_TRIGGER):
            set_trigger(bot, update)
        elif text.startswith(CC_UNSET_TRIGGER):
            del_trigger(bot, update)
        elif text == CC_TRIGGER_LIST:
            list_triggers(bot, update)
        elif text == CC_ADMIN_LIST:
            list_admins(bot, update)
        elif text == CC_PING:
            ping(bot, update)

        elif text == CC_ALLOW_TRIGGER_ALL:
            enable_trigger_all(bot, update)
        elif text == CC_DISALLOW_TRIGGER_ALL:
            disable_trigger_all(bot, update)
        elif text in CC_ADMINS:
            admins_for_users(bot, update)
        elif text == CC_ALLOW_PIN_ALL:
            pin_all(bot, update)
        elif text == CC_DISALLOW_PIN_ALL:
            not_pin_all(bot, update)

        elif update.message.reply_to_message is not None:
            if text == CC_PIN:
                pin(bot, update)
            elif text == CC_SILENT_PIN:
                silent_pin(bot, update)
            elif text == CC_DELETE:
                delete_msg(bot, update)
            elif text == CC_KICK:
                delete_user(bot, update)
            else:
                trigger_show(bot, update)

        else:
            trigger_show(bot, update)

# might need to remove elif statements below

    elif update.message.chat.type == 'private':
            admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
            is_admin = False
            for _ in admin:
                is_admin = True
                break

            if not is_admin:
                user_panel(bot, update)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    disp = updater.dispatcher

    # on different commands - answer in Telegram
    # disp.add_handler(CommandHandler("test", ready_to_battle_result))

    disp.add_handler(CommandHandler("start", user_panel))
    disp.add_handler(CommandHandler("admin", admin_panel))
    disp.add_handler(CommandHandler("help", help_msg))
    disp.add_handler(CommandHandler("ping", ping))
    disp.add_handler(CommandHandler("set_global_trigger", set_global_trigger))
    disp.add_handler(CommandHandler("add_global_trigger", add_global_trigger))
    disp.add_handler(CommandHandler("del_global_trigger", del_global_trigger))
    disp.add_handler(CommandHandler("set_trigger", set_trigger))
    disp.add_handler(CommandHandler("add_trigger", add_trigger))
    disp.add_handler(CommandHandler("del_trigger", del_trigger))
    disp.add_handler(CommandHandler("list_triggers", list_triggers))
    disp.add_handler(CommandHandler("set_welcome", set_welcome))
    disp.add_handler(CommandHandler("enable_welcome", enable_welcome))
    disp.add_handler(CommandHandler("disable_welcome", disable_welcome))
    disp.add_handler(CommandHandler("show_welcome", show_welcome))
    disp.add_handler(CommandHandler("add_admin", set_admin))
    disp.add_handler(CommandHandler("add_global_admin", set_global_admin))
    disp.add_handler(CommandHandler("del_global_admin", del_global_admin))
    disp.add_handler(CommandHandler("add_super_admin", set_super_admin))
    disp.add_handler(CommandHandler("del_admin", del_admin))
    disp.add_handler(CommandHandler("list_admins", list_admins))
    disp.add_handler(CommandHandler("kick", kick))
    disp.add_handler(CommandHandler("enable_trigger", enable_trigger_all))
    disp.add_handler(CommandHandler("disable_trigger", disable_trigger_all))

    disp.add_handler(CommandHandler("ban", ban))
    disp.add_handler(CommandHandler("unban", unban))

    # on noncommand i.e message - echo the message on Telegram
    # disp.add_handler(MessageHandler(Filters.status_update, welcome))
    disp.add_handler(MessageHandler(
        Filters.text))
    disp.add_handler(MessageHandler(
        Filters.all, manage_all))

    # log all errors
    disp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # app.run(port=API_PORT)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

