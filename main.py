import sqlite3
from sqlite3 import Error
import keyboards as kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, message
from xlsxwriter.workbook import Workbook
from config import chiefadm,token,anumber


workbook = Workbook('users.xlsx')
worksheet = workbook.add_worksheet()


class invite(StatesGroup):
    fio = State()
    dostup = State()
    wpost = State()
    pnumber = State()
class find(StatesGroup):
    who = State()
class setchart(StatesGroup):
    nfind = State()
    chart = State()
class free(StatesGroup):
    type = State()
    uns = State()
    sdate = State()
    edate = State()
    com = State()
    chief = State()

TOKEN = token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage = MemoryStorage())


with sqlite3.connect("database.db") as conn:
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS users
  (user INTEGER, fio TEXT,dostuplvl TEXT, post TEXT,number INTEGER,chart TEXT)
  """)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    access = cursor.execute(f'SELECT user FROM users WHERE user = {message.from_user.id}')
    if access.fetchone() is None: 
        await bot.send_message(message.chat.id,text = 'Вы не являетесь сотрудником.\nДля доступа к боту оставьте заявку',reply_markup = kb.cvv)
    else:
        post = cursor.execute(f'SELECT dostuplvl FROM users WHERE user = {message.from_user.id}').fetchone()[0]
        if post == 'Администратор':
            await bot.send_message(message.chat.id,text = 'Вы авторизировались как администратор\nВам доступны следующие функции:',reply_markup = kb.admin)
        if post == 'Бухгалтер':
            await bot.send_message(message.chat.id,text = 'Вы авторизировались как бухгалтер\nВам доступны следующие функции:',reply_markup = kb.accountant)
        if post == 'Сотрудник':
            await bot.send_message(message.chat.id,text = 'Вы авторизировались как сотрудник\nВам доступны следующие функции:',reply_markup = kb.employee)




@dp.message_handler(state=invite.fio)
async def ivitef(message: types.Message, state: FSMContext):
    fio = message.text
    await state.update_data(fio=fio)
    global emplyee
    emplyee = message.from_user.id
    await message.answer('Введите ваш уровень доступа: "сотрудник"')
    await invite.dostup.set()


@dp.message_handler(state=invite.dostup)
async def ivited(message: types.Message, state: FSMContext):
    dostup = message.text
    await state.update_data(dostup=dostup)
    await message.answer('Введите Вашу должность в организации')
    await invite.wpost.set()


@dp.message_handler(state=invite.wpost)
async def invitewp(message: types.Message, state: FSMContext):
    wpost = message.text
    await state.update_data(wpost=wpost)
    await message.answer('Введите Ваш контактный номер телефона')
    await invite.pnumber.set()


@dp.message_handler(state=invite.pnumber)
async def invitepn(message: types.Message, state: FSMContext):
    global pnumber
    pnumber = message.text
    await state.update_data(pnumber=pnumber)
    data = await state.get_data()
    global fio
    fio = data.get('fio')
    global wpost
    wpost = data.get('wpost')
    global dostup
    dostup = data.get('dostup')
    await bot.send_message(message.chat.id,text = 'Ваше заявление было отправлено на рассмотрение!\nОжидайте ответа')
    await bot.send_message(chiefadm,text = f'Новое заявление!\n\nФИО: <b>{fio}\n</b>Уровень доступа:<b>{dostup}</b>\nДолжность: <b>{wpost}</b>\nНомер телефона: <b>{pnumber}</b>',reply_markup = kb.confirm,parse_mode = 'HTML')
    await state.finish()

@dp.message_handler(state=find.who)
async def findw(message: types.Message, state: FSMContext):
    who = message.text
    await state.update_data(who=who)
    try:
        s1 = cursor.execute(f"SELECT post FROM users WHERE fio = '{who}'").fetchone()[0]
        s2 = cursor.execute(f"SELECT number FROM users WHERE fio = '{who}'").fetchone()[0]
        s3 = cursor.execute(f"SELECT chart FROM users WHERE fio = '{who}'").fetchone()[0]
        s4 = cursor.execute(f"SELECT dostuplvl FROM users WHERE fio = '{who}'").fetchone()[0]
        await bot.send_message(message.chat.id,text = f'Фамилия: <b>{who}\n</b>Уровень доступа: <b>{s4}</b>\nДолжность: <b>{s1}</b>\nНомер телефона: <b>{s2}</b>\nГрафик работы: <b>{s3}</b>',parse_mode = 'HTML')
        await state.finish()
    except:
        await bot.send_message(message.chat.id,text = 'Сотрудников с таким ФИО не обнаружено.')
        await state.finish()


@dp.message_handler(state=setchart.nfind)
async def nfind(message: types.Message, state: FSMContext):
    nfind = message.text
    await state.update_data(nfind=nfind)
    await bot.send_message(message.chat.id,text = 'Введите график для сотрудника')
    await setchart.chart.set()


@dp.message_handler(state=setchart.chart)
async def chart(message: types.Message,state: FSMContext):
    chart = message.text
    await state.update_data(chart=chart)
    data = await state.get_data()
    nfind = data.get('nfind')
    try:
        cursor.execute(f"UPDATE users SET chart = '{chart}' WHERE fio = '{nfind}'")
        conn.commit()
        await bot.send_message(message.chat.id,text = 'График был успешно поставлен!')
        await state.finish()
    except:
        await bot.send_message(message.chat.id,text = 'Сотрудников с таким ФИО не обнаружено.')
        await state.finish()

    
@dp.message_handler(state=free.type)
async def type(message: types.Message, state: FSMContext):
    type = message.text
    await state.update_data(type=type)
    await bot.send_message(message.chat.id,text = 'Внеплановый отпуск (да или нет)')
    await free.uns.set()


@dp.message_handler(state=free.uns)
async def uns(message: types.Message, state: FSMContext):
    uns = message.text
    await state.update_data(uns=uns)
    await bot.send_message(message.chat.id,text = 'Напишите дату начала отпуска в формате День.Месяц.Год\nВнимание! Количество возможных дней отпуска уточняйте у своего руководителя.')
    await free.sdate.set()

@dp.message_handler(state=free.sdate)
async def sdate(message: types.Message, state: FSMContext):
    sdate = message.text
    await state.update_data(sdate=sdate)
    await bot.send_message(message.chat.id,text = 'Напишите дату окончания отпуска в формате День.Месяц.Год')
    await free.edate.set()


@dp.message_handler(state=free.edate)
async def edate(message: types.Message, state: FSMContext):
    edate = message.text
    global emplye
    emplye = message.from_user.id
    await state.update_data(edate=edate)
    await bot.send_message(message.chat.id,text = 'Напишите комментарий по своему желанию. Если нет, напишите прочерк.')
    await free.com.set()

@dp.message_handler(state=free.com)
async def com(message: types.Message, state: FSMContext):
    com = message.text
    await state.update_data(com=com)
    await bot.send_message(message.chat.id,text = 'Напишите ФИО согласующего руководителя.')
    await free.chief.set()


@dp.message_handler(state=free.chief)
async def chief(message: types.Message, state: FSMContext):
    chief = message.text
    await state.update_data(chief=chief)
    await bot.send_message(message.chat.id,text = 'Ваша заявка была отправлены администрации')
    data = await state.get_data()
    l1 = data.get('type')
    l2 = data.get('uns')
    l3 = data.get('sdate')
    l4 = data.get('edate')
    l5 = data.get('com')
    await bot.send_message(chiefadm,text = f'Заявление на отпуск!\n\n1.{l1}\n2.{l2}\n3.{l3}\n4.{l4}\n5.{l5}\n6.{chief}\n',reply_markup = kb.econfirm)
    await state.finish()




@dp.callback_query_handler(lambda c: c.data)
async def functions(call: CallbackQuery,state: FSMContext):
    if call.data == 'resume':
        await bot.send_message(call.message.chat.id,text = 'Введите свое ФИО')
        await invite.fio.set()
    if call.data == 'no':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id,text = 'Вы отказались от подачи заявления.\nВсего доброго')
    if call.data == 'agreee':
        await bot.send_message(call.message.chat.id,text = 'Заявление было одобрено\nСотрудник будет оповещен')
        await bot.send_message(emplye,text = 'Ваша заявка на отпуск была одобрена.\n')
    if call.data == 'disagree':
        await bot.send_message(emplye,text = 'Ваша заявка на отпуск была отклонена.')
        await state.finish()
    if call.data == 'agree':
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users values (:user, :fio, :dostuplvl,  :post, :number, :chart);" ,
            {'user':emplyee,
            'fio': fio,
            'dostuplvl':dostup,
            'post':wpost,
            'number':pnumber,
            'chart': ""})
            conn.commit()
        await state.finish()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id,text = 'Заявление было одобрено\nСотрудник будет оповещен')
        await bot.send_message(emplyee,text = 'Ваша заявка была одобрена.\nДля авторизации в системе пропишите /start')
    if call.data == 'disagree':
        await bot.send_message(emplyee,text = 'Ваша заявка была отклонена.')
        await state.finish()
    if call.data == 'excel':
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        c.execute("select * from users")
        mysel=c.execute("select * from users ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()
        doc = open('users.xlsx', 'rb')
        await bot.send_document(call.message.chat.id,doc)
        doc.close()
    if call.data == 'find':
        await bot.send_message(call.message.chat.id,text = 'Введите ФИО сотрудника по которому желаете вывести информацию')
        await find.who.set()    
    if call.data == 'chart':
        await bot.send_message(call.message.chat.id,text = 'Введите ФИО сотрудника которому хотите установить график работы')
        await setchart.nfind.set()
    if call.data == 'statement':
        await bot.send_message(call.message.chat.id,text = 'Вид отпуска: (Напишите необходимый вид отпуска)\n- Ежегодный основной оплачиваемый\n- Без сохранения з/платы\n- Учебный\n- Дополнительный')
        await free.type.set()
    if call.data == 'emchart':
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            chart = cursor.execute(f"SELECT chart FROM users WHERE user = '{call.from_user.id}'").fetchone()[0]
            await bot.send_message(call.message.chat.id,text = f'Ваш график работы:\n{chart}')
    if call.data == 'admnumber':
        await bot.send_message(call.message.chat.id,text = anumber)
    if call.data == 'check':
        await bot.send_message(call.message.chat.id,text = 'Вы успешно отмечены на работе.\nПросьба нажимать кнопку только 1 раз в день!')







executor.start_polling(dp)