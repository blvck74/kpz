from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

admin = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
excl = types.InlineKeyboardButton(text = 'Выгрузить таблицу',callback_data = 'excel')
fnd = types.InlineKeyboardButton(text = 'Поиск сотрудника',callback_data = 'find')
chrt = types.InlineKeyboardButton(text = 'Установить график работы',callback_data = 'chart')
admin.add(excl,fnd,chrt)

accountant = types.InlineKeyboardMarkup(resize_keyboard = True)
fnd = types.InlineKeyboardButton(text = 'Поиск сотрудника',callback_data = 'find')
accountant.add(fnd)

employee = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
sttmnt = types.InlineKeyboardButton(text = 'Заявление на отпуск',callback_data = 'statement')
emchrt = types.InlineKeyboardButton(text = 'График работы',callback_data = 'emchart')
admnmbr = types.InlineKeyboardButton(text = 'Номер администратора',callback_data = 'admnumber')
chck = types.InlineKeyboardButton(text = 'Отметиться на работе',callback_data = 'check')
employee.add(sttmnt,emchrt,admnmbr,chck)

cvv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
res = types.InlineKeyboardButton(text = 'Запросить доступ',callback_data = 'resume')
net = types.InlineKeyboardButton(text = 'Отклонить',callback_data = 'no')
cvv.add(res,net)

confirm = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
da = types.InlineKeyboardButton(text = 'Одобрить',callback_data = 'agree')
net = types.InlineKeyboardButton(text = 'Отклонить',callback_data = 'disagree')
confirm.add(da,net)

econfirm = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
da = types.InlineKeyboardButton(text = 'Одобрить',callback_data = 'agreee')
net = types.InlineKeyboardButton(text = 'Отклонить',callback_data = 'disagreee')
econfirm.add(da,net)