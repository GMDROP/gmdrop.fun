from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputMediaPhoto, InputMediaVideo
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import escape_md
from aiogram.dispatcher import FSMContext

from datetime import datetime, timedelta
from math import ceil, floor
import logging
import sqlite3
import random


from config import BOT_TOKEN, ADMIN_IDS, MANAGER_IDS, PAGINATION_ACTIVE_LOTS, ADMIN_CHANNEL_ID, bot_username, \
    ORDERS_CHAT_LINK, ORDERS_CHANNEL_ID, MAIN_CHANNEL
import keyboards
import db

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

info_db = 'info.db'

with sqlite3.connect(info_db) as con:
    cursor = con.cursor()

    help_link_data = cursor.execute('SELECT text FROM help_link').fetchone()[0]
    help_text_data = cursor.execute('SELECT text FROM help_text').fetchone()[0]

    price_in_currency_UAH_data = cursor.execute('SELECT data FROM price_in_currency WHERE currency = ?', ('UAH',)).fetchone()[0]
    price_in_currency_RUB_data = cursor.execute('SELECT data FROM price_in_currency WHERE currency = ?', ('RUB',)).fetchone()[0]
    price_in_currency_USD_data = cursor.execute('SELECT data FROM price_in_currency WHERE currency = ?', ('USD',)).fetchone()[0]
    price_in_currency_G_data = cursor.execute('SELECT data FROM price_in_currency WHERE currency = ?', ('G',)).fetchone()[0]

    requisites_UAH_data = cursor.execute('SELECT data FROM requisites WHERE currency = ?', ('UAH',)).fetchone()[0]
    requisites_RUB_data = cursor.execute('SELECT data FROM requisites WHERE currency = ?', ('RUB',)).fetchone()[0]
    requisites_USD_data = cursor.execute('SELECT data FROM requisites WHERE currency = ?', ('USD',)).fetchone()[0]

help_link = help_link_data
help_text = help_text_data

price_in_currency = {
    'UAH': price_in_currency_UAH_data,
    'RUB': price_in_currency_RUB_data,
    'USD': price_in_currency_USD_data,
    'G': price_in_currency_G_data
}

requisites = {
    'UAH': requisites_UAH_data,

    'RUB': requisites_RUB_data,

    'USD': requisites_USD_data,
}

how_use_bot_text = '''
Приветствую тебя , Друг 👋🏻

Раз ты читаешь эту статью - это значит , что ты не совсем разобрался как пользоваться нашим Ботом, сейчас всё объясню 😉
——————————————————-

КАК ПОПОЛНИТЬ БАЛАНС

Начнём? Так, для покупки переходим в Профиль и нажимаем на кнопку «пополнить баланс».
Пополнение счета происходит в YC, это внутренняя валюта , которая по курсу равна
1 грн - 1 YC
2 руб - 1 YC
Пополнить Баланс можно на Украинские, на Русские и на Грузинские банковские карты , а так же , мы принимаем в Tether $ !
Отлично, теперь у нас имеются YC
——————————————————-

РОЗЫГРЫШИ 

Далее мы нажимаем на кнопку «Розыгрыши», где у нас открывается список актуальных розыгрышей , и там уже выбираем самый подходящий для нас розыгрыш и принимаем в нем участие ✨

Функционал у всех розыгрышей разный 
Это зависит от:

-Приза
-Стоимость участия 
-Количество участников 
-Количество победителей
-Количество допустимых участии для одного пользователя 
-Минимальный уровень пользователя для участия 
——————————————————-

Отлично , мы разобрались с тем как пополнить баланс и учавствовать в розыгрышах ✅


УРОВЕНЬ ПОЛЬЗОВАТЕЛЯ 

О Уровне пользователя!
У каждого пользователя ,если нажать на кнопку «Профиль», есть «Уровень» от 1 до 50.
В розыгрышах бывает так , что для участия требуется определённый уровень, например , чтобы учавствовать в том или ином розыгрыше , требуется 2 - 5 или 40 уровень , и тд 
А ещё , от Уровня зависит то, как часто вы можете делать вывод YC 

От 1 до 10 уровня - 1 раз в 3 дня 
От 11 до 25 уровня - 1 раз в 2 дня
От 26 до 49 уровня - 1 раз в день
А 50 уровень даёт вам безлимит 
——————————————————-

ВЫВОД YLION COINS НА РЕАЛЬНЫЕ ДЕНЬГИ

У вас есть возможность как пополнять баланс , так же и выводить Реальные деньги которые вы получили в виде приза или Илион Коина!

Кнопка вывода так же находится в Профиле!
-Минимальная сумма для вывода 40 YC
-Вывод ограничен, подробнее об этом мы рассказали выше в разделе УРОВНИ
-Вывод можно сделать на Украинские , Российские и Грузинские банковские карты, так же в TETHER $
——————————————————-


РЕФЕРАЛЬНАЯ СИСТЕМА 

У каждого пользователя есть своя собственная Реферальная ссылка , с помощью которой он может приглашать друзей и знакомых , и за это получать Приз в виде 
2 YC 

Но чтобы получить приз, требуется чтобы ваш приглашённый пополнил баланс минимум на 40YC
——————————————————-


КАК ПОПАСТЬ В ТОП 10

В Топ 10 у нас есть 3 раздела 

Топ 10 Игроков в Дуэли 
Топ 10 Донатеров 
и 
Топ 10 Участников

Донатеры это те , кто больше всех пополнили Баланс.
Участники это те , кто больше всех приняли участие в розыгрышах 
А в Дуэлях это игроки с наибольшим количеством побед в Дуэлях 
——————————————————-

Думаю , на этом мы с тобой уже имеем полное представление как пользоваться ботом YLION GIVEAWAY ✅

Спасибо , что обратился , для более подробной информации Нажми на кнопку «Поддержка» и тебе наши сотрудники всё объяснят и покажут    '''

statistic_months = {
    1: 'Января',
    2: 'Февраля',
    3: 'Марта',
    4: 'Апреля',
    5: 'Мая',
    6: 'Июня',
    7: 'Июля',
    8: 'Августа',
    9: 'Сентября',
    10: 'Октября',
    11: 'Ноября',
    12: 'Декабря',
}


class UserWithdrawal(StatesGroup):
    get_bank_name = State()
    get_name = State()
    get_card = State()
    get_amount = State()
    get_currency = State()
    get_confirm = State()


class UserWithdrawalG(StatesGroup):
    get_amount = State()
    get_confirm = State()


class UserTopUp(StatesGroup):
    get_amount = State()
    get_currency = State()
    get_confirmation = State()


class UserWriteReview(StatesGroup):
    get_text = State()


class UserPromoCode(StatesGroup):
    name = State()


class UserDuelsRegistration(StatesGroup):
    st_id = State()
    game_mode = State()
    st_rank = State()
    bet = State()
    st_name = State()
    confirm = State()


class UserDuelTakePart(StatesGroup):
    st_id = State()
    st_rank = State()
    st_name = State()


class UserChangeYcToG(StatesGroup):
    amount = State()
    confirm = State()


class AdminCreateLot(StatesGroup):
    create_lot_name = State()
    create_lot_desc = State()
    create_lot_one_bid_price = State()
    create_lot_total_bids = State()
    create_lot_max_user_bets = State()
    create_lot_media = State()
    create_lot_need_level = State()

    winners_amount = State()

    want_add_automatic_prize = State()
    automatic_prize_amount = State()

    create_lot_confirm = State()


class AdminTopUp(StatesGroup):
    get_amount = State()


class AdminSetWinner(StatesGroup):
    get_id_or_username = State()
    confirm = State()


class AdminEditUserData(StatesGroup):
    get_user_id = State()
    balance = State()
    level = State()


class AdminEditBotData(StatesGroup):
    edit_requisites_type = State()
    edit_requisites_data = State()
    edit_in_currency_type = State()
    edit_in_currency_data = State()
    edit_help_link = State()
    edit_help_text = State()


class AdminMail(StatesGroup):
    get_data = State()
    confirm = State()


class AdminAddPromoCode(StatesGroup):
    promo_type = State()
    amount = State()
    name = State()
    activations = State()
    confirm = State()


class AdminEditPromo(StatesGroup):
    activations = State()
    amount = State()


class AdminDuelInfo(StatesGroup):
    duel_id = State()

# Обработчик для забаненых пользователей

@dp.message_handler(content_types=['text', 'photo', 'document', 'voice', 'video'], state='ban')
async def for_baned_users(message: types.Message, state: FSMContext):
    pass

@dp.callback_query_handler(lambda call: True, state='ban')
async def for_baned_users_callback(call: types.CallbackQuery, state: FSMContext):
    pass



# Создание лота

@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_name)
async def create_lot_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    name = message.text

    await state.update_data(name=name)

    await message.answer('Введите описание розыгрыша', reply_markup=keyboards.cancel_keyboard)
    await AdminCreateLot.create_lot_desc.set()


