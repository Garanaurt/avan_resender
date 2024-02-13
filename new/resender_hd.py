from aiogram import Router, Bot, F, types
from typing import List
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import uuid
import os
from user_data import ADMIN_ID, USERBOT_USER_ID
from database import DbSpamer
from admin_kb import kb_confirmm, kb_confirm_admin
import re
from aiogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)



router = Router()



async def create_media_group(photos_paths, message):
    media_group = []

    for index, photo in enumerate(photos_paths):
        file_extension = os.path.splitext(photo)[1].lower()

        if index == len(photos_paths) - 1:

            if file_extension in ('.jpg', '.jpeg', '.png'):
                media_group.append(types.InputMediaPhoto(media=types.FSInputFile(photo), caption=message, parse_mode='HTML'))
            elif file_extension in ('.mp4', '.mov', '.avi'):
                media_group.append(types.InputMediaVideo(media=types.FSInputFile(photo), caption=message, parse_mode='HTML'))
        
        else:

            if file_extension in ('.jpg', '.jpeg', '.png'):
                media_group.append(types.InputMediaPhoto(media=types.FSInputFile(photo)))
            elif file_extension in ('.mp4', '.mov', '.avi'):
                media_group.append(types.InputMediaVideo(media=types.FSInputFile(photo)))

    return media_group



@router.message(F.text)
async def any_message_answer(message: types.Message, bot: Bot, state: FSMContext):
    if not message.from_user.id == USERBOT_USER_ID:
        return
    text = message.text
    try:
        group_a = f'{message.forward_origin.chat.id}'
        with DbSpamer() as db:
            pair_info = db.db_get_pair_with_group_a(group_a)

        if not pair_info:
            return

        if pair_info[7]:
            return
        if pair_info[4] != '0':
            text = text.replace(pair_info[4], "")

        if int(pair_info[3]) == 1:
            new_text = text + '\n'+ '\n' + pair_info[5] 
            await send_message(caption=new_text, destination=pair_info[2], bot=bot)
        else:
            await send_message(caption=text, destination=pair_info[2], capt=pair_info[5], admin=pair_info[6], bot=bot)
    except Exception as e:
        print(e)





@router.message(F.media_group_id)
async def process_product_media(message: types.Message, bot: Bot, album: List[Message]):
    if not message.from_user.id == USERBOT_USER_ID:
        return
    post_text = ''
    file_paths = []

    for element in album:
        caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}

        for k, v in caption_kwargs.items():
            if k == 'caption' and v is not None:
                post_text += v

        if element.photo:
            name = f'images/{uuid.uuid4()}.png'
            file_paths.append(str(name))
            input_media = InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)
            await bot.download(input_media.media, destination=str(name))

        elif element.video:
            try:
                name = f'images/{uuid.uuid4()}{element.video.file_name[-4:]}'
            except:
                name = f'images/{uuid.uuid4()}.{element.video.mime_type[-3:]}'

            file_paths.append(str(name))

            input_media = InputMediaVideo(media=element.video.file_id, **caption_kwargs)

            try:
                await bot.download(input_media.media, destination=str(name))
            except TelegramBadRequest:
                pass


    group_a = f'{message.forward_origin.chat.id}'
    with DbSpamer() as db:
        pair_info = db.db_get_pair_with_group_a(group_a)

    if not pair_info:
        return
    
    if pair_info[7]:
        return
    
    if pair_info[4] != '0':
        post_text = post_text.replace(pair_info[4], "")

        
    new_text = post_text + '\n'+ '\n' + pair_info[5]
    media = await create_media_group(file_paths, new_text)
    if int(pair_info[3]) == 1:

        await bot.send_media_group(pair_info[2], media=media, parse_mode='HTML')
        for media in file_paths:
            os.remove(media)
    else:
        with DbSpamer() as db:
            message_id = uuid.uuid4()
            paths_as_string = ':'.join(file_paths)
            db.db_save_media(str(message_id), paths_as_string, post_text, pair_info[2], pair_info[5])
        await bot.send_media_group(ADMIN_ID, media)  # дописать отправку через соглашение админа
        await bot.send_message(ADMIN_ID, f'<b>Пересылаю пару {pair_info[6]}</b>',reply_markup=kb_confirmm(message_id), parse_mode='HTML')

    


@router.callback_query(lambda c: re.match(r'^cancel_.*$', c.data))
async def process_cancel_media(call: types.CallbackQuery, bot: Bot):
    message = call.message.text
    await bot.delete_message(ADMIN_ID, call.message.message_id)
    await bot.delete_message(ADMIN_ID, call.message.message_id - 1)



@router.callback_query(lambda c: re.match(r'^cancell_.*$', c.data))
async def process_cancel_media(call: types.CallbackQuery, bot: Bot):
    message = call.message.text
    await bot.delete_message(ADMIN_ID, call.message.message_id)
    await bot.delete_message(ADMIN_ID, call.message.message_id - 1)





