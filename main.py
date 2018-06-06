from telegram.ext import Updater, CommandHandler


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater('602671114:AAFO7AajY4QtufjBgYG7y8dQb4IcpeLgWss')

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