@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_desc)
async def create_lot_desc(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    desc = message.text

    await state.update_data(desc=desc)

    await message.answer('Укажите цену одного участия', reply_markup=keyboards.cancel_keyboard)
    await AdminCreateLot.create_lot_one_bid_price.set()


@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_one_bid_price)
async def create_lot_one_bid_price(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    try:
        one_bid_price = int(message.text)
        if one_bid_price < 0:
            return await message.answer('Укажите цену больше 0')

        await state.update_data(one_bid_price=one_bid_price)

        await message.answer('Укажите общее количество участий', reply_markup=keyboards.cancel_keyboard)

        await AdminCreateLot.create_lot_total_bids.set()

    except:
        await message.answer('Вы ввели не число\nПопробуйте еще раз ввести число не меньше 1')
        await message.answer('Укажите цену одного участия')


@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_total_bids)
async def create_lot_total_bids(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    try:
        total_bids = int(message.text)
        if total_bids < 1:
            return await message.answer('Укажите количество больше 1')

        await state.update_data(total_bids=total_bids)

        await message.answer('Отправьте максимальное количество участий для одного пользователя', reply_markup=keyboards.cancel_keyboard)

        await AdminCreateLot.create_lot_max_user_bets.set()

    except:
        await message.answer('Вы ввели не число\nПопробуйте еще раз ввести число не меньше 1')
        await message.answer('Укажите общее количество участий')


@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_max_user_bets)
async def create_lot_max_user_bets(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    try:
        max_user_bets = int(message.text)
        if max_user_bets <= 0:
            return await message.answer('Укажите количество больше нуля')

        await state.update_data(max_user_bets=max_user_bets)
        async with state.proxy() as data:
            data['files'] = []

        await message.answer('Отправьте фото', reply_markup=keyboards.cancel_keyboard)

        await AdminCreateLot.create_lot_media.set()

    except:
        await message.answer('Вы ввели не число\nПопробуйте еще раз ввести число не меньше 1')
        await message.answer('Отправьте максимальное количество ставок для одного пользователя')


@dp.message_handler(content_types=['text', 'photo'], state=AdminCreateLot.create_lot_media)
async def create_lot_media(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if message.text == 'Отменить':
            await state.finish()
            return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

        else:
            await message.answer('Отправьте фото')
        return 1

    elif message.content_type == 'photo':
        file_id = message.photo[0].file_id

        await state.update_data(photo=file_id)

        await message.answer('Отправьте требованный уровень (число от 1 до 50)', reply_markup=keyboards.cancel_keyboard)
        await AdminCreateLot.create_lot_need_level.set()


@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_need_level)
async def create_lot_need_level(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    try:
        need_level = int(message.text)
        if need_level < 1 or need_level > 50:
            return await message.answer('Укажите число от 1 до 50')

        await state.update_data(need_level=need_level)

        await message.answer('Сколько будет победителей?', reply_markup=keyboards.cancel_keyboard)
        await AdminCreateLot.winners_amount.set()

    except:
        return await message.answer('Укажите число от 1 до 50')


@dp.message_handler(content_types=['text'], state=AdminCreateLot.winners_amount)
async def create_lot_winners_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    try:
        winners_amount = int(message.text)

        await state.update_data(winners_amount=winners_amount)

        await message.answer('Хотите установить автоматический приз в монетах?', reply_markup=keyboards.yes_or_no_keyboard)
        await AdminCreateLot.want_add_automatic_prize.set()

    except:
        return await message.answer('Укажите число')



@dp.message_handler(content_types=['text'], state=AdminCreateLot.want_add_automatic_prize)
async def AdminCreateLot_want_add_automatic_prize(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    if message.text == 'Да':
        await message.answer('Введите сумму монет для победителя', reply_markup=keyboards.cancel_keyboard)
        await AdminCreateLot.automatic_prize_amount.set()

    elif message.text == 'Нет':
        await state.update_data(prize_amount=0)

        await message.answer('Подтвердите данные', reply_markup=keyboards.confirm_keyboard)
        await AdminCreateLot.create_lot_confirm.set()

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.yes_or_no_keyboard)


@dp.message_handler(content_types=['text'], state=AdminCreateLot.automatic_prize_amount)
async def AdminCreateLot_automatic_prize_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Добавление розыгрыша отменено', reply_markup=keyboards.main_keyboard)

    try:
        prize_amount = int(message.text)

        await state.update_data(prize_amount=prize_amount)

        await message.answer('Подтвердите данные', reply_markup=keyboards.confirm_keyboard)
        await AdminCreateLot.create_lot_confirm.set()

    except:
        return await message.answer('Введите число монет победителю числом', reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=AdminCreateLot.create_lot_confirm)
async def create_lot_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Верно':
        data = await state.get_data()
        lot_id = message.message_id
        db.add_lot(lot_id, data['name'], data['desc'], data['one_bid_price'], data['total_bids'],
                   data['need_level'], data['photo'], data['max_user_bets'], data['prize_amount'], data['winners_amount'])

        await message.answer('Розыгрыш успешно создан', reply_markup=keyboards.main_keyboard)
        await message.answer('Админ Панель', reply_markup=keyboards.admin_keyboard)

        mail_caption = f'''
{data['name']}

{data['desc']}

Успей принять участие 🤩✨
        '''
        image = data['photo']

        await state.finish()

        keyboard = keyboards.lot_keyboard(lot_id, is_admin=False)

        all_users_ids = db.get_all_users_ids()
        for user_id in all_users_ids:
            try:
                await bot.send_photo(user_id, image, mail_caption, reply_markup=keyboard)
            except Exception as ex:
                pass
        await bot.send_photo(MAIN_CHANNEL, image, mail_caption + '\n@ylionbot',
                             reply_markup=keyboards.lot_channel_keyboard(lot_id))


    else:
        await state.finish()
        await message.answer('Добавление лота отменено', reply_markup=keyboards.main_keyboard)


# Пополнение

@dp.message_handler(content_types=['text'], state=UserTopUp.get_amount)
async def TopUp_get_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Пополнение отменено', reply_markup=keyboards.main_keyboard)

    try:
        amount = int(message.text)

        if amount < 40:
            return await message.answer('Минимальная сумма пополнения -- 40 монет')

        await state.update_data(amount=amount)

        await message.answer('Выберите в какой валюте желаете провести оплату', reply_markup=keyboards.top_up_methods_keyboard)
        await UserTopUp.get_currency.set()

    except:
        await message.answer('Введите количество монет целым числом')


@dp.message_handler(content_types=['text'], state=UserTopUp.get_currency)
async def TopUp_get_currency(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Пополнение отменено', reply_markup=keyboards.main_keyboard)

    elif message.text in ['УКР 🇺🇦 Карты:', 'RU 🇷🇺 Карты:', 'TETHER $ “USDT”']:
        if message.text == 'УКР 🇺🇦 Карты:':
            currency = 'UAH'
        elif message.text == 'RU 🇷🇺 Карты:':
            currency = 'RUB'
        elif message.text == 'TETHER $ “USDT”':
            currency = 'USD'

        data = await state.get_data()

        price = data['amount'] * float(price_in_currency[currency])

        await state.update_data(price=price, currency=currency)

        await message.answer(f'''
{requisites[currency]}

Отправьте {price} {currency} на реквизиты выше.
После оплаты отправьте скриншот подтверждающий перевод.
''', reply_markup=keyboards.cancel_keyboard)
        await UserTopUp.get_confirmation.set()

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.top_up_methods_keyboard)


@dp.message_handler(content_types=['text', 'photo', 'document'], state=UserTopUp.get_confirmation)
async def TopUp_get_confirmation(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if message.text == 'Отменить':
            await state.finish()
            return await message.answer('Пополнение отменено', reply_markup=keyboards.main_keyboard)
        else:
            return await message.answer('Отправьте скриншот подтверждающий перевод.', reply_markup=keyboards.cancel_keyboard)

    elif message.content_type in ['photo', 'document']:
        data = await state.get_data()

        payment_id = message.message_id

        caption = f'''
Пользователь {db.get_user_full_name(message.chat.id)}
ID: {message.chat.id}
ID платежа: {payment_id}
Сумма в монетах: {data['amount']}
Сумма в валюте: {data['price']} {data['currency']}
        '''

        keyboard = keyboards.admin_payment_keyboard(payment_id)

        if message.content_type == 'photo':
            file_id = message.photo[0].file_id
            m = await bot.send_photo(ADMIN_CHANNEL_ID, file_id, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

        elif message.content_type == 'document':
            file_id = message.document.file_id
            m = await bot.send_document(ADMIN_CHANNEL_ID, file_id, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

        db.add_payment(payment_id, message.chat.id, data['amount'], data['price'], data['currency'], file_id,
                       message.content_type, m.message_id)

        await message.answer('Мы оповестим Вас когда оплата пройдет проверку', reply_markup=keyboards.main_keyboard)
        await state.finish()


# Вывод

@dp.message_handler(content_types=['text'], state=UserWithdrawal.get_bank_name)
async def UserWithdrawal_get_bank_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    bank_name = message.text.strip()

    await state.update_data(bank_name=bank_name)

    await UserWithdrawal.get_name.set()
    await message.answer('Введите имя получателя',
                         reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=UserWithdrawal.get_name)
async def UserWithdrawal_get_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    name = message.text.strip()

    await state.update_data(name=name)

    await UserWithdrawal.get_card.set()
    await message.answer('Введите реквизиты для перевода',
                         reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=UserWithdrawal.get_card)
async def UserWithdrawal_get_card(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    card = message.text.strip()

    await state.update_data(card=card)

    await UserWithdrawal.get_amount.set()
    await message.answer('Введите сумму вывода в YC',
                         reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=UserWithdrawal.get_amount)
async def UserWithdrawal_get_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    try:
        yc_amount = int(message.text)
    except ValueError:
        return await message.answer('''
Вы некорректно ввели число. Введите еще раз
        ''',
                                    reply_markup=keyboards.cancel_keyboard)

    if yc_amount <= 0:
        return await message.answer('Вы некорректно ввели число. Введите еще раз.',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    if yc_amount > db.get_user_balance(message.chat.id):
        return await message.answer('Недостаточно средств на балансе.\n\nВведите сумму еще раз',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    if yc_amount < 40:
        return await message.answer('Минимальная сумма для вывода -- 40 YC. Введите число еще раз',
                                    reply_markup=keyboards.cancel_keyboard)

    await state.update_data(yc_amount=yc_amount)

    await message.answer('Выберите валюту для вывода', reply_markup=keyboards.currencies_keyboard)
    await UserWithdrawal.get_currency.set()


@dp.message_handler(content_types=['text'], state=UserWithdrawal.get_currency)
async def UserWithdrawal_get_currency(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    if message.text in ['UAH', 'RUB']:
        data = await state.get_data()

        currency = message.text.strip()

        in_currency = data['yc_amount'] * float(price_in_currency[currency])
        await state.update_data(currency=currency, in_currency=in_currency)

        await message.answer(f'''
Подтвердите вывод
Сумма: {in_currency} {currency}
Реквизиты: {data["card"]}
Имя получателя: {data["name"]}
Название Банка: {data["bank_name"]}
                            ''', parse_mode='Markdown', reply_markup=keyboards.withdrawal_confirm_keyboard)

        await UserWithdrawal.get_confirm.set()

    else:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.currencies_keyboard)


@dp.message_handler(content_types=['text'], state=UserWithdrawal.get_confirm)
async def UserWithdrawal_get_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    elif message.text == 'Подтвердить вывод':
        data = await state.get_data()

        withdrawal_id = message.message_id

        db.update_user_balance(message.chat.id, -1*data['yc_amount'])

        db.add_withdrawal(withdrawal_id, message.chat.id, data['yc_amount'], data['in_currency'], data['currency'],
                          data['bank_name'], data['name'], data['card'], datetime.now())

        await bot.send_message(ADMIN_CHANNEL_ID, f'''
Заявка на вывод
Пользователь {db.get_user_full_name(message.chat.id)} (ID: {message.chat.id})
Сумма: {data['in_currency']} {data['currency']} (YC - {data['yc_amount']})
Реквизиты: {data["card"]}
Имя получателя: {data["name"]}
Название Банка: {data["bank_name"]}
ID вывода: {withdrawal_id}
                        ''', parse_mode='Markdown',
                               reply_markup=keyboards.withdrawal_admin_keyboard(withdrawal_id))

        await message.answer('Ваша заявка отправлена на выплату',
                             reply_markup=keyboards.main_keyboard, parse_mode='Markdown')
        await state.finish()

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.withdrawal_confirm_keyboard)


# Вывод G

@dp.message_handler(content_types=['text'], state=UserWithdrawalG.get_amount)
async def UserWithdrawalG_get_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    try:
        g_amount = int(message.text)
    except ValueError:
        return await message.answer('''
Вы некорректно ввели число. Введите еще раз
        ''',
                                    reply_markup=keyboards.cancel_keyboard)

    if g_amount <= 0:
        return await message.answer('Вы некорректно ввели число. Введите еще раз.',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    if g_amount < 100:
        return await message.answer('Минимальный вывод 100 G. Введите еще раз.',
                                    reply_markup=keyboards.cancel_keyboard)


    if g_amount > db.get_user_balance_G(message.chat.id):
        return await message.answer('Недостаточно средств на балансе.\n\nВведите сумму еще раз',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    await state.update_data(g_amount=g_amount)

    await message.answer(f'Подтвердите вывод {g_amount} G.', reply_markup=keyboards.withdrawal_confirm_keyboard)
    await UserWithdrawalG.get_confirm.set()


@dp.message_handler(content_types=['text'], state=UserWithdrawalG.get_confirm)
async def UserWithdrawalG_get_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Вывод отменен', reply_markup=keyboards.main_keyboard)

    elif message.text == 'Подтвердить вывод':
        data = await state.get_data()

        db.update_user_balance_G(message.chat.id, -1*data['g_amount'])

        await bot.send_message(ADMIN_CHANNEL_ID, f'''
Заявка на вывод G
Сумма: {data['g_amount']}
Пользователь {db.get_user_full_name(message.chat.id)} (ID: {message.chat.id})
                        ''', parse_mode='Markdown',
                               reply_markup=None)

        await message.answer('Ваша заявка отправлена менеджеру',
                             reply_markup=keyboards.main_keyboard, parse_mode='Markdown')
        await state.finish()

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.withdrawal_confirm_keyboard)


# Написание отзыва

@dp.message_handler(content_types=['text'], state=UserWriteReview.get_text)
async def UserWriteReview_get_text(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    await message.forward(ORDERS_CHANNEL_ID)
    await state.finish()
    await message.answer('Спасибо за отзыв', reply_markup=keyboards.main_keyboard)

    db.add_review(message.chat.id, message.text)


# Создание дуэли

@dp.message_handler(content_types=['text'], state=UserDuelsRegistration.st_id)
async def UserDuelsRegistration_st_id(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    await state.update_data(st_id=message.text)

    await message.answer('В каком режиме предпочитаете играть?', reply_markup=keyboards.game_modes_keyboard)
    await UserDuelsRegistration.game_mode.set()


@dp.message_handler(content_types=['text'], state=UserDuelsRegistration.game_mode)
async def UserDuelsRegistration_game_mode(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    if message.text not in ['Командный Бой', 'Союзники', 'Соревновательный', 'Эскалация', 'Гонка вооружений', 'Аркада']:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.game_modes_keyboard)

    await state.update_data(game_mode=message.text)

    await message.answer('Укажите свой Ранг', reply_markup=keyboards.st_ranks_keyboard)
    await UserDuelsRegistration.st_rank.set()


@dp.message_handler(content_types=['text'], state=UserDuelsRegistration.st_rank)
async def UserDuelsRegistration_st_rank(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    if message.text not in ['BRONZE I','BRONZE II','BRONZE III','BRONZE IV','SILVER I','SILVER II','SILVER III','SILVER IV','GOLD I','GOLD II','GOLD III','GOLD IV','PHOENIX','RANGER','CHAMPION','MASTER','ELITE','THE LEGEND']:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.st_ranks_keyboard)

    await state.update_data(st_rank=message.text)

    await message.answer('Укажите количество YC для ставки', reply_markup=keyboards.cancel_keyboard)
    await UserDuelsRegistration.bet.set()


@dp.message_handler(content_types=['text'], state=UserDuelsRegistration.bet)
async def UserDuelsRegistration_bet(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        bet_amount = int(message.text)
    except ValueError:
        return await message.answer('''
Введите ставку числом.
        ''',
                                    reply_markup=keyboards.cancel_keyboard)

    if bet_amount < 0:
        return await message.answer('Вы некорректно ввели число. Введите еще раз.',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    if bet_amount > db.get_user_balance(message.chat.id):
        return await message.answer('Недостаточно средств на балансе.\n\nВведите сумму ставки еще раз',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    await state.update_data(bet=bet_amount)

    await message.answer('Ваш Ник в Standoff2', reply_markup=keyboards.cancel_keyboard)
    await UserDuelsRegistration.st_name.set()


@dp.message_handler(content_types=['text'], state=UserDuelsRegistration.st_name)
async def UserDuelsRegistration_st_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    await state.update_data(st_name=message.text)

    data = await state.get_data()

    await message.answer('Подтвердите данные дуэли:')
    await message.answer(f'''
ID в Standoff2: {data["st_id"]}
Предпочитаемый режим игры: {data["game_mode"]}
Ваш Ранг: {data["st_rank"]}
Сумма ставки YC: {data["bet"]}
Ник в Standoff2: {data["st_name"]}
    ''', reply_markup=keyboards.duels_confirm_keyboard)

    await UserDuelsRegistration.confirm.set()


@dp.message_handler(content_types=['text'], state=UserDuelsRegistration.confirm)
async def UserDuelsRegistration_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    elif message.text == 'Опубликовать':
        data = await state.get_data()

        if data['bet'] > db.get_user_balance(message.chat.id):
            await state.finish()
            return await message.answer('Недостаточно средств на балансе. Попробуйте заново',
                                        reply_markup=keyboards.main_keyboard, parse_mode='Markdown')

        duel_id = message.message_id
        db.add_duel(duel_id, message.chat.id, data['bet'], data['st_id'], data['game_mode'], data['st_rank'], data['st_name'], 'wait')
        db.update_user_balance(message.chat.id, -1*data['bet'])

        await state.finish()
        await message.answer(f'Дуэль номер {duel_id} создана', reply_markup=keyboards.main_keyboard)
    else:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.duels_confirm_keyboard)


# Дуэль заполнение заявки участвия

@dp.message_handler(content_types=['text'], state=UserDuelTakePart.st_id)
async def UserDuelTakePart_st_id(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    await state.update_data(st_id=message.text)

    await message.answer('Укажите свой Ранг', reply_markup=keyboards.st_ranks_keyboard)
    await UserDuelTakePart.st_rank.set()


@dp.message_handler(content_types=['text'], state=UserDuelTakePart.st_rank)
async def UserDuelTakePart_st_rank(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    if message.text not in ['BRONZE I','BRONZE II','BRONZE III','BRONZE IV','SILVER I','SILVER II','SILVER III','SILVER IV','GOLD I','GOLD II','GOLD III','GOLD IV','PHOENIX','RANGER','CHAMPION','MASTER','ELITE','THE LEGEND']:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.st_ranks_keyboard)

    await state.update_data(st_rank=message.text)

    await message.answer('Ваш Ник в Standoff2', reply_markup=keyboards.cancel_keyboard)
    await UserDuelTakePart.st_name.set()


@dp.message_handler(content_types=['text'], state=UserDuelTakePart.st_name)
async def UserDuelTakePart_st_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    await state.update_data(st_name=message.text)

    data = await state.get_data()
    await state.finish()

    db.add_duel_request(data['duel_id'], message.chat.id, data['st_id'], data['st_rank'], data['st_name'])

    try:
        await bot.send_message(db.get_duel_creator_id(data['duel_id']), f'''
Заявка на дуэль #{data['duel_id']}
{db.get_duel_bet(data['duel_id'])} YC | {db.get_duel_game_mode(data['duel_id'])}

Противник: 
ID в Standoff2: {data['st_id']}
Ранг: {data['st_rank']}
Ник в Standoff2: {data['st_name']}
        ''', reply_markup=keyboards.duel_request_keyboard(data['duel_id'], message.chat.id))

    except:
        pass

    await message.answer('Заявка отправлена', reply_markup=keyboards.main_keyboard)


# Обмен YC на G

@dp.message_handler(content_types=['text'], state=UserChangeYcToG.amount)
async def UserChangeYcToG_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        yc_amount = int(message.text)
    except ValueError:
        return await message.answer('''
Вы некорректно ввели число. Введите еще раз
        ''',
                                    reply_markup=keyboards.cancel_keyboard)

    if yc_amount == 0:
        return await message.answer('Вы некорректно ввели число. Введите еще раз.',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    if yc_amount > db.get_user_balance(message.chat.id):
        return await message.answer('Недостаточно средств на балансе.\n\nВведите сумму еще раз',
                                    reply_markup=keyboards.cancel_keyboard, parse_mode='Markdown')

    await state.update_data(yc_amount=yc_amount)
    await message.answer(f'''
Вы действительно хотите обменять {yc_amount} YC на {round(yc_amount * float(price_in_currency["G"]), 2)} G?
    ''', reply_markup=keyboards.confirm_keyboard)
    await UserChangeYcToG.confirm.set()


@dp.message_handler(content_types=['text'], state=UserChangeYcToG.confirm)
async def UserChangeYcToG_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Обмен отменен', reply_markup=keyboards.main_keyboard)

    elif message.text == 'Верно':
        data = await state.get_data()

        yc_amount = data['yc_amount']
        g_amount = round(yc_amount * float(price_in_currency["G"]), 2)

        db.update_user_balance(message.chat.id, -1*data['yc_amount'])
        db.update_user_balance_G(message.chat.id, g_amount)

        await message.answer('Обмен совершен',
                             reply_markup=keyboards.main_keyboard, parse_mode='Markdown')
        await state.finish()

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.confirm_keyboard)




# Начисление админом

@dp.message_handler(content_types=['text'], state=AdminTopUp.get_amount)
async def AdminTopUp_get_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        yc_amount = int(message.text)
    except Exception as ex:
        return await message.answer('Введите число', reply_markup=keyboards.cancel_keyboard)

    data = await state.get_data()

    payment_data = db.get_payment_data(data['payment_id'])
    mes_in_channel_id = payment_data[8]

    await successful_payment(data['payment_id'], data['user_id'], yc_amount)

    try:
        await bot.edit_message_reply_markup(ADMIN_CHANNEL_ID, message_id=mes_in_channel_id,
                                            reply_markup=keyboards.payment_confirmed_by_hands)
    except:
        pass

    await message.answer('Платеж зачислен пользователю', reply_markup=keyboards.main_keyboard)
    await state.finish()



# Назначение победителя розыгрыша

@dp.message_handler(content_types=['text'], state=AdminSetWinner.get_id_or_username)
async def AdminSetWinner_get_id_or_username(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    message.text = message.text.strip()
    if message.text.startswith('@'):
        message.text = message.text.replace('@', '')

    search_user = db.search_user(message.text)

    if not search_user:
        return await message.answer('Пользователя не найдено. Введите еще раз', reply_markup=keyboards.cancel_keyboard)

    await message.answer(f'''
Пользователь найден ({message.text})

{db.get_user_full_name(search_user)}
    ''', parse_mode='Markdown')

    await state.update_data(winner_id=search_user)

    await message.answer('Подтвердите победителя', reply_markup=keyboards.confirm_keyboard)
    await AdminSetWinner.confirm.set()


@dp.message_handler(content_types=['text'], state=AdminSetWinner.confirm)
async def AdminSetWinner_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    elif message.text == 'Верно':
        data = await state.get_data()

        lot_id = data['lot_id']
        lot_data = db.get_lot_data(lot_id)

        status = lot_data[8]

        if not lot_data:
            return await message.answer('Lot_id не найден')

        if status != 'active':
            return await message.answer('Этот розыгрыш уже закончен')

        await set_winner(lot_id, winner_id=data['winner_id'])

        mes_id_in_channel = db.get_lot_mes_id_in_channel(lot_id)

        try:
            await bot.edit_message_caption(ADMIN_CHANNEL_ID, mes_id_in_channel,
                                           caption=f'Победитель выбран, им стал -- {db.get_user_full_name(data["winner_id"])}',
                                           reply_markup=None, parse_mode='Markdown')
        except:
            pass

        await state.finish()
        await message.answer('Победитель выбран', reply_markup=keyboards.main_keyboard)

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.confirm_keyboard)



# Изминение данных пользователя

@dp.message_handler(content_types=['text'], state=AdminEditUserData.get_user_id)
async def AdminEditUserData_get_user_id(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Дейтвие отменено', reply_markup=keyboards.main_keyboard)

    search_user = db.search_user(message.text.strip())

    if not search_user:
        return await message.answer('Пользователя не найдено. Введите еще раз', reply_markup=keyboards.cancel_keyboard)

    user_balance = db.get_user_balance(search_user)
    user_level = db.get_user_level(search_user)

    is_baned_user = db.is_baned_user(search_user)

    if is_baned_user:
        baned_text = 'Забанен'
    else:
        baned_text = 'Без бана'

    await message.answer(f'''
Пользователь найден ({message.text})

{db.get_user_full_name(search_user)}

Баланс: {user_balance} YC
Уровень: {user_level}

{baned_text}
        ''', parse_mode='Markdown', reply_markup=keyboards.admin_edit_user_data(search_user))

    await state.finish()


@dp.message_handler(content_types=['text'], state=AdminEditUserData.balance)
async def AdminEditUserData_balance(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        new_balance = float(message.text)
    except:
        return await message.answer('Введите новый баланс числом', reply_markup=keyboards.cancel_keyboard)

    db.set_user_balance(data['user_id'], new_balance)

    await state.finish()
    await message.answer(f'Новый баланс пользователя: {new_balance}', reply_markup=keyboards.main_keyboard)


@dp.message_handler(content_types=['text'], state=AdminEditUserData.level)
async def AdminEditUserData_level(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        new_level = int(message.text)
    except:
        return await message.answer('Введите новый баланс числом', reply_markup=keyboards.cancel_keyboard)

    db.set_user_level(data['user_id'], new_level)

    await state.finish()
    await message.answer(f'Новый уровень пользователя: {new_level}')



# Изминения данных бота

@dp.message_handler(content_types=['text'], state=AdminEditBotData.edit_help_link)
async def AdminEditBotData_edit_help_link(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    if message.text.startswith('@'):
        message.text = message.text.replace('@', 'https://t.me/')

    new_help_link = message.text

    try:
        await message.answer('Тест', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Связаться с тех. поддержкой', url=new_help_link)))

        global help_link
        help_link = new_help_link

        with sqlite3.connect(info_db) as con:
            cursor = con.cursor()

            cursor.execute('UPDATE help_link SET text = (?)', (help_link,))

        await message.answer('Новая ссылка установлена', reply_markup=keyboards.main_keyboard)
        await state.finish()

    except:
        return await message.answer('Ссылка или юзернейм не верные. Отправьте еще раз', reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=AdminEditBotData.edit_help_text)
async def AdminEditBotData_edit_help_text(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    new_help_text = message.text

    global help_text

    help_text = new_help_text

    with sqlite3.connect(info_db) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE help_text SET text = (?)', (help_text,))

    await message.answer('Новые Правила установлены', reply_markup=keyboards.main_keyboard)
    await state.finish()


@dp.message_handler(content_types=['text'], state=AdminEditBotData.edit_requisites_type)
async def AdminEditBotData_edit_requisites_type(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    if message.text in ['UAH', 'RUB', 'USD']:
        currency = message.text
        await state.update_data(currency=currency)
        await message.answer(f'Выбраная валюта: {currency}')

        await message.answer('Введите новые реквизиты для этой валюты', reply_markup=keyboards.cancel_keyboard)
        await AdminEditBotData.edit_requisites_data.set()

    else:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.all_currencies_keyboard)


@dp.message_handler(content_types=['text'], state=AdminEditBotData.edit_requisites_data)
async def AdminEditBotData_edit_requisites_data(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    data = await state.get_data()

    new_requisites = message.text.strip()

    global requisites
    requisites[data['currency']] = new_requisites

    with sqlite3.connect(info_db) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE requisites SET data = (?) WHERE currency = (?)', (new_requisites, data['currency']))

    await message.answer(f'Новая реквизиты для {data["currency"]} установлены', reply_markup=keyboards.main_keyboard)
    await state.finish()


@dp.message_handler(content_types=['text'], state=AdminEditBotData.edit_in_currency_type)
async def AdminEditBotData_edit_in_currency_type(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    if message.text in ['UAH', 'RUB', 'USD', 'G']:
        currency = message.text
        await state.update_data(currency=currency)
        await message.answer(f'Выбраная валюта: {currency}')

        await message.answer('Введите новый курс 1 YC = фиата в этой валюте. Введите только число', reply_markup=keyboards.cancel_keyboard)
        await AdminEditBotData.edit_in_currency_data.set()

    else:
        return await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.all_currencies_keyboard)


@dp.message_handler(content_types=['text'], state=AdminEditBotData.edit_in_currency_data)
async def AdminEditBotData_edit_in_currency_data(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    data = await state.get_data()

    try:
        new_price_in_currency = float(message.text)
    except:
        return await message.answer('Введите число', reply_markup=keyboards.cancel_keyboard)

    global price_in_currency
    price_in_currency[data['currency']] = new_price_in_currency

    with sqlite3.connect(info_db) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE price_in_currency SET data = (?) WHERE currency = (?)', (new_price_in_currency, data['currency']))

    await message.answer(f'Новая цена 1 YC = {new_price_in_currency} {data["currency"]} установлена', reply_markup=keyboards.main_keyboard)
    await state.finish()



# Рассылка

@dp.message_handler(content_types=['photo', 'video', 'text'], state=AdminMail.get_data)
async def admin_get_data(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if message.text == 'Отменить':
            await state.finish()
            return await message.answer('Рассылка отменена', reply_markup=keyboards.main_keyboard)

        else:
            async with state.proxy() as data:
                data['content_type'] = 'text'
                data['text'] = message.text
                data['entities'] = message.entities

    elif message.content_type == 'photo':
        async with state.proxy() as data:
            data['content_type'] = 'photo'
            data['file_id'] = message.photo[0].file_id
            data['caption'] = message.caption
            data['entities'] = message.caption_entities

    elif message.content_type == 'video':
        async with state.proxy() as data:
            data['content_type'] = 'video'
            data['file_id'] = message.video.file_id
            data['caption'] = message.caption
            data['entities'] = message.caption_entities

    await AdminMail.confirm.set()
    await message.answer('Подтвердите рассылку', reply_markup=keyboards.confirm_keyboard)


@dp.message_handler(state=AdminMail.confirm)
async def admin_get_data(message: types.Message, state: FSMContext):
    if message.text != 'Верно':
        await state.finish()
        return await message.answer('Рассылка отменена', reply_markup=keyboards.main_keyboard)

    all_users_ids = db.get_all_users_ids()
    await message.answer(f'Рассылка началась для {len(all_users_ids)} пользователей', reply_markup=keyboards.main_keyboard)

    not_active_users = []

    data = await state.get_data()
    await state.finish()

    if data['content_type'] == 'text':
        for user_id in all_users_ids:
            try:
                await bot.send_message(user_id, data['text'], entities=data['entities'])
            except:
                not_active_users.append(user_id)

    elif data['content_type'] == 'photo':
        for user_id in all_users_ids:
            try:
                await bot.send_photo(user_id, data['file_id'], caption=data["caption"],
                                     caption_entities=data['entities'])
            except:
                not_active_users.append(user_id)

    elif data['content_type'] == 'video':
        for user_id in all_users_ids:
            try:
                await bot.send_video(user_id, data['file_id'], caption=data["caption"],
                                     caption_entities=data['entities'])
            except:
                not_active_users.append(user_id)

    await message.answer('Рассылка окончена')
    await message.answer(f'Рассылку не получили {len(not_active_users)}.\nВсего активных пользователей перед рассылкой {len(all_users_ids)}')



# Создание промокода

@dp.message_handler(content_types=['text'], state=AdminAddPromoCode.promo_type)
async def AdminAddPromoCode_promo_type(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    elif message.text in ['Начисление', 'Процент к пополнению']:
        if message.text == 'Начисление':
            promo_type = 'bonus'
        elif message.text == 'Процент к пополнению':
            promo_type = 'percent'

        await state.update_data(promo_type=promo_type)
        await AdminAddPromoCode.amount.set()
        await message.answer('Введите число', reply_markup=keyboards.cancel_keyboard)

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.promo_code_types_keyboard)


@dp.message_handler(content_types=['text'], state=AdminAddPromoCode.amount)
async def AdminAddPromoCode_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        amount = int(message.text)

        await state.update_data(amount=amount)
        await AdminAddPromoCode.name.set()
        await message.answer('Назвите промокод', reply_markup=keyboards.cancel_keyboard)


    except:
        await message.answer('Введите число еще раз', reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=AdminAddPromoCode.name)
async def AdminAddPromoCode_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    name = message.text
    await state.update_data(name=name)

    await AdminAddPromoCode.activations.set()
    await message.answer('Введите количество активаций промокода', reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=AdminAddPromoCode.activations)
async def AdminAddPromoCode_activations(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        activations = int(message.text)
    except:
        return await message.answer('Введите число', reply_markup=keyboards.cancel_keyboard)


    await state.update_data(activations=activations)

    data = await state.get_data()

    if data['promo_type'] == 'bonus':
        promo_type_text = 'Начисление'
    elif data['promo_type'] == 'percent':
        promo_type_text = 'Процент к пополнению'
    else:
        promo_type_text = 'Не определено'

    await message.answer(f'''
Подтвердите данные:

Промокод: {data['name']}
Тип: {promo_type_text}
Число монет/%к поплнению: {data['amount']}
Количество активаций: {data['activations']}

''', reply_markup=keyboards.confirm_keyboard)

    await AdminAddPromoCode.confirm.set()


@dp.message_handler(content_types=['text'], state=AdminAddPromoCode.confirm)
async def AdminAddPromoCode_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    elif message.text == 'Верно':
        data = await state.get_data()

        is_promo = db.get_promo_code_data(data['name'])

        if is_promo:
            await state.finish()
            await message.answer('Такой промокод уже был создан. Начните заново', reply_markup=keyboards.main_keyboard)
        else:
            db.add_promo_code(message.message_id, data['name'], data['promo_type'], data['amount'], data['activations'])

            await state.finish()
            await message.answer('Промокод добавлен', reply_markup=keyboards.main_keyboard)

    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=keyboards.confirm_keyboard)


@dp.message_handler(content_types=['text'], state=AdminEditPromo.activations)
async def AdminEditPromo_activations(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        activations = int(message.text)

        data = await state.get_data()

        db.update_promo_code_activations(data['promo_id'], activations)

        await state.finish()

        await message.answer('Промокод обновлен', reply_markup=keyboards.main_keyboard)

    except:
        await message.answer('Введите число', reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=AdminEditPromo.amount)
async def AdminEditPromo_amount(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    try:
        amount = int(message.text)

        data = await state.get_data()

        db.update_promo_code_amount(data['promo_id'], amount)

        await state.finish()

        await message.answer('Промокод обновлен', reply_markup=keyboards.main_keyboard)

    except:
        await message.answer('Введите число', reply_markup=keyboards.cancel_keyboard)


@dp.message_handler(content_types=['text'], state=UserPromoCode.name)
async def UserPromoCode_name(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    name = message.text

    promo_data = db.get_promo_code_data(name)

    if promo_data:
        promo_id, name, promo_type, amount, activations, members = promo_data
        members_list = members.split(',')

        if len(members_list) - 1 >= activations:
            await state.finish()
            return await message.answer('Этот промокод уже был активирован максимальное количество раз',
                                        reply_markup=keyboards.main_keyboard)

        if str(message.chat.id) in members_list:
            await state.finish()
            return await message.answer('Вы уже активировали этот промокод',
                                        reply_markup=keyboards.main_keyboard)

        if promo_type == 'bonus':
            db.update_user_balance(message.chat.id, amount)

            members_list.append(str(message.chat.id))
            db.add_promo_activation(name, ','.join(members_list))

            await message.answer(f'Промокод успешно активирован. На Ваш баланс начислено {amount} YC',
                                 reply_markup=keyboards.main_keyboard)

        elif promo_type == 'percent':
            if db.get_user_active_promo_code(message.chat.id):
                await state.finish()
                return await message.answer('У вас уже есть активный промокод, который дает бонус к пополнению',
                                            reply_markup=keyboards.main_keyboard)

            db.update_user_active_promo_code(message.chat.id, name)
            members_list.append(str(message.chat.id))
            db.add_promo_activation(name, ','.join(members_list))

            await message.answer(f'Промокод успешно активирован. Он даст Вам бонус к пополнению {amount}%',
                                 reply_markup=keyboards.main_keyboard)

        else:
            await message.answer('Промокод не опознан', reply_markup=keyboards.main_keyboard)
    else:
        await message.answer('Такого промокода не существует', reply_markup=keyboards.main_keyboard)

    await state.finish()


# Поиск дуэли

@dp.message_handler(content_types=['text'], state=AdminDuelInfo.duel_id)
async def AdminDuelInfo_duel_id(message: types.Message, state: FSMContext):
    if message.text == 'Отменить':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=keyboards.main_keyboard)

    message.text = message.text.replace('#', '')
    duel_id = message.text

    duel_info = db.get_duel_info(duel_id)

    if not duel_info:
        return await message.answer('Дуэль не найдена. Введите номер дуэли еще раз', reply_markup=keyboards.cancel_keyboard)

    duel_id, user_first, user_second, bet, st_id, game_mode, st_rank, st_name, status, winnner = duel_info

    player_one_info = db.duel_player_info(duel_id, user_first)
    st_id, st_rank, st_name = player_one_info
    user_result = db.duel_get_user_result(duel_id, user_first=user_first)

    if user_result == 'win':
        user_result = 'Выигрыш'
    elif user_result == 'lose':
        user_result = 'Проигрыш'
    else:
        user_result = 'Не указан'

    data = {}
    data.update(
        {
            user_first: {
                'st_id': st_id,
                'st_rank': st_rank,
                'st_name': db.filter_text_markdown(st_name),
                'result': user_result
            }
        })

    player_two_info = db.duel_player_info(duel_id, user_second)
    st_id, st_rank, st_name = player_two_info
    user_result = db.duel_get_user_result(duel_id, user_second=user_second)

    if user_result == 'win':
        user_result = 'Выигрыш'
    elif user_result == 'lose':
        user_result = 'Проигрыш'
    else:
        user_result = 'Не указан'

    data.update(
        {
            user_second: {
                'st_id': st_id,
                'st_rank': st_rank,
                'st_name': db.filter_text_markdown(st_name),
                'result': user_result
            }
        })

    await state.finish()

    status = db.get_duel_status(duel_id)
    if status == 'progress':
        keyboard = keyboards.admin_duel_set_result(duel_id)
    else:
        keyboard = None

    if status == 'wait':
        duel_status_label = 'Статус дуэли: Создана'
    elif status == 'progress':
        duel_status_label = 'Статус дуэли: В процессе'
    elif status == 'end':
        duel_status_label = 'Статус дуэли: Закончена'
    else:
        duel_status_label = ''

    await message.answer('Информация о дуэли:', reply_markup=keyboards.main_keyboard)
    await message.answer(f'''
Дуэль #{duel_id}
Предпочитаемый режим игры: {game_mode}
Сумма ставки YC: {bet}
{duel_status_label}

Игрок 1:
{db.get_user_full_name(user_first)}
ID в Standoff2: {data[user_first]['st_id']}
Ранг: {data[user_first]['st_rank']}
Ник в Standoff2: {data[user_first]['st_name']}
Выставленный резулат: {data[user_first]['result']}

Игрок 2:
{db.get_user_full_name(user_second)}
ID в Standoff2: {data[user_second]['st_id']}
Ранг: {data[user_second]['st_rank']}
Ник в Standoff2: {data[user_second]['st_name']}
Выставленный резулат: {data[user_second]['result']}

    ''', parse_mode='Markdown', reply_markup=keyboard)
    await state.finish()


async def successful_payment(payment_id, user_id, yc_amount, promo_bonus=False):
    payment_data = db.get_payment_data(payment_id)

    status = payment_data[5]

    if status != 'created':
        return

    db.update_user_balance(user_id, yc_amount)
    db.update_payment_status(payment_id, 'confirmed')

    try:
        await bot.send_message(user_id, f'''
Платеж №{payment_id} прошел успешно
На Ваш баланс начислено {yc_amount} монет
                        ''')
    except:
        pass

    if promo_bonus:
        db.update_user_balance(user_id, yc_amount)
        try:
            await bot.send_message(user_id, f'''
За ранее введенный промокод на Ваш баланс начислено {yc_amount} монет.
                            ''')
        except:
            pass

    referrer_id = db.check_referral(user_id)
    if referrer_id:
        try:
            await bot.send_message(referrer_id, f'Ваш реферал {db.get_user_full_name(user_id)} сделал пополнение. Вам начислено 2 YLION COIN',
                                   parse_mode='Markdown')
        except:
            pass


async def send_active_lots(message, page, user_lots=False):
    active_lots = db.get_active_lots(user_lots=user_lots)

    if not active_lots:
        return await message.answer('Сейчас нет активных розыгрышей')

    if page == -1:
        return

    if page+1 > ceil(len(active_lots)/PAGINATION_ACTIVE_LOTS):
        return

    if active_lots:
        keyboard = keyboards.active_lots_keyboard(active_lots, page, user_lots=user_lots)
        try:
            await message.edit_reply_markup(reply_markup=keyboard)
        except:
            await message.answer('Список активных розыгрышей', reply_markup=keyboard)
    else:
        await message.answer('Сейчас нет активных розыгрышей')


async def send_duels_list(message, page, free=False):
    active_duels = db.get_active_duels(free)

    if not active_duels:
        return await message.answer('Сейчас нет дуэлей')

    if page == -1:
        return

    if page+1 > ceil(len(active_duels)/10):
        return

    if active_duels:
        keyboard = keyboards.list_duels_keyboard(active_duels, page=page, free=free)
        try:
            await message.edit_reply_markup(reply_markup=keyboard)
        except:
            await message.answer('Список дуэлей', reply_markup=keyboard)
    else:
        await message.answer('Сейчас нет дуэлей')


def lot_text(name, description, one_bid_price, now_bids, total_bids, need_level, user_bids_count):
    if one_bid_price == 0:
        one_bid_price = 'Бесплатно'

    return f'''
{name}

{description}

Стоимость участия: {one_bid_price}
Количество участников: {now_bids} из {total_bids}

Уровень требуемый для участия: {need_level}

Ваших участий: {user_bids_count}
        '''


async def set_winner(lot_id, winner_id):
    db.set_complete_lot(lot_id, winner_id)

    await send_winner_message(lot_id, winner_id)
    await automatic_prize(lot_id, winner_id)
    await send_winner_post(lot_id, winner_id)


async def set_winners(lot_id, winners_ids):
    db.set_complete_lot(lot_id, ','.join(winners_ids))

    for winner_id in winners_ids:
        await send_winner_message(lot_id, winner_id)
        await automatic_prize(lot_id, winner_id)
        await send_winners_post(lot_id, winners_ids)


async def send_winner_post(lot_id, winner_id):
    lot_data = db.get_lot_data(lot_id)

    full_name = db.get_user_full_name(winner_id)

    name = lot_data[1]
    image = lot_data[6]

    caption = f'''
В розыгрыше {name} победителем стал пользователь {full_name}
    '''

    await bot.send_photo(MAIN_CHANNEL, image, caption=caption, parse_mode='Markdown')


async def send_winners_post(lot_id, winners_ids):
    lot_data = db.get_lot_data(lot_id)

    full_names = '\n'.join(list(map(db.get_user_full_name, winners_ids)))

    name = lot_data[1]
    image = lot_data[6]

    caption = f'''
В розыгрыше {name} победителями стали пользователи:\n\n{full_names}
    '''

    await bot.send_photo(MAIN_CHANNEL, image, caption=caption, parse_mode='Markdown')


async def send_winner_message(lot_id, winner_id):
    lot_data = db.get_lot_data(lot_id)

    name = lot_data[1]
    image = lot_data[6]

    caption = f'''
Поздравляем
Вы стали победителем в розыгрыше {name}
    '''

    try:
        await bot.send_photo(winner_id, image, caption=caption, parse_mode='Markdown')
    except:
        full_name = db.get_user_full_name(winner_id)

        await bot.send_message(ADMIN_CHANNEL_ID, f'Не удалось отправить сообщение о победе пользователю {full_name}. Победителю розыгрыша {name}',
                               parse_mode='Markdown')


async def automatic_prize(lot_id, winner_id):
    lot_data = db.get_lot_data(lot_id)

    prize_amount = lot_data[13]

    if prize_amount > 0:
        db.update_user_balance(winner_id, prize_amount)

        try:
            await bot.send_message(winner_id, f'Вам насчитан приз {prize_amount} YC')
        except:
            pass


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext):
    if ' ' in message.text:
        if 'payment_id' in message.text and message.chat.id in ADMIN_IDS:
            payment_id = message.text.split('payment_id=')[1]
            payment_data = db.get_payment_data(payment_id)

            if not payment_data:
                return await message.answer('Payment_id не найден')

            user_id = payment_data[1]

            await state.update_data(user_id=user_id, payment_id=payment_id)

            await message.answer(f'''
Пользователь {db.get_user_full_name(user_id)}

Введите сумму монет которую нужно пополнить
            ''', parse_mode='Markdown', reply_markup=keyboards.cancel_keyboard)

            return await AdminTopUp.get_amount.set()

        elif 'set_winner_lot_id' in message.text and message.chat.id in ADMIN_IDS:
            lot_id = message.text.split('set_winner_lot_id=')[1]
            lot_data = db.get_lot_data(lot_id)

            name = lot_data[1]
            status = lot_data[8]

            if not lot_data:
                return await message.answer('Lot_id не найден')

            if status != 'active':
                return await message.answer('Этот розыгрыш уже закончен')

            await state.update_data(lot_id=lot_id)

            await message.answer(f'''
Розыгрыш {name}

Введите id или юзернейм победителя
                        ''', parse_mode='Markdown', reply_markup=keyboards.cancel_keyboard)

            return await AdminSetWinner.get_id_or_username.set()


        else:
            try:
                referrer_id = int(message.text.split(' ', maxsplit=1)[1])
                referral_id = message.chat.id
                if referrer_id != referral_id:
                    db.add_referral(referral_id, referrer_id)
            except:
                pass

    db.add_new_user(message.chat.id,
                    message.from_user.first_name,
                    message.from_user.last_name if message.from_user.last_name else '',
                    message.from_user.username if message.from_user.username else ''
                    )

    await message.answer('''
Мы рады приветствовать вас ✨⚔️

У нас весело 🤩 и очень Интересно ⚔️

💎 Ежедневные розыгрыши на скины , Голду и YLION Коины 🔥

💎 Крутой функционал Дуэлей, где вы можете сражаться с друзьями и с незнакомыми игроками со всего мира , делая ставки на YC , или играть бесплатно ⚔️

А в планах усовершенствоваться до самого функционального бота в Standoff 2 🔫

💕Надеемся вам у нас понравится 

                                      Ваш GM YLION
    ''', reply_markup=keyboards.main_keyboard)


@dp.message_handler(commands=['admin'], state='*')
async def admin_command(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_IDS:
        await message.answer('Админ Панель', reply_markup=keyboards.admin_keyboard)
    elif message.chat.id in MANAGER_IDS:
        await message.answer('Панель менеджера', reply_markup=keyboards.manager_keyboard)


@dp.message_handler(content_types=['text'], state='*')
async def text_worker(message: types.Message, state: FSMContext):
    # if message.chat.type == 'supergroup':
    #     if message.chat.id == ORDERS_CHAT_ID:
    #         chat_status = await bot.get_chat_member(ORDERS_CHAT_ID, message.from_user.id)
    #
    #         if chat_status.status not in ['creator', 'administrator']:
    #             await bot.restrict_chat_member(ORDERS_CHAT_ID, message.from_user.id,
    #                                            permissions=types.ChatPermissions(can_send_messages=False))

    if message.chat.type != 'private':
        return

    db.add_new_user(message.chat.id,
                    message.from_user.first_name,
                    message.from_user.last_name if message.from_user.last_name else '',
                    message.from_user.username if message.from_user.username else ''
                    )

    if message.text == 'РОЗЫГРЫШИ':
        await send_active_lots(message, 0)

    elif message.text == 'ДУЭЛЬ':
        await message.answer('Дуэли', reply_markup=keyboards.duels_keyboard)

    elif message.text == 'ПРОФИЛЬ':
        user_balance = db.get_user_balance(message.chat.id)
        user_balance_G = db.get_user_balance_G(message.chat.id)
        user_level = db.get_user_level(message.chat.id)
        user_participation = db.get_user_participation(message.chat.id)

        await message.answer(f'''
Профиль

Ваш ID: {message.chat.id}

Баланс YC: {user_balance}
Баланс G: {user_balance_G}

Уровень: {user_level}

Участий в конкурсах: {user_participation}
        ''', reply_markup=keyboards.cabinet_keyboard)

    elif message.text == 'ТОП 10':
        top_users = db.get_top_users_spent_balance()
        top_donates_users = db.get_top_users_donations()
        top_duel_winners = db.get_top_duel_winners()

        text = 'Топ 10 Игроков в Дуэли:\n\n'

        n = 1
        for user_id, amount in top_duel_winners:

            text += f'{n}) {db.get_user_full_name(user_id)} -- {amount} побед\n'
            n += 1

        text += '\n\nТоп 10 участников по донатам (YC):\n\n'

        n = 1
        for user_id, amount in top_donates_users:
            text += f'{n}) {db.get_user_full_name(user_id)} -- {amount} YC\n'
            n += 1

        text += '\n\nТоп 10 участников по потраченым YC:\n\n'

        n = 1
        for user_id, amount in top_users:
            text += f'{n}) {db.get_user_full_name(user_id)} -- {amount} YC\n'
            n += 1

        await message.answer(text, parse_mode='Markdown')

    elif message.text == 'ПРОМОКОД':
        await UserPromoCode.name.set()
        await message.answer('Введите промокод', reply_markup=keyboards.cancel_keyboard)

    elif message.text == 'РЕФЕРАЛЬНАЯ СИСТЕМА':
        referrals_count, bonus = db.user_referral_info(message.chat.id)

        await message.answer(f'''
Ваша реферальная ссылка:
https://t.me/{bot_username}?start={message.chat.id}

Количество рефералов: {referrals_count}

Реферальный доход: {bonus}
            ''', )

    elif message.text == 'ПРАВИЛА':
        await message.answer(help_text)

    elif message.text == 'КАК ПОЛЬЗОВАТЬСЯ БОТОМ':
        await message.answer(how_use_bot_text)

    elif message.text == 'ПОДДЕРЖКА':
        await message.answer('''
Часы Работы Поддержки ежедневно с 08:00 до 00:00 
        ''', reply_markup=keyboards.help_contact(help_link))

    elif message.text == 'ОТЗЫВЫ':
        review = db.get_review(message.chat.id)

        await message.answer(f'''
Переходите в канал с отзывами по ссылке:
{ORDERS_CHAT_LINK}
        ''', reply_markup=keyboards.orders_chat_keyboard(review))

    else:
        await message.answer('Главное меню', reply_markup=keyboards.main_keyboard)


@dp.callback_query_handler(lambda call: True, state='*')
async def callback_worker(call: types.CallbackQuery, state: FSMContext):
    if call.data.startswith('admin'):
        if call.data == 'admin_create_lot':
            await call.message.delete()
            await call.message.answer('Введите название розыгрыша', reply_markup=keyboards.cancel_keyboard)
            await AdminCreateLot.create_lot_name.set()

        elif call.data.startswith('admin_delete_lot_'):
            lot_id = call.data.split('admin_delete_lot_')[1]

            db.delete_lot(lot_id)
            await call.message.delete()

        elif call.data.startswith('admin_mail_lot_'):
            await call.message.edit_reply_markup(reply_markup=None)

            lot_id = call.data.split('admin_mail_lot_')[1]
            lot_data = db.get_lot_data(lot_id)

            name = lot_data[1]
            description = lot_data[2]
            image = lot_data[6]

            mail_caption = f'''
{name}

{description}

Успей принять участие 🤩✨
                    '''

            keyboard = keyboards.lot_keyboard(lot_id, is_admin=False)

            await call.message.answer(f'Рассылка лота №{lot_id} началась')

            all_users_ids = db.get_all_users_ids()
            for user_id in all_users_ids:
                try:
                    await bot.send_photo(user_id, image, mail_caption, reply_markup=keyboard)
                except:
                    pass
            await call.message.answer(f'Рассылка лота №{lot_id} закончилась')

        elif call.data.startswith('admin_payment'):
            if call.data.startswith('admin_payment_confirm_'):
                payment_id = call.data.split('admin_payment_confirm_')[1]
                payment_data = db.get_payment_data(payment_id)

                user_id = payment_data[1]
                yc_amount = payment_data[2]

                promo_bonus = False

                promo_percent = db.get_user_active_promo_code(user_id)
                if promo_percent:
                    bonus = round(yc_amount / 100 * promo_percent)
                    if bonus >= 1:
                        promo_bonus = bonus

                    db.update_user_active_promo_code(user_id, '')

                await successful_payment(payment_id, user_id, yc_amount, promo_bonus=promo_bonus)

                try:
                    await call.message.edit_reply_markup(reply_markup=keyboards.payment_confirmed)
                except:
                    pass

            elif call.data.startswith('admin_payment_reject_'):
                payment_id = call.data.split('admin_payment_reject_')[1]
                payment_data = db.get_payment_data(payment_id)

                user = payment_data[1]

                db.update_payment_status(payment_id, 'canceled')

                try:
                    await bot.send_message(user, f'''
    Платеж №{payment_id} отклонен
                                ''')
                except:
                    pass

                await call.message.edit_reply_markup(reply_markup=keyboards.payment_canceled)

        elif call.data.startswith('admin_withdrawal'):
            if call.data.startswith('admin_withdrawal_confirm_'):
                withdrawal_id = int(call.data.split('admin_withdrawal_confirm_')[1])
                withdrawal_data = db.get_withdrawal_data(withdrawal_id)

                user_id = withdrawal_data[1]

                db.update_withdrawal_status(withdrawal_id, 'confirmed')

                try:
                    await bot.send_message(user_id, f'Ваш вывод №{withdrawal_id} выполнено')
                except:
                    pass

                await call.message.edit_reply_markup(reply_markup=keyboards.withdrawal_confirmed)

            elif call.data.startswith('admin_withdrawal_reject_'):
                withdrawal_id = int(call.data.split('admin_withdrawal_reject_')[1])
                withdrawal_data = db.get_withdrawal_data(withdrawal_id)

                user_id = withdrawal_data[1]
                yc_amount = withdrawal_data[2]

                db.update_user_balance(user_id, yc_amount)
                db.update_withdrawal_status(withdrawal_id, 'canceled')

                try:
                    await bot.send_message(user_id, f'Вашему выводу №{withdrawal_id} было отказано. Предлагаем связаться с менеджером для выяснения причины',
                                           reply_markup=keyboards.help_contact)
                except:
                    pass

                await call.message.edit_reply_markup(reply_markup=keyboards.withdrawal_canceled)

        elif call.data == 'admin_user_profile':
            await call.message.answer(f'''
Введите id или юзернейм победителя
                                      ''', parse_mode='Markdown', reply_markup=keyboards.cancel_keyboard)
            await AdminEditUserData.get_user_id.set()

            await call.message.edit_reply_markup(reply_markup=None)

        elif call.data.startswith('admin_edit_user'):
            if call.data.startswith('admin_edit_user_ban_'):
                user_id = call.data.split('admin_edit_user_ban_')[1]

                new_status = db.ban_or_unban_user(user_id)

                if new_status:
                    await storage.set_state(user=user_id, chat=user_id, state='ban')
                    await call.answer('Пользователь забанен', show_alert=True)
                else:
                    await storage.set_state(user=user_id, chat=user_id, state='*')
                    await call.answer('Пользователь теперь без бана', show_alert=True)

            elif call.data.startswith('admin_edit_user_balance_'):
                user_id = call.data.split('admin_edit_user_balance_')[1]

                await state.update_data(user_id=user_id)

                await call.message.answer('Введите новый баланс для пользователя', reply_markup=keyboards.cancel_keyboard)
                await AdminEditUserData.balance.set()

            elif call.data.startswith('admin_edit_user_level_'):
                user_id = call.data.split('admin_edit_user_level_')[1]

                await state.update_data(user_id=user_id)

                await call.message.answer('Введите новый уровень для пользователя', reply_markup=keyboards.cancel_keyboard)
                await AdminEditUserData.level.set()

            elif call.data.startswith('admin_edit_user_w_limits_'):
                user_id = call.data.split('admin_edit_user_w_limits_')[1]

                db.add_non_limit_user(user_id)

                await call.answer('Пользователю сняты лимиты на вывод')

        elif call.data == 'admin_edit_bot_data':
            await call.message.edit_reply_markup(reply_markup=keyboards.admin_edit_bot_data)

        elif call.data.startswith('admin_edit_bot'):
            if call.data == 'admin_edit_bot_requisites':
                await call.message.answer('Выберите валюту', reply_markup=keyboards.all_currencies_keyboard)
                await AdminEditBotData.edit_requisites_type.set()

            elif call.data == 'admin_edit_bot_in_currency':
                await call.message.answer('Выберите валюту', reply_markup=keyboards.all_currencies_keyboard)
                await AdminEditBotData.edit_in_currency_type.set()

            elif call.data == 'admin_edit_bot_help_link':
                await call.message.answer('Отправьте ссылку или юзернейм', reply_markup=keyboards.cancel_keyboard)
                await AdminEditBotData.edit_help_link.set()

            elif call.data == 'admin_edit_bot_help_text':
                await call.message.answer('Отправьте текст правил', reply_markup=keyboards.cancel_keyboard)
                await AdminEditBotData.edit_help_text.set()

        elif call.data == 'admin_count_users':
            all_users_ids = db.get_all_users_ids()

            await call.message.answer(f'Всего в боте {len(all_users_ids)} пользователей')

        elif call.data == 'admin_mail':
            await AdminMail.get_data.set()
            await call.message.answer('Отправьте текст, фото или видео для рассылки', reply_markup=keyboards.cancel_keyboard)

        elif call.data == 'admin_promo_codes':
            await call.message.edit_text('Админ Панель\nПромокоды', reply_markup=keyboards.admin_promo_codes_keyboard)
        elif call.data == 'admin_add_promo_code':
            await AdminAddPromoCode.promo_type.set()
            await call.message.answer('Выберите тип промокода', reply_markup=keyboards.promo_code_types_keyboard)

        elif call.data == 'admin_promo_codes_list':
            active_promo_codes = db.get_active_promo_codes()
            await call.message.answer('Активные промо коды',
                                      reply_markup=keyboards.generate_active_promo_codes_keyboard(active_promo_codes))

        elif call.data.startswith('admin_edit_promo_'):
            promo_id = int(call.data.split('admin_edit_promo_', maxsplit=1)[1])
            promo_data = db.get_promo_code_data_by_id(promo_id)
            promo_id, name, promo_type, amount, activations, members = promo_data

            if promo_type == 'bonus':
                promo_type_text = 'Начисление'
            elif promo_type == 'percent':
                promo_type_text = 'Процент к пополнению'
            else:
                promo_type_text = 'Не определено'

            members_list = members.split(',')

            await call.message.answer(f'''
Промокод: {name}
Тип: {promo_type_text}
Число монет/%к поплнению: {amount}
Количество активаций: {len(members_list)}/{activations}
            ''', reply_markup=keyboards.edit_promo_code(promo_id))

        elif call.data == 'admin_back':
            await call.message.edit_text('Админ Панель', reply_markup=keyboards.admin_keyboard)

        elif call.data == 'admin_duel':
            await call.message.answer('Введите номер дуэли', reply_markup=keyboards.cancel_keyboard)
            await AdminDuelInfo.duel_id.set()

        elif call.data.startswith('admin_duel_result_'):
            call_data = call.data.split('admin_duel_result_')[1]
            result, duel_id = call_data.split('_')

            status = db.get_duel_status(duel_id)
            if status != 'progress':
                return await call.answer('Дуэль уже закончена', show_alert=True)

            user_first = db.get_duel_creator_id(duel_id)
            user_second = db.duel_opponent_id(duel_id, user_first)

            if result in ['win1', 'win2']:
                if result == 'win1':
                    winner = user_first
                elif result == 'win2':
                    winner = user_second

                bet = db.get_duel_bet(duel_id)
                win_amount = 2 * bet * 0.9

                db.duel_update_to_end(duel_id, winner)
                db.update_user_balance(winner, win_amount)

                try:
                    await bot.send_message(winner, f'Вы победили в дуэли #{duel_id}. Ваш выигрыш {win_amount} YC')
                except:
                    pass

            elif result == 'draw':
                bet = db.get_duel_bet(duel_id)

                db.update_user_balance(user_first, bet)
                db.update_user_balance(user_second, bet)
                db.duel_update_to_end(duel_id, 'Возврат ставок')

                try:
                    await bot.send_message(user_first, f'Дуэль #{duel_id}. Возврат ставок')
                except:
                    pass
                try:
                    await bot.send_message(user_second, f'Дуэль #{duel_id}. Возврат ставок')
                except:
                    pass

            try:
                await call.message.edit_reply_markup(reply_markup=None)
            except:
                pass

            await call.answer('Результат установлен', show_alert=True)


    elif call.data.startswith('promo_edit_'):
        if call.data.startswith('promo_edit_activations_'):
            promo_id = int(call.data.split('promo_edit_activations_', maxsplit=1)[1])
            await call.message.answer('Введите новое кол-во использований', reply_markup=keyboards.cancel_keyboard)
            await AdminEditPromo.activations.set()
            await state.update_data(promo_id=promo_id)

        elif call.data.startswith('promo_edit_amount_'):
            promo_id = int(call.data.split('promo_edit_amount_', maxsplit=1)[1])
            await call.message.answer('Введите новый процент/кол-во монет', reply_markup=keyboards.cancel_keyboard)
            await AdminEditPromo.amount.set()
            await state.update_data(promo_id=promo_id)

        elif call.data.startswith('promo_edit_delete_'):
            promo_id = int(call.data.split('promo_edit_delete_', maxsplit=1)[1])
            db.delete_promo_code(promo_id)

            await call.message.answer('Промокод удален')
            await call.message.delete()

    elif call.data.startswith('lot'):
        if call.data.startswith('lot_data_'):
            await call.message.delete()

            lot_id = call.data.split('lot_data_', maxsplit=1)[1]
            lot_data = db.get_lot_data(lot_id)

            name = lot_data[1]
            description = lot_data[2]
            one_bid_price = lot_data[3]
            total_bids = lot_data[4]
            need_level = lot_data[5]
            members = lot_data[7]
            image = lot_data[6]
            now_bids = lot_data[9]

            user_bids_count = members.split(',').count(f'{call.message.chat.id}')

            caption = lot_text(name, description, one_bid_price, now_bids, total_bids, need_level, user_bids_count)

            if call.message.chat.id in ADMIN_IDS:
                is_admin=True
            else:
                is_admin=False

            await call.message.answer_photo(image, caption, reply_markup=keyboards.lot_keyboard(lot_id, is_admin=is_admin))

        elif call.data.startswith('lots_my_page_'):
            page = int(call.data.split('lots_my_page_')[1])
            await send_active_lots(call.message, page, user_lots=call.message.chat.id)

        elif call.data.startswith('lots_page_'):
            page = int(call.data.split('lots_page_')[1])
            await send_active_lots(call.message, page)

        elif call.data.startswith('lot_choose_winner_'):
            if call.data.startswith('lot_choose_winner_random_'):
                lot_id = call.data.split('lot_choose_winner_random_')[1]

                members = db.get_lot_members(lot_id).split(',')[:-1]
                winners_amount = db.get_winners_amount(lot_id)

                if winners_amount == 1:
                    winner_id = random.choice(members)

                    await set_winner(lot_id, winner_id)

                    await call.message.edit_caption(caption=f'Победитель выбран, им стал -- {db.get_user_full_name(winner_id)}',
                                                    reply_markup=None, parse_mode='Markdown')

                else:
                    winners_ids = []

                    for i in range(1, winners_amount+1):
                        winner_id = random.choice(members)
                        winners_ids.append(winner_id)

                        while winner_id in members:
                            members.remove(winner_id)

                    await set_winners(lot_id, winners_ids)

                    winners_text = ','.join(list(map(db.get_user_full_name, winners_ids)))

                    await call.message.edit_caption(caption=f'Победители выбраны, ими стали -- {winners_text}',
                                                    reply_markup=None, parse_mode='Markdown')

            # elif call.data.startswith('lot_choose_winner_manually_'):
            #     lot_id = call.data.split('lot_choose_winner_manually_')[1]

    elif call.data == 'my_lots':
        await call.message.delete()
        await send_active_lots(call.message, 0, user_lots=call.message.chat.id)

    elif call.data == 'change_yc_to_g':
        await call.message.answer(f'''
1 YC = {price_in_currency["G"]} G
        
Введите количество YC которые хотите обменять на G
        ''', reply_markup=keyboards.cancel_keyboard)
        await UserChangeYcToG.amount.set()

    elif call.data.startswith('take_part_in_'):
        lot_id = call.data.split('take_part_in_', maxsplit=1)[1]

        user_balance = db.get_user_balance(call.message.chat.id)
        user_level = db.get_user_level(call.message.chat.id)

        lot_data = db.get_lot_data(lot_id)

        name = lot_data[1]
        description = lot_data[2]
        one_bid_price = lot_data[3]
        total_bids = lot_data[4]
        need_level = lot_data[5]
        image = lot_data[6]
        members = lot_data[7]
        now_bids = lot_data[9]
        max_user_bets = lot_data[11]

        user_bids_count = members.split(',').count(f'{call.message.chat.id}')

        if now_bids >= total_bids:
            return await call.answer('Уже заняты все места', show_alert=True)

        if user_bids_count >= max_user_bets:
            return await call.answer('Вы уже приняли участие максимальное количество раз', show_alert=True)

        if one_bid_price > user_balance:
            return await call.message.answer('Недостаточно средств для участия в данном Розыгрыше , пожалуйста пополните баланс',
                                             reply_markup=keyboards.top_up)

        if user_level < need_level:
            return await call.answer(f'Для участия нужен уровень {need_level}.', show_alert=True)

        # add_user_lot(lot_id, call.message.chat.id)
        db.successful_bid(call.message.chat.id, lot_id, one_bid_price)
        db.add_spent_balance(call.message.chat.id, one_bid_price)

        if user_bids_count == 0:
            db.user_add_participation(call.message.chat.id)

        await call.answer('Вы приняли участвие')

        if call.message.chat.id in ADMIN_IDS:
            is_admin = True
        else:
            is_admin = False

        try:
            await call.message.edit_caption(caption=lot_text(name, description, one_bid_price, now_bids+1, total_bids, need_level, user_bids_count),
                                            reply_markup=keyboards.lot_keyboard(lot_id, is_admin=is_admin))
        except Exception as ex:
            print(ex)

        if now_bids + 1 >= total_bids:
            m = await bot.send_photo(ADMIN_CHANNEL_ID, image, caption=f'''
В розыгрыше {name} все места выкуплены. Нужно выбрать победителя.
            ''', reply_markup=keyboards.lot_choose_winner_method(lot_id))
            db.update_winner_post_id(lot_id, m.message_id)

    elif call.data.startswith('channel_take_part_in_'):
        lot_id = call.data.split('channel_take_part_in_', maxsplit=1)[1]

        lot_data = db.get_lot_data(lot_id)

        name = lot_data[1]
        description = lot_data[2]
        one_bid_price = lot_data[3]
        total_bids = lot_data[4]
        need_level = lot_data[5]
        members = lot_data[7]
        image = lot_data[6]
        now_bids = lot_data[9]

        user_bids_count = members.split(',').count(f'{call.from_user.id}')

        caption = lot_text(name, description, one_bid_price, now_bids, total_bids, need_level, user_bids_count)

        if call.from_user.id in ADMIN_IDS:
            is_admin = True
        else:
            is_admin = False

        await call.answer('Бот @ylionbot отправил Вам лот. Перейдите в него и снова нажмите на кнопку «Принять Участие»', show_alert=True)
        try:
            await bot.send_photo(call.from_user.id, image, caption, reply_markup=keyboards.lot_keyboard(lot_id, is_admin=is_admin))
        except:
            pass

    elif call.data == 'top_up':
        await UserTopUp.get_amount.set()
        await call.message.answer('Введите количесво монет сколько хотите пополнить',
                                  reply_markup=keyboards.cancel_keyboard)

    elif call.data == 'withdrawal':
        is_non_limit = db.is_non_limit_user(call.message.chat.id)

        if not is_non_limit:
            last_withdrawal_date = db.get_last_withdrawal_date(call.message.chat.id)

            if last_withdrawal_date:
                last_withdrawal_date = datetime.strptime(last_withdrawal_date[-1][0], '%Y-%m-%d %H:%M:%S.%f')

                user_level = db.get_user_level(call.message.chat.id)

                if user_level <= 10:
                    period = 3
                elif user_level <= 25:
                    period = 2
                elif user_level <= 49:
                    period = 1
                elif user_level >= 50:
                    period = 0
                else:
                    period = 3

                if floor((datetime.now() - last_withdrawal_date).days) < period:
                    next_time_to_withdrawal = last_withdrawal_date + timedelta(days=period)

                    next_time_to_withdrawal_text = f'{next_time_to_withdrawal.day} {statistic_months[next_time_to_withdrawal.month]} {next_time_to_withdrawal.year} года {next_time_to_withdrawal.hour if next_time_to_withdrawal.hour >= 10 else f"0{next_time_to_withdrawal.hour}"}:{next_time_to_withdrawal.minute if next_time_to_withdrawal.minute >= 10 else f"0{next_time_to_withdrawal.minute}"} МСК'

                    return await call.message.answer(f'Следующий вывод будет доступен {next_time_to_withdrawal_text}')

        await UserWithdrawal.get_bank_name.set()
        await call.message.answer('Введите название Вашего банка',
                                  reply_markup=keyboards.cancel_keyboard)

    elif call.data == 'withdrawal_G':
        await UserWithdrawalG.get_amount.set()
        await call.message.answer('Введите количество G которое хотите вывести',
                                  reply_markup=keyboards.cancel_keyboard)

    elif call.data == 'back_to_list':
        await call.message.delete()
        await send_active_lots(call.message, 0)

    elif call.data == 'write_review':
        await call.message.answer('Напишите отзыв о нашем Боте', reply_markup=keyboards.cancel_keyboard)
        await UserWriteReview.get_text.set()

    elif call.data.startswith('duels'):
        if call.data == 'duels_registration':
            active_duels = db.get_active_users_duels(call.message.chat.id)

            if len(active_duels) >= 3:
                return await call.message.answer('Одновременно нельзя создать больше трех активных дуэлей')

            try:
                await call.message.edit_reply_markup(reply_markup=None)
            except:
                pass

            await call.message.answer('Напишите свой ID в Standoff2', reply_markup=keyboards.cancel_keyboard)
            await UserDuelsRegistration.st_id.set()

        elif call.data == 'duels_list_select':
            await call.message.edit_reply_markup(reply_markup=keyboards.duels_bet_type)

        elif call.data == 'duels_list_free':
            await send_duels_list(call.message, 0, free=True)
        elif call.data == 'duels_list_paid':
            await send_duels_list(call.message, 0, free=False)

        elif call.data == 'duels_my':
            user_duels = db.get_user_duels(call.message.chat.id)

            if len(user_duels) == 0:
                return await call.answer('У вас еще нет дуэлей')

            await call.message.answer('Ваши дуэли', reply_markup=keyboards.my_list_duels_keyboard(user_duels))

        elif call.data == 'duels_info':
            await call.message.answer('''
Здравствуйте , Друзья. 
Здесь Инструкция, как играть в Дуэли ⚔️

Так, начнем . 
Для начала Вам нужно нажать на кнопку «ДЭУЛЬ», после чего пройти регистрацию, введя данные , которые Вас просит Бот, после чего  заявка появляется в списке Дэулей, где любой желающий , которого устроит сумма ставки и режим игры, сможет отправить Вам заявку на игру. 

Дальше вы списываетесь и идете играть !

Во время игры <b>НАСТОЯТЕЛЬНО РЕКОМЕНДУЕТСЯ делать скрины и запись экрана,</b> чтобы в случае апелляции вы смогли доказать свою правоту в случае спорной ситуации.
После того , как Вы сыграли, возвращаетесь к боту , и видите 3 кнопки:

-Я выиграл 
- Я проиграл 
- Апелляция 

Рекомендуем отвечать честно , ведь по итогу администрация выяснит правду, а за обман Вас забанят навсегда . Апелляция- это кнопка означающая , что если вдруг Вы не согласны с результатами, и имеете подозрения ,что против вас играли с Читами, или же игрок нарушил правила , будет разбирательство со стороны Администрации.

Комиссия бота 10% за каждую дуэль 

Надеемся , что Вам понравится , желаем удачных игр ❤️

Ваш GM YLION ✅
            ''', parse_mode='HTML')


    elif call.data.startswith('duel_list_free_page_'):
        page = int(call.data.split('duel_list_free_page_')[1])
        await send_duels_list(call.message, page, free=True)

    elif call.data.startswith('duel_list_paid_page_'):
        page = int(call.data.split('duel_list_paid_page_')[1])
        await send_duels_list(call.message, page, free=False)

    elif call.data.startswith('duel_info_'):
        duel_id = call.data.split('duel_info_', maxsplit=1)[1]
        duel_info = db.get_duel_info(duel_id)

        if not duel_info:
            return await call.answer('Дуэль была удалена', show_alert=True)

        duel_id, user_first, user_second, bet, st_id, game_mode, st_rank, st_name, status, winnner = duel_info

        duel_text = f'''
Предпочитаемый режим игры: {game_mode}
Ранг: {st_rank}
Сумма ставки YC: {bet}
        '''

        await call.message.answer(duel_text, reply_markup=keyboards.duel_take_part_keyboard(duel_id))

    elif call.data.startswith('duel_take_part_'):
        duel_id = call.data.split('duel_take_part_', maxsplit=1)[1]
        status = db.get_duel_status(duel_id)
        duel_creator_id = db.get_duel_creator_id(duel_id)

        if duel_creator_id == call.message.chat.id:
            return await call.answer('Вы не можете участвовать в своем дуэле')

        if status == 'wait':
            if db.get_duel_bet(duel_id) > db.get_user_balance(call.message.chat.id):
                return await call.answer('Недостаточно средств для участия', show_alert=True)

            if db.has_duel_request(duel_id, call.message.chat.id):
                return await call.answer('Вы уже отправляли заявку на эту дуэль', show_alert=True)

            await call.message.answer('Напишите свой ID в Standoff2', reply_markup=keyboards.cancel_keyboard)
            await state.update_data(duel_id=duel_id)
            await UserDuelTakePart.st_id.set()
        else:
            await call.answer('Эта дуэль уже не активна', show_alert=True)

    elif call.data.startswith('duel_my_info_'):
        duel_id = call.data.split('duel_my_info_', maxsplit=1)[1]
        duel_info = db.get_duel_info(duel_id)

        if not duel_info:
            return await call.answer('Дуэль была удалена', show_alert=True)

        duel_id, user_first, user_second, bet, st_id, game_mode, st_rank, st_name, status, winnner = duel_info

        duel_text = f'''
Дуэль #{duel_id}
ID в Standoff2: {st_id}
Предпочитаемый режим игры: {game_mode}
Ваш Ранг: {st_rank}
Сумма ставки YC: {bet}
Ник в Standoff2: {st_name}

'''

        if status == 'wait':
            duel_text += '🕙 Статус дуэли: в ожидании противника\n'
            keyboard = keyboards.duel_cancel_keyboard(duel_id)
        elif status == 'progress':
            duel_opponent_id = db.duel_opponent_id(duel_id, call.message.chat.id)
            opponent_info = db.duel_player_info(duel_id, duel_opponent_id)
            st_id, st_rank, st_name = opponent_info
            st_name = db.filter_text_markdown(st_name)
            duel_text += f'''
Противник:
{db.get_user_full_name(duel_opponent_id)}
ID в Standoff2: {st_id}
Ранг: {st_rank}
Ник в Standoff2: {st_name}

'''

            duel_text += '🕙 Статус дуэли: в прогресее\n'
            keyboard = keyboards.duel_result_keyboard(duel_id, db.get_duel_bet(duel_id))
        elif status == 'end':
            duel_opponent_id = db.duel_opponent_id(duel_id, call.message.chat.id)
            opponent_info = db.duel_player_info(duel_id, duel_opponent_id)
            st_id, st_rank, st_name = opponent_info
            st_name = db.filter_text_markdown(st_name)

            duel_text += f'''
Противник:
{db.get_user_full_name(duel_opponent_id)}
ID в Standoff2: {st_id}
Ранг: {st_rank}
Ник в Standoff2: {st_name}

'''

            duel_text += '🕙 Статус дуэли: закончена\n'
            if winnner == user_first:
                duel_text += 'Результат: выигрыш'
            elif winnner == user_second:
                duel_text += 'Результат: проигрыш'
            else:
                duel_text += 'Результат: возврат ставок'
            keyboard = None
        else:
            keyboard = None

        await call.message.answer(duel_text, parse_mode='Markdown', reply_markup=keyboard)

    elif call.data.startswith('duel_cancel_'):
        duel_id = call.data.split('duel_cancel_', maxsplit=1)[1]
        status = db.get_duel_status(duel_id)

        if status == 'wait':
            bet = db.get_duel_bet(duel_id)
            db.duel_cancel(duel_id)

            if bet:
                db.update_user_balance(call.message.chat.id, bet)

            try:
                await call.message.delete()
            except:
                pass

            await call.message.answer('Дуэль отменена')

        else:
            await call.answer('Дуэль уже была начата.')

    elif call.data.startswith('duel_req_con_'):
        call_data = call.data.split('duel_req_con_', maxsplit=1)[1]
        duel_id, from_user_id = call_data.split('_', maxsplit=1)

        status = db.get_duel_status(duel_id)

        if status != 'wait':
            return await call.answer('Дуэль уже была начата', show_alert=True)

        if db.get_duel_bet(duel_id) > db.get_user_balance(call.message.chat.id):
            return await call.answer('У оппонента недостаточно средств для участия', show_alert=True)

        db.duel_update_to_progress(duel_id, from_user_id)
        db.update_user_balance(from_user_id, -1*db.get_duel_bet(duel_id))

        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except:
            pass

        await call.answer('Заявка принята')

        opponent_info = db.duel_player_info(duel_id, from_user_id)
        st_id, st_rank, st_name = opponent_info
        st_name = db.filter_text_markdown(st_name)

        duel_text = f'''
Противник:
{db.get_user_full_name(from_user_id)}
ID в Standoff2: {st_id}
Ранг: {st_rank}
Ник в Standoff2: {st_name}
        '''

        await call.message.answer(duel_text, parse_mode='Markdown', reply_markup=keyboards.duel_result_keyboard(duel_id, db.get_duel_bet(duel_id)))

        opponent_info = db.duel_player_info(duel_id, call.message.chat.id)
        st_id, st_rank, st_name = opponent_info
        st_name = db.filter_text_markdown(st_name)

        duel_text = f'''
Противник:
{db.get_user_full_name(call.message.chat.id)}
ID в Standoff2: {st_id}
Ранг: {st_rank}
Ник в Standoff2: {st_name}
                '''
        try:
            await bot.send_message(from_user_id, f'''
Ваша заявка на участие в дуэли {db.get_duel_bet(duel_id)} YC | {db.get_duel_game_mode(duel_id)} принята
{duel_text}
                ''', parse_mode='Markdown', reply_markup=keyboards.duel_result_keyboard(duel_id, db.get_duel_bet(duel_id)))
        except:
            pass

    elif call.data.startswith('duel_req_rej_'):
        call_data = call.data.split('duel_req_rej_', maxsplit=1)[1]
        duel_id, from_user_id = call_data.split('_', maxsplit=1)

        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except:
            pass

        await call.answer('Заявка отклонена')

        try:
            await bot.send_message(from_user_id, f'''
Ваша заявка на участие в дуэли {db.get_duel_bet(duel_id)} YC | {db.get_duel_game_mode(duel_id)} отклонена
            ''')
        except:
            pass


    elif call.data.startswith('duel_res_win_') or call.data.startswith('duel_res_lose_'):

        call_data = call.data.split('duel_res_')[1]
        result, duel_id = call_data.split('_')

        status = db.get_duel_status(duel_id)
        if status != 'progress':
            return await call.answer('Дуэль уже закончена')

        if result == 'win':
            result_text = 'Выигрыш'
        elif result == 'lose':
            result_text = 'Проигрыш'

        await call.answer(f'Результат {result_text} установлен')

        duel_opponent_id = db.duel_opponent_id(duel_id, call.message.chat.id)
        try:
            await bot.send_message(duel_opponent_id, f'Дуэль #{duel_id}. Противник установил результат: {result_text}')
        except:
            pass

        db.duel_set_result(duel_id, call.message.chat.id, result)
        duel_result = db.duel_check_result(duel_id)

        if duel_result:
            winner = duel_result

            bet = db.get_duel_bet(duel_id)
            win_amount = 2*bet * 0.9

            db.duel_update_to_end(duel_id, winner)
            db.update_user_balance(winner, win_amount)

            try:
                await bot.send_message(winner, f'Вы победили в дуэли #{duel_id}. Ваш выигрыш {win_amount} YC')
            except:
                pass


async def on_startup(_):
    baned_users_list = db.get_baned_users()

    for user_id in baned_users_list:
        await storage.set_state(user=user_id, chat=user_id, state='ban')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
