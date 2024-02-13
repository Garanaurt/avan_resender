from aiogram import types


def kb_go_to_add_main_menu():
    keys = [
        [types.InlineKeyboardButton(text='Назад', callback_data="cancel_addingg")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_cancel_but():
    keys = [
        [types.InlineKeyboardButton(text='Отмена', callback_data="cancel_adding")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_get_main_menu():
    keys = [
        [types.InlineKeyboardButton(text='Добавить пару групп А и Б', callback_data='add_pair')],
        [types.InlineKeyboardButton(text='Удалить пару', callback_data='delete_pair')],
        [types.InlineKeyboardButton(text='Список пар', callback_data="list_pair")],
    ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_confirm(message):
    keys = [
        [types.InlineKeyboardButton(text="Подтвердить", callback_data=f"confirm_{message}")],
        [types.InlineKeyboardButton(text="Отмена", callback_data=f"cancel_{message}")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_confirm_admin(med_id):
    keys = [
        [types.InlineKeyboardButton(text="Подтвердить", callback_data=f"conf_{med_id}")],
        [types.InlineKeyboardButton(text="Отмена", callback_data=f"cancel_{med_id}")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb




def kb_pause(chanel_id):
    keys = [
        [types.InlineKeyboardButton(text="Пауза", callback_data=f"pause_{chanel_id}")],
        [types.InlineKeyboardButton(text="Запуск", callback_data=f"star_{chanel_id}")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb




def kb_confirmm(message):
    keys = [
        [types.InlineKeyboardButton(text="Подтвердить", callback_data=f"confirmm_{message}")],
        [types.InlineKeyboardButton(text="Отмена", callback_data=f"cancell_{message}")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb