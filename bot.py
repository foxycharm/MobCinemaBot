#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)
from telegram.ext.dispatcher import run_async

from config import TOKEN
from src import params
from src.parser import Parser

# Create parser
parser = Parser()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, SEARCH = range(2)

reply_keyboard_more = [['Больше', 'Смотреть онлайн'],
                       ['Другой фильм/сериал']]
markup_more = ReplyKeyboardMarkup(reply_keyboard_more, one_time_keyboard=True)

reply_keyboard_less = [['Меньше', 'Смотреть онлайн'],
                       ['Другой фильм/сериал']]
markup_less = ReplyKeyboardMarkup(reply_keyboard_less, one_time_keyboard=True)


@run_async
def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text(params.START_MSG)

    return SEARCH


@run_async
def sos(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(params.HELP_MSG)


@run_async
def search_text(update, context):
    update.message.reply_text("Минутку...")
    response = parser.parse_text(update.message.text)
    update.message.reply_text(response, reply_markup=markup_more)

    return CHOOSING


@run_async
def search_id(update, context):
    update.message.reply_text("Минутку...")
    parser.parse_id(int(update.message.text[2:]))
    response, photo = parser.output, parser.photo

    if photo is not None:
        update.message.reply_text("[​​​​​​​​​​​]({}) {}".format(photo, response),
                                  reply_markup=markup_more)
    else:
        update.message.reply_text(response, reply_markup=markup_more)

    return CHOOSING


@run_async
def more(update, context):
    print("I`m in more")
    response, photo = parser.full_output, parser.photo
    bot = context.bot
    chat_id = update.message.chat_id  # 3

    bot.send_message(chat_id, 'Preparing...')  # None
    if photo is not None:
        bot.send_message(chat_id, text="[​​​​​​​​​​​]({}) {}".format(photo, response))
    else:
        bot.send_message(chat_id, text=response)

    update.message.reply_text(reply_markup=markup_less)

    return CHOOSING


@run_async
def less(update, context):
    print("I`m in less")
    response, photo = parser.output, parser.photo
    if photo is not None:
        update.message.reply_text("[​​​​​​​​​​​]({}) {}".format(photo, response),
                                  reply_markup=markup_more)
    else:
        update.message.reply_text(response, reply_markup=markup_more)

    return CHOOSING


@run_async
def show(update, context):
    print("I`m in show")
    links = ''
    if parser.id is not None or parser.id == "":
        links += "💰 KINOPOISK " + str(params.link_kinopoisk(parser.id)) + "\n"
    if parser.name is not None or parser.name == "":
        links += " IVI " + params.LINK_IVI + str(parser.name) + "\n" + \
                 "💰 OKKO " + params.LINK_OKKO + str(parser.name) + "\n" +\
                 "🆓 FS " + params.LINK_FS + str(parser.name) +  "\n" +\
                 "🆓 HDREZKA " + params.LINK_HDREZKA + str(parser.name) + "\n" +\
                 "🆓 BASKINO " + params.LINK_BASKINO + str(parser.name) + "\n"
    if links != '':
        update.message.reply_text(links)
    else:
        update.message.reply_text("Ccылок не найдено:(")
    update.message.reply_text(reply_markup=ReplyKeyboardRemove())


@run_async
def other(update, context):
    update.message.reply_text("Какой фильм/сериал вы бы хотели посмотреть?")

    return SEARCH


@run_async
def stop(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('See you soon!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


@run_async
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True,
                      base_url='https://telegg.ru/orig/bot')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", sos))

    # Add conversation handler with the states CHOOSING, SEARCH
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(Filters.text, search_text)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^Больше$'),
                                      more),
                       MessageHandler(Filters.regex('^Меньше$'),
                                      less),
                       MessageHandler(Filters.regex('^Смотреть онлайн$'),
                                      show),
                       MessageHandler(Filters.regex('^Другой фильм/сериал$'),
                                      show),
                       MessageHandler(Filters.regex(r'\/i\d+'), search_id)
                       ],
            SEARCH: [MessageHandler(Filters.text, search_text)]
        },

        fallbacks=[CommandHandler("stop", stop)],
        name="my_conversation",
        persistent=False
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
