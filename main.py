import currencyapicom
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /set <value> <0/1> to set a threshold "
                                                                          "value and more/less comparator(0 - value "
                                                                          "must be higher than target, 1 - value must "
                                                                          "be lower than target), /unset to remove")


async def currency(context: ContextTypes.DEFAULT_TYPE) -> None:
    data = client.latest(currencies=['KZT'])
    value = float(data['data']['KZT']['value'])

    if int(context.job.data[1]) == 1:
        if context.job.data[0] >= value:
            text = "TARGET VALUE REACHED, current value is equal to " + str(value)
        else:
            text = "target value haven't been reached, current value is equal to " + str(value)
    else:
        if context.job.data[0] <= value:
            text = "TARGET VALUE REACHED, current value is equal to " + str(value)
        else:
            text = "target value haven't been reached, current value is equal to " + str(value)

    await context.bot.send_message(chat_id=context.job.chat_id, text=text)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the new threshold value/creates new threshold value"""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the value for the currency checker
        threshold = float(context.args[0])
        if threshold < 0:
            await update.effective_message.reply_text("Target value cant be negative!")
            return

        more_less = (context.args[1])
        if threshold < 0:
            await update.effective_message.reply_text("Target value2 cant be negative!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(currency, interval=14400, chat_id=chat_id, name=str(chat_id),
                                        data=[threshold, more_less], first=5)

        text = "Value set successfully!"
        if job_removed:
            text += " Old value was replaced."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <value> <1/0>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Currency checker successfully cancelled!" if job_removed else "You have no active checkers."
    await update.message.reply_text(text)


if __name__ == '__main__':
    application = ApplicationBuilder().token('869735841:AAFvY-ZLU8CxdSo9jtPDrwZqOk2hlYygsgg').build()
    client = currencyapicom.Client('tJl01wusNfgv3zqCGpGK8FlSiZtnlfRlt3pbLTaB')

    start_handler = CommandHandler(['start', 'help'], start)
    application.add_handler(start_handler)

    application.add_handler(CommandHandler('set', set_timer))
    application.add_handler(CommandHandler('unset', unset))

    application.run_polling(poll_interval=3600)

# """
# Simple Bot to send timed Telegram messages.
#
# This Bot uses the Application class to handle the bot and the JobQueue to send
# timed messages.
#
# First, a few handler functions are defined. Then, those functions are passed to
# the Application and registered at their respective places.
# Then, the bot is started and runs until we press Ctrl-C on the command line.
#
# Usage:
# Basic Alarm Bot example, sends a message after a set time.
# Press Ctrl-C on the command line or send a signal to the process to stop the
# bot.
#
# Note:
# To use the JobQueue, you must install PTB via
# `pip install python-telegram-bot[job-queue]`
# """
#
# import logging
#
# from telegram import __version__ as TG_VER
#
# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
#
# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
# from telegram import Update
# from telegram.ext import Application, CommandHandler, ContextTypes
#
# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
#
#
# # Define a few command handlers. These usually take the two arguments update and
# # context.
# # Best practice would be to replace context with an underscore,
# # since context is an unused local variable.
# # This being an example and not having context present confusing beginners,
# # we decided to have it present as context.
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Sends explanation on how to use the bot."""
#     await update.message.reply_text("Hi! Use /set <seconds> to set a timer")
#
#
# async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send the alarm message."""
#     job = context.job
#     await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")
#
#
# def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
#     """Remove job with given name. Returns whether job was removed."""
#     current_jobs = context.job_queue.get_jobs_by_name(name)
#     if not current_jobs:
#         return False
#     for job in current_jobs:
#         job.schedule_removal()
#     return True
#
#
# async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Add a job to the queue."""
#     chat_id = update.effective_message.chat_id
#     try:
#         # args[0] should contain the time for the timer in seconds
#         due = float(context.args[0])
#         if due < 0:
#             await update.effective_message.reply_text("Sorry we can not go back to future!")
#             return
#
#         job_removed = remove_job_if_exists(str(chat_id), context)
#         context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
#
#         text = "Timer successfully set!"
#         if job_removed:
#             text += " Old one was removed."
#         await update.effective_message.reply_text(text)
#
#     except (IndexError, ValueError):
#         await update.effective_message.reply_text("Usage: /set <seconds>")
#
#
# async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Remove the job if the user changed their mind."""
#     chat_id = update.message.chat_id
#     job_removed = remove_job_if_exists(str(chat_id), context)
#     text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
#     await update.message.reply_text(text)
#
#
# def main() -> None:
#     """Run bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("869735841:AAFvY-ZLU8CxdSo9jtPDrwZqOk2hlYygsgg").build()
#
#     # on different commands - answer in Telegram
#     application.add_handler(CommandHandler(["start", "help"], start))
#     application.add_handler(CommandHandler("set", set_timer))
#     application.add_handler(CommandHandler("unset", unset))
#
#     # Run the bot until the user presses Ctrl-C
#     application.run_polling(allowed_updates=Update.ALL_TYPES)
#
#
# if __name__ == "__main__":
#     main()
