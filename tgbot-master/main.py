import telebot
from telebot import types

import datetime
from prettytable import PrettyTable

import psycopg2

from KEY import token, dbpass

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password=dbpass,
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

bot = telebot.TeleBot(token)

date = datetime.datetime.now()
dt = datetime.date(date.year, date.month, date.day)
wk = dt.isocalendar()[1]
week = ''

if (wk % 2) == 0:
    week = 'нижняя'
else:
    week = 'верхняя'

sql_this_week = "SELECT timetable.day, timetable.time, timetable.subject, teachers.full_name FROM timetable.timetable JOIN \
                 timetable.teachers ON timetable.subject = teachers.subject WHERE (week=%s OR week=%s) AND timetable.day=%s ORDER BY timetable.time"

sql_next_week = "SELECT timetable.day, timetable.time, timetable.subject, teachers.full_name FROM timetable.timetable JOIN \
                 timetable.teachers ON timetable.subject = teachers.subject WHERE (week!=%s OR week=%s) AND timetable.day=%s ORDER BY timetable.time"


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup()
    button = ['Расписание на неделю', 'Расписание на день']
    keyboard.add(*button)
    bot.send_message(message.chat.id,
                     'Здравствуйте, выберите формат расписания',
                     reply_markup=keyboard)


@bot.message_handler(content_types='text')
def select(message):
    if message.text == "Расписание на неделю" or message.text == 'Расписание на день':
        message_reply(message)
    if message.text == "Расписание на нынешнюю неделю" or message.text == "Расписание на следующую неделю":
        message_reply_week(message)
    if message.text == "Понедельник" or message.text == "Вторник" or message.text == "Среда" or \
            message.text == "Четверг" or message.text == "Пятница":
        message_reply_day(message)
    if message.text != "Расписание на неделю" and message.text != 'Расписание на день' \
            and message.text != "Расписание на нынешнюю неделю" and message.text != "Расписание на следующую неделю" \
            and message.text != "Понедельник" and message.text != "Вторник" and message.text != "Среда" \
            and message.text != "Четверг" and message.text != "Пятница":
        bot.send_message(message.chat.id,
                         'Простите, что?')


def message_reply(message):
    if message.text == "Расписание на неделю":
        keyboard = types.ReplyKeyboardMarkup()
        button = ['Расписание на нынешнюю неделю', 'Расписание на следующую неделю']
        keyboard.add(*button)
        bot.send_message(message.chat.id,
                         'Выберите неделю',
                         reply_markup=keyboard)
    if message.text == 'Расписание на день':
        keyboard = types.ReplyKeyboardMarkup()
        button = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        keyboard.add(*button)
        bot.send_message(message.chat.id,
                         'Выберите день недели',
                         reply_markup=keyboard)


def message_reply_week(message):
    records = ''
    keyboard = types.ReplyKeyboardMarkup()
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    table = PrettyTable()
    table.field_names = ["Время", "Предмет", "Преподаватель"]
    if message.text == "Расписание на нынешнюю неделю":
        for n in days:
            j = 0
            cursor.execute(sql_this_week, (week, 'обе', n))
            records = list(cursor.fetchall())
            # print(records)
            table.add_row(['', '', ''])
            table.add_row([n, '', ''])
            table.add_row(['', '', ''])
            while j < len(records):
                # print(n)
                table.add_row([records[j][1], records[j][2], records[j][3]])
                j += 1

    if message.text == "Расписание на следующую неделю":
        for s in days:
            o = 0
            cursor.execute(sql_next_week, (week, 'обе', s))
            records = list(cursor.fetchall())
            # print(records)
            table.add_row(['', '', ''])
            table.add_row([s, '', ''])
            table.add_row(['', '', ''])
            while o < len(records):
                table.add_row([records[o][1], records[o][2], records[o][3]])
                o += 1
    bot.send_message(message.chat.id,
                     f'<pre>{table}</pre>',
                     parse_mode='HTML',
                     reply_markup=keyboard)


def message_reply_day(message):
    if message.text == 'Понедельник' or message.text == 'Вторник' or message.text == 'Среда' or \
            message.text == 'Четверг' or message.text == 'Пятница':
        keyboard = types.ReplyKeyboardMarkup()
        cursor.execute("SELECT timetable.time, timetable.subject, full_name FROM timetable.timetable JOIN "
                       "timetable.teachers ON timetable.subject = teachers.subject "
                       "WHERE day=%s and (week=%s or week=%s) ORDER BY timetable.time ", (message.text, week, 'обе',))
        records = list(cursor.fetchall())
        table = PrettyTable()
        table.field_names = ["Время", "Предмет", "Преподаватель"]
        for i in range(len(records)):
            table.add_row([records[i][0], records[i][1], records[i][2]])
        bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode='HTML', reply_markup=keyboard)


bot.polling()