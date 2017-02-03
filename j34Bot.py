from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
import configparser
import logging

config=configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)

RUNNING = range(1)

#
# Start the hi3 bot
#
def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(
        'Hallo %s! Ich habe dich für ein Waschmaschinen-Update registriert.' % user.first_name
    )
    return RUNNING

def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Du bekommst keine Updates mehr %s.' % user.first_name)
    return ConversationHandler.END

def main():
    updater = Updater(config['Telegram']['Token'])
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('Start', start)],
        states={
            RUNNING: [
            ]
        },
        fallbacks=[CommandHandler('stop', cancel),
                   CommandHandler('Stop', cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