@router.callback_query(lambda c: re.match(r'^confirmm_.*$', c.data))
async def process_confirmation_media(call: types.CallbackQuery, bot: Bot):
    media_id = call.data.split('_')[1]
    with DbSpamer() as db:   
        media = db.db_get_media_with_id(media_id)
    photos_paths = media[1].split(":")
    text = media[2] +  '\n'+ '\n' + media[4]
    media_group = await create_media_group(photos_paths, text)
    await bot.send_media_group(media[3], media=media_group)
    for media in photos_paths:
        os.remove(media)
    await bot.delete_message(ADMIN_ID, call.message.message_id)
    await bot.delete_message(ADMIN_ID, call.message.message_id - 1)




@router.callback_query(lambda c: re.match(r'^conf_.*$', c.data))
async def process_confirmat_adm(call: types.CallbackQuery, bot: Bot):
    med_id = call.data.split("_")[1]

    with DbSpamer() as db:
        data = db.db_get_photovideo_with_id(med_id)

    message = data[1] + '\n'+ '\n' + data[2]
    if not call.message.media_group_id:
        if call.message.video:
            video = call.message.video.file_id
            await bot.send_video(data[3], video=video, caption=message, parse_mode='HTML')
        elif call.message.photo:
            photo = call.message.photo[-1].file_id
            await bot.send_photo(data[3], photo=photo, caption=message, parse_mode='HTML')
        else:
            await bot.send_message(data[3], text=message, parse_mode="HTML", disable_web_page_preview=True)

    await bot.delete_message(ADMIN_ID, call.message.message_id)
    await bot.delete_message(ADMIN_ID, call.message.message_id - 1)





@router.message(F.video)
@router.message(F.photo)
async def process_product_one_photo(message: types.Message, bot: Bot):
    if not message.from_user.id == USERBOT_USER_ID:
        print('netnetnet')
        return
    photo = ''

    if message.caption:
        post_text = message.caption
    else:
        post_text = ''  

    group_a = f'{message.forward_origin.chat.id}'

    with DbSpamer() as db:
        pair_info = db.db_get_pair_with_group_a(group_a)

    if not pair_info:
        return
    
    if pair_info[7]:
        return
    

    if message.photo:
        photo = message.photo[-1].file_id
        
        if pair_info:
            if pair_info[4] != '0':
                    post_text = post_text.replace(pair_info[4], "")

            if int(pair_info[3]) == 1:
                new_text = post_text + '\n'+ '\n' + pair_info[5]
                await send_message(photo=photo, caption=new_text, destination=pair_info[2], bot=bot)
            else:
                await send_message(photo=photo, caption=post_text, destination=pair_info[2], bot=bot, admin=pair_info[6], capt=pair_info[5])
            
    elif message.video:
        video = message.video.file_id
        if pair_info:
            if pair_info[4] != '0':
                post_text.replace(pair_info[4], "")
            
            if int(pair_info[3]) == 1:
                new_text = post_text + '\n'+ '\n' + pair_info[5]
                await send_message(video=video, caption=new_text, destination=pair_info[2], bot=bot)
            else:
                await send_message(video=video, caption=post_text, destination=pair_info[2], admin=pair_info[6], capt=pair_info[5], bot=bot)




async def send_message(photo=None, video=None, caption=None, file_paths=None, admin=None, destination=None, bot=Bot, capt=None):
    print('send')
    if video:
        if not admin:
            await bot.send_video(destination, video=video, caption=caption, parse_mode='HTML', disable_web_page_preview=True)
        else:
            await bot.send_message(ADMIN_ID, f'<b>Пересылаю пару {admin}</b>', parse_mode='HTML')
            new_text = caption + '\n'+ '\n' + capt
            with DbSpamer() as db:
                photovideo_id = uuid.uuid4()
                db.db_save_photovideo(photovideo_id, caption, capt, destination)
            await bot.send_video(ADMIN_ID, video=video, caption=new_text, reply_markup=kb_confirm_admin(photovideo_id), parse_mode="HTML")

    elif photo:
        if not admin:
            await bot.send_photo(destination, photo=photo, caption=caption, parse_mode='HTML')
        else:
            await bot.send_message(ADMIN_ID, f'<b>Пересылаю пару {admin}</b>', parse_mode='HTML')
            new_text = caption + '\n'+ '\n' + capt
            with DbSpamer() as db:
                photovideo_id = uuid.uuid4()
                db.db_save_photovideo(photovideo_id, caption, capt, destination)
            await bot.send_photo(ADMIN_ID, photo=photo, caption=new_text, reply_markup=kb_confirm_admin(photovideo_id), parse_mode="HTML")
    else:
        if not admin:
            await bot.send_message(destination, text=caption, parse_mode='HTML', disable_web_page_preview=True)
        else:
            await bot.send_message(ADMIN_ID, text=f'<b>Пересылаю пару {admin}</b>', parse_mode='HTML', disable_web_page_preview=True)
            new_text = caption + '\n'+ '\n' + capt
            with DbSpamer() as db:
                photovideo_id = uuid.uuid4()
                db.db_save_photovideo(photovideo_id, caption, capt, destination)
            await bot.send_message(ADMIN_ID, text=new_text, reply_markup=kb_confirm_admin(photovideo_id), parse_mode="HTML", disable_web_page_preview=True)



    


