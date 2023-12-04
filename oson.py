from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
import re
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
BOT_TOKEN = ''
CHANNEL_ID = "" 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message,state:FSMContext):
    
    check_sub_channel = await bot.get_chat_member(chat_id=CHANNEL_ID,user_id=message.from_user.id)

    if check_sub_channel['status']!="left":
        await message.answer("<b>❕Iltimos videoni silkasini yuboring</b>",parse_mode="HTML")
        
        await state.set_state('silka')
        

    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="❓Kanalga azo bo'lish", url="https://t.me/python_bot_codelar")],
                [InlineKeyboardButton(text="✅A'zo bo'ldim✅", callback_data="azo")]
         ]  ,
            row_width=2
        )
        await message.reply("⬇️<b>Botdan foydalanish uchun quyidagi kanalga azo boling</b>⬇️", reply_markup=keyboard,parse_mode='HTML')
    
@dp.message_handler(state="silka")
async def silka(msg: types.Message, state: FSMContext):
    url = msg.text 
    try:
        if "www." in url:
            ne = re.sub(str("www."), "dd", url)
            await msg.answer(f"{ne} \n\n❗️@osson_yukla_bot orqali yuklandi✅") 
        else:
                    await msg.answer("❌Xato silka yuborildi! Silka instagramdan ekanligini tekshiring!")
      
    except:
        await msg.answer("❌Xato silka yuborildi! Silka instagramdan ekanligini tekshiring!")



@dp.callback_query_handler(lambda c: c.data == 'azo')
async def callback_subscribe(callback_query: types.CallbackQuery, state: FSMContext):
    check_sub_channel = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)
    
    if check_sub_channel['status'] != "left":
        await callback_query.message.answer(f"<b>❕Botdan foydalanish mumkin! Iltimos videoni silkasini yuboring</b> ",parse_mode="HTML")
        await state.set_state("silka")
        

    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="❓Kanalga azo bo'lish", url="https://t.me/python_bot_codelar")],
                [InlineKeyboardButton(text="✅A'zo bo'ldim✅", callback_data="azo")]
            ],
            row_width=2
        )
        await callback_query.message.reply("❌Azo bolmadingiz qayta urining!❌", reply_markup=keyboard)
       

if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True)

