import telebot as tb
import sqlite3
import datetime as dt

bot = tb.TeleBot('673810626:AAFwq4l_fWxkRlg38tswsft9Egy_IrplQ-M')
FIO = ''
FN = ''
LN = ''
PN = ''
birth = ''
DM = ''
time = ''


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, '"Этот бот предназначен для '
                                            'быстрой и удобной записи на '
                                            'собеседование. Для регистрации '
                                            'напишите /reg')


@bot.message_handler(commands=['reg'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Введите ваше ФИО:")
    bot.register_next_step_handler(message, get_FIO)


def get_FIO(message):
    global FIO
    FIO = message.text
    FIO = FIO.split(' ')
    if (len(FIO) < 2):
        bot.send_message(message.from_user.id, "Некоректный ввод\nВведите ваше "
                                               "ФИО:")
        bot.register_next_step_handler(message, get_FIO)
    else:
        bot.send_message(message.from_user.id,
                         'Введите дату рождения в формате '
                         'YYYY-MM-DD')
        bot.register_next_step_handler(message, get_birth_day)


def is_number(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def get_birth_day(message):
    global birth
    birth = message.text
    if len(birth) == 10 and birth[4] == '-' and birth[7] == '-':
        year = birth[0:4]
        mon = birth[5:7]
        day = birth[8:10]
        if ((is_number(year) and is_number(mon) and is_number(day))
                and int(year) < 2019 and int(mon) <= 12 and int(mon) > 0 and
                int(day) <= 31 and int(day) > 0):
            keyboard = tb.types.InlineKeyboardMarkup()
            key_RKT = tb.types.InlineKeyboardButton(text='ФШ '
                                                         'радиотехники '
                                                         'и компьютерных '
                                                         'технологий',
                                                    callback_data='RKT')
            key_FOPF = tb.types.InlineKeyboardButton(text='ФШ физики и '
                                                          'исследований им. '
                                                          'Ландау',
                                                     callback_data='FOPF')
            key_FAKI = tb.types.InlineKeyboardButton(text='ФШ '
                                                          'аэрокосмических '
                                                          'технологий',
                                                     callback_data='FAKI')
            key_HF = tb.types.InlineKeyboardButton(
                text='ФШ электроники, фотоники '
                     'и молекулярной физики',
                callback_data='HF')
            key_FPMI = tb.types.InlineKeyboardButton(text='ФШ '
                                                          'прикладной '
                                                          'математики и '
                                                          'информатики',
                                                     callback_data='FPMI')
            key_BM = tb.types.InlineKeyboardButton(text='ФШ биологической и '
                                                        'медицинской физики',
                                                   callback_data='BM')
            keyboard.add(key_FPMI)
            keyboard.add(key_BM)
            keyboard.add(key_FOPF)
            keyboard.add(key_FAKI)
            keyboard.add(key_HF)
            keyboard.add(key_RKT)
            qu = 'Выберите Физтех-Школу на которую хотите поступать:'
            bot.send_message(message.from_user.id, text=qu,
                             reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id,
                             'Несуществующая дата \nВведите дату рождения в '
                             'формате '
                             'YYYY-MM-DD')
            bot.register_next_step_handler(message, get_birth_day)
    else:
        bot.send_message(message.from_user.id,
                         'Неверный формат ввода даты \nВведите дату рождения в'
                         ' формате YYYY-MM-DD')
        bot.register_next_step_handler(message, get_birth_day)


@bot.callback_query_handler(func=lambda call: call.data == 'BM' or call.data
                                              == 'FPMI' or call.data == 'RKT' or
                                              call.data == 'FAKI' or call.data
                                              == 'FOPF' or call.data == 'HF')
def callback_worker(call):
    global DM
    DM = call.data
    ans = 'Верно ли введены данные?\nФИО: '
    for i in FIO:
        ans += i
        ans += ' '
    if call.data == 'BM':
        sch = 'Биологической и медицинской физики'
    elif call.data == 'FPMI':
        sch = 'Прикладной математики и информатики'
    elif call.data == 'RKT':
        sch = 'Радиотехники и компьютерных технологий'
    elif call.data == 'FAKI':
        sch = 'Аэрокосмических технологий'
    elif call.data == 'FOPF':
        sch = 'Физики и исследований им. Ландау'
    elif call.data == 'HF':
        sch = 'Электроники, фотоники и молекулярной физики'

    ans += '\nДата рождения: {}\nФизтех-Школа: {}'.format(birth, sch)
    # bot.send_message(call.message.chat.id, 'Запомню : )')
    # bot.register_next_step_handler(call.message, get_FIO)
    newkeyboard = tb.types.InlineKeyboardMarkup()
    key_yes = tb.types.InlineKeyboardButton(text='Да',
                                            callback_data='yes')
    key_no = tb.types.InlineKeyboardButton(text='Нет',
                                           callback_data='no')
    newkeyboard.add(key_yes)
    newkeyboard.add(key_no)
    bot.send_message(call.message.chat.id, text=ans,
                     reply_markup=newkeyboard)

    # record(FIO, birth, DM)


@bot.callback_query_handler(func=lambda call: call.data == 'yes' or call.data
                                              == 'no')
def callback_worker(call):
    if call.data == 'yes':
        record(FIO, birth, DM)
        ans = 'Вы успешно записаны!\nЖдем вас на ' \
              'собеседовании: '
        ans_time = time[0:10]
        ans += ans_time + ' в ' + time[11:16] + '\nПри себе ' \
            'необходимо иметь ' \
            'документы указанные на сайте приемной комиссии: https://pk.mipt.ru'
        bot.send_message(call.message.chat.id, ans)
    else:
        bot.send_message(call.message.chat.id, 'Введите ваше ФИО:')
        bot.register_next_step_handler(call.message, get_FIO)


def record(FIO, birth, DM):
    global time
    conn = sqlite3.connect('People.db')
    c = conn.cursor()
    for row in c.execute('SELECT max(ID)  FROM People'):
        New_id = int(row[0]) + 1
    # c.execute('''CREATE TABLE People
    # (ID INT PRIMARY KEY,FirstName VARCHAR(40),Lastname VARCHAR(40),
    # Patronymic VARCHAR(40), Birth VARCHAR(11))''')
    if len(FIO) > 2:
        row = [(New_id, FIO[1], FIO[0], FIO[2], birth)]
    else:
        row = [(New_id, FIO[1], FIO[0], 'NULL', birth)]
    c.executemany('INSERT INTO People VALUES (?,?,?,?,?)', row)
    conn.commit()
    c.close()
    conn = sqlite3.connect('DepI.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE DepI (ID INT PRIMARY KEY, Depart VARCHAR(10),
    # Interview VARCHAR(25))''')
    for row in c.execute('SELECT Interview  FROM DepI WHERE ID IN (SELECT '
                         'max(ID)  FROM DepI)'):
        LInterview = str(row[0])
    hour = int(LInterview[11:13])
    minute = int(LInterview[14:16])
    time = dt.datetime(year=2019, month=7, day=15, hour=hour, \
                       minute=minute)
    time = time + dt.timedelta(minutes=15)
    time = str(time)
    print(New_id, type(New_id), DM, type(DM), time, type(time))
    row = [(New_id, DM, time)]
    c.executemany('INSERT INTO DepI VALUES(?,?,?)', row)
    conn.commit()
    c.close()


bot.polling(none_stop=True, interval=0)
