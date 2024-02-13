from aiogram import Router, Bot, F, types
from aiogram.filters import Command
from admin_kb import kb_get_main_menu, kb_cancel_but, kb_go_to_add_main_menu, kb_pause
from aiogram.filters.state import State, StatesGroup
from user_data import ADMIN_ID
from aiogram.fsm.context import FSMContext
from database import DbSpamer
import re



class AdminStatesGroup(StatesGroup):
    ADMIN_STATE = State()
    ADD_NAME = State()
    ADD_GROUP_A = State()
    ADD_GROUP_B = State()
    ADD_TYPE = State()
    ADD_CAPT_A = State()
    ADD_CAPT_B = State()
    DELETE_PAIR = State()



router = Router()



@router.callback_query(F.data == 'cancel_adding')
async def cancel_add_pair(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = call.message.from_user.id
    await delete_chat_mess(bot, chat_id)
    await state.clear()
    me = await call.message.answer(f"<b>Главная</b>\n",reply_markup=kb_get_main_menu(), parse_mode='HTML')
    await save_message(me)



@router.callback_query(F.data == 'cancel_addingg')
async def cancel_add_pairr(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = call.message.from_user.id
    await delete_chat_mess(bot, chat_id)
    await state.clear()
    me = await call.message.answer(f"<b>Главная</b>\n",reply_markup=kb_get_main_menu(), parse_mode='HTML')
    await save_message(me)




async def save_message(message):
    chat_id = message.chat.id
    message_id = message.message_id
    with DbSpamer() as db:
        db.db_add_message_in_messages_admin(chat_id, message_id)



async def delete_chat_mess(bot: Bot, chat):
    with DbSpamer() as db:
        messages = db.db_get_messages_in_chat_admin(chat)

    for msg in messages:
        chat_mess = int(msg[1])
        try:
            await bot.delete_message(chat_id=msg[0], message_id=chat_mess)
        except Exception:
            continue
    with DbSpamer() as db:
        db.db_delete_message_in_chat_admin(chat)



@router.message(Command('start'))
async def cmd_start(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    await delete_chat_mess(bot, chat_id)
    if chat_id == ADMIN_ID:
        #await state.set_state(AdminStatesGroup.ADMIN_STATE)
        await message.answer('Добавь меня админом во все группы куда нужно выкладывать посты', reply_markup=kb_get_main_menu())


@router.callback_query(F.data == 'add_pair')
async def add_pair(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStatesGroup.ADD_NAME)
    me = await call.message.answer(f"<b>Напиши название пары:</b>\n", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)


@router.message(AdminStatesGroup.ADD_NAME, F.text)
async def processing_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(AdminStatesGroup.ADD_GROUP_A)
    me = await message.answer(f"<b>Напиши айди канала А (-10021321321):</b>\n", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)

@router.message(AdminStatesGroup.ADD_GROUP_A, F.text)
async def processing_group_a(message: types.Message, state: FSMContext):
    group_a = message.text
    await state.update_data(group_a=group_a)
    await state.set_state(AdminStatesGroup.ADD_GROUP_B)
    me = await message.answer(f"<b>Напиши айди канала Б (-10021321321):</b>\n", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)


@router.message(AdminStatesGroup.ADD_GROUP_B, F.text)
async def processing_group_b(message: types.Message, state: FSMContext):
    group_b = message.text
    await state.update_data(group_b=group_b)
    await state.set_state(AdminStatesGroup.ADD_TYPE)
    me = await message.answer(f"<b>Напиши 1 если пересыл моментальный или 2 если посты нужно отправлять на подтверждение админу:</b>\n", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)



@router.message(AdminStatesGroup.ADD_TYPE, F.text)
async def processing_type(message: types.Message, state: FSMContext):
    type = message.text
    try:
        int(type)
        if int(type) in (1, 2):
            await state.update_data(type=type)
        else:
            me = message.answer('1 если пересыл моментальный или 2 если посты нужно отправлять на подтверждение админу')
            await save_message(me)
            return
    except:
        me = message.answer('1 если пересыл моментальный или 2 если посты нужно отправлять на подтверждение админу')
        await save_message(me)
        return
    
    await state.set_state(AdminStatesGroup.ADD_CAPT_A)
    me = await message.answer(f"<b>Пришли подпись постов из группы А если нет то пришли 0:</b>\n", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)




@router.message(AdminStatesGroup.ADD_CAPT_A, F.text)
async def processing_capt_a(message: types.Message, state: FSMContext):
    capt_a = message.text
    await state.update_data(capt_a=capt_a)
    await state.set_state(AdminStatesGroup.ADD_CAPT_B)
    me = await message.answer(f"<b>Пришли подпись с которой буду выкладывать в группу Б если нет то пришли 0:</b>\n", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)



@router.message(AdminStatesGroup.ADD_CAPT_B, F.text)
async def processing_capt_b(message: types.Message, state: FSMContext):
    capt_b = message.text
    await state.update_data(capt_b=capt_b)
    pair_data = await state.get_data()
    with DbSpamer() as db:
        db.db_add_pair_to_db(pair_data)
    me = await message.answer(f"<b>Пара добавлена</b>", reply_markup=kb_go_to_add_main_menu(), parse_mode='HTML')
    await save_message(me)





@router.callback_query(F.data == 'list_pair')
async def list_pair(call: types.CallbackQuery, bot: Bot):
    chat_id = call.message.chat.id
    await delete_chat_mess(bot, chat_id)
    text = ''
    cnt = 0
    with DbSpamer() as db:
        pairs = db.db_get_all_pairs()
    if not pairs:
        text = 'Пусто'
    for pair in pairs:
        pause = 'Да' if pair[7] == True else 'Нет'
        type = 'Моментальная отправка' if pair[3] == 1 else 'Отправка через админа'
        text += f"{pair[6]}\nТип - {type}\nПодпись А - {pair[4]}\nПодпись Б - {pair[5]}\n\nСейчас на паузе - {pause}"
        me = await call.message.answer(text=text, parse_mode='HTML', reply_markup=kb_pause(pair[0]))
        await save_message(me)

    text = 'Конец'
    me = await call.message.answer(text=text, reply_markup=kb_go_to_add_main_menu(), parse_mode='HTML')
    await save_message(me)



@router.callback_query(lambda c: re.match(r'^pause_.*$', c.data))
async def process_pause(call: types.CallbackQuery, bot: Bot):
    pair_id = call.data.split('_')[1]
    with DbSpamer() as db:
        db.db_set_pause_to_pair(pair_id)
    me = await call.message.answer('Пара остановлена', reply_markup=kb_go_to_add_main_menu())
    await save_message(me)


@router.callback_query(lambda c: re.match(r'^star_.*$', c.data))
async def process_start(call: types.CallbackQuery, bot: Bot):
    pair_id = call.data.split('_')[1]
    with DbSpamer() as db:
        db.db_set_start_to_pair(pair_id)
    me = await call.message.answer('Пара запущена', reply_markup=kb_go_to_add_main_menu())
    await save_message(me)



@router.callback_query(F.data == 'delete_pair')
async def delete_pair(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStatesGroup.DELETE_PAIR)
    text = '<b>Для удаления пары пришли ее ID\n</b>'
    cnt = 0
    with DbSpamer() as db:
        pairs = db.db_get_all_pairs()
    if not pairs:
        text = 'Пусто'
    for pair in pairs:
        cnt+=1
        text += f"ID - {pair[0]} {pair[6]}\n"
        if cnt == 20:
            me = await call.message.answer(text=text, parse_mode='HTML')
            await save_message(me)
            cnt = 0
            text = ''
    if cnt > 0:
        me = await call.message.answer(text=text, reply_markup=kb_cancel_but(), parse_mode='HTML')
        await save_message(me)
    else:
        text = 'Конец'
        me = await call.message.answer(text=text, reply_markup=kb_cancel_but(), parse_mode='HTML')
        await save_message(me)

    
@router.message(AdminStatesGroup.DELETE_PAIR, F.text)
async def delete_pair_proc(message: types.Message, state: FSMContext):
    pair_id = message.text
    with DbSpamer() as db:
        db.db_delete_pair(pair_id)
    text = f'Пара с айди {pair_id} удалена'
    me = await message.answer(text=text, reply_markup=kb_go_to_add_main_menu(), parse_mode='HTML')
    await save_message(me)
    


