from pytimeparse import parse

import ptbot

from decouple import config

TG_TOKEN = config('CookEggs_TOKEN')
TG_CHAT_ID = config('TG_ID')


def notify_progress(
                    secs_left,
                    auther_id,
                    id_message_notify,
                    max_secs_notify,
                    bot
                    ):
    message_notify_1 = 'Осталось секунд: {}'.format(secs_left)
    message_notify_2 = render_progressbar(max_secs_notify,
                                          max_secs_notify-secs_left)
    message_notify = message_notify_1 + message_notify_2

    bot.update_message(auther_id, id_message_notify, message_notify)


def render_progressbar(
                       total,
                       iteration,
                       prefix='',
                       suffix='',
                       length=30,
                       fill='█',
                       zfill='░'
                       ):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '\n{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def wait(chat_id, pause_sec, bot):
    secs_left = max_secs = parse(pause_sec)
    id_message = bot.send_message(chat_id, 'Запускаю таймер')
    bot.create_countdown(
                         secs_left,
                         notify_progress,
                         auther_id=chat_id,
                         id_message_notify=id_message,
                         max_secs_notify=max_secs,
                         bot=bot
                         )
    bot.create_timer(secs_left, answer, author_id=chat_id, bot=bot)


def answer(author_id, bot):
    message_time_out = 'Время вышло'
    bot.send_message(author_id, message_time_out)


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':

    main()
