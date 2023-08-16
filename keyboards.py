from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import PAGINATION_ACTIVE_LOTS, ORDERS_CHAT_LINK, bot_username
from math import ceil

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='РОЗЫГРЫШИ'),
    KeyboardButton(text='ДУЭЛЬ'),
    KeyboardButton(text='ПРОФИЛЬ'),
).add(
    KeyboardButton(text='ТОП 10'),
    KeyboardButton(text='ПРОМОКОД'),
    KeyboardButton(text='РЕФЕРАЛЬНАЯ СИСТЕМА'),
).add(
    KeyboardButton(text='ПРАВИЛА'),
    KeyboardButton(text='ПОДДЕРЖКА'),
    KeyboardButton(text='ОТЗЫВЫ'),
).add(
    KeyboardButton(text='КАК ПОЛЬЗОВАТЬСЯ БОТОМ'),
)


def active_lots_keyboard(lots: list, page, user_lots=False):
    keyboard = InlineKeyboardMarkup()
    buttons = []
    for lot_id, name in lots[page * PAGINATION_ACTIVE_LOTS: page * PAGINATION_ACTIVE_LOTS + PAGINATION_ACTIVE_LOTS]:
        buttons.append(InlineKeyboardButton(text=name, callback_data=f'lot_data_{lot_id}'))

    keyboard.row_width = 1
    keyboard.add(*buttons)

    keyboard.row_width = 3

    if user_lots:
        callback_page_start = 'lots_my_page'
    else:
        callback_page_start = 'lots_page'

    keyboard.add(
        InlineKeyboardButton(text='<<<', callback_data=f'{callback_page_start}_{page-1}'),
        InlineKeyboardButton(text=f'{page+1}/{ceil(len(lots)/PAGINATION_ACTIVE_LOTS)}', callback_data='main_menu'),
        InlineKeyboardButton(text='>>>', callback_data=f'{callback_page_start}_{page+1}'),
    )

    return keyboard


def lot_keyboard(lot_id, is_admin=False):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='🟢 Принять участие 🟢', callback_data=f'take_part_in_{lot_id}'),
        InlineKeyboardButton(text='Вернуться к списку розыгрышей', callback_data='back_to_list'),
    )

    if is_admin:
        keyboard.add(
            InlineKeyboardButton(text='Удалить лот', callback_data=f'admin_delete_lot_{lot_id}'),
            InlineKeyboardButton(text='Рассылка', callback_data=f'admin_mail_lot_{lot_id}')
        )

    return keyboard


def lot_channel_keyboard(lot_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='Принять участие', callback_data=f'channel_take_part_in_{lot_id}'),
    )

    return keyboard


def lot_choose_winner_method(lot_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Выбрать автоматически', callback_data=f'lot_choose_winner_random_{lot_id}'),
        InlineKeyboardButton(text='Выбрать в ручную', url=f'https://t.me/{bot_username}?start=set_winner_lot_id={lot_id}'),
    )

    return keyboard


def help_contact(help_link):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Связаться с тех. поддержкой', url=help_link)
    )

    return keyboard


def orders_chat_keyboard(review):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Перейти в чат', url=ORDERS_CHAT_LINK)
    )

    if review:
        keyboard.add(
            InlineKeyboardButton(text='Оставить Отзыв', callback_data='write_review')
        )

    return keyboard


top_up = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up')
)

cabinet_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up'),
    InlineKeyboardButton(text='Запросить вывод YC', callback_data='withdrawal'),
    InlineKeyboardButton(text='Запросить вывод G', callback_data='withdrawal_G'),
    InlineKeyboardButton(text='Обменять YC на G', callback_data='change_yc_to_g'),
    InlineKeyboardButton(text='Мои участия', callback_data='my_lots')
)

duels_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Регистрация', callback_data='duels_registration'),
    InlineKeyboardButton(text='Список участников', callback_data='duels_list_select'),
    InlineKeyboardButton(text='Мои дуэли', callback_data='duels_my'),
    InlineKeyboardButton(text='Инструкция', callback_data='duels_info'),
)

duels_bet_type = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Бесплатные', callback_data='duels_list_free'),
    InlineKeyboardButton(text='Платные', callback_data='duels_list_paid'),
)

duels_confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Опубликовать'),
    KeyboardButton(text='Отменить'),
)


def list_duels_keyboard(duels: list, page=0, free=False):
    keyboard = InlineKeyboardMarkup()

    for duel_id, status, bet, game_mode in duels[page*10:page*10+10]:
        keyboard.add(
            InlineKeyboardButton(text=f'{bet} YC | {game_mode}', callback_data=f'duel_info_{duel_id}')
        )

    if free:
        keyboard.add(
            InlineKeyboardButton(text='<<<', callback_data=f'duel_list_free_page_{page-1}'),
            InlineKeyboardButton(text=f'{page+1}/{ceil(len(duels)/10)}', callback_data='main_menu'),
            InlineKeyboardButton(text='>>>', callback_data=f'duel_list_free_page_{page+1}'),
        )
    else:
        keyboard.add(
            InlineKeyboardButton(text='<<<', callback_data=f'duel_list_paid_page_{page-1}'),
            InlineKeyboardButton(text=f'{page+1}/{ceil(len(duels)/10)}', callback_data='main_menu'),
            InlineKeyboardButton(text='>>>', callback_data=f'duel_list_paid_page_{page+1}'),
        )

    return keyboard


def duel_take_part_keyboard(duel_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='Участвовать', callback_data=f'duel_take_part_{duel_id}')
    )

    return keyboard


def duel_request_keyboard(duel_id, from_user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='Принять противника', callback_data=f'duel_req_con_{duel_id}_{from_user_id}'),
        InlineKeyboardButton(text='Отклонить', callback_data=f'duel_req_rej_{duel_id}_{from_user_id}')
    )

    return keyboard


def my_list_duels_keyboard(duels: list):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for duel_id, status, bet, game_mode in duels:
        if status == 'wait':
            label = '🕙'
        elif status == 'progress':
            label = '▶️'
        elif status == 'end':
            label = '🔚'
        else:
            label = ''

        keyboard.add(
            InlineKeyboardButton(text=f'{label} {bet} YC | {game_mode}', callback_data=f'duel_my_info_{duel_id}')
        )

    return keyboard


def duel_cancel_keyboard(duel_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='Отменить', callback_data=f'duel_cancel_{duel_id}')
    )

    return keyboard


def duel_result_keyboard(duel_id, free=False):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(text='Я проиграл', callback_data=f'duel_res_lose_{duel_id}'),
        InlineKeyboardButton(text='Я выиграл', callback_data=f'duel_res_win_{duel_id}')
    )

    if free:
        keyboard.add(InlineKeyboardButton(text='Апелляция', url=f'https://t.me/ylionadmin'))

    return keyboard


game_modes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    KeyboardButton(text='Командный Бой'),
    KeyboardButton(text='Союзники'),
    KeyboardButton(text='Соревновательный'),
    KeyboardButton(text='Эскалация'),
    KeyboardButton(text='Гонка вооружений'),
    KeyboardButton(text='Аркада'),
)


st_ranks_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4).add(
    KeyboardButton('BRONZE I'),
    KeyboardButton('BRONZE II'),
    KeyboardButton('BRONZE III'),
    KeyboardButton('BRONZE IV'),
).add(
    KeyboardButton('SILVER I'),
    KeyboardButton('SILVER II'),
    KeyboardButton('SILVER III'),
    KeyboardButton('SILVER IV'),
).add(
    KeyboardButton('GOLD I'),
    KeyboardButton('GOLD II'),
    KeyboardButton('GOLD III'),
    KeyboardButton('GOLD IV'),
).add(
    KeyboardButton('PHOENIX'),
    KeyboardButton('RANGER'),
    KeyboardButton('CHAMPION'),
).add(
    KeyboardButton('MASTER'),
    KeyboardButton('ELITE'),
    KeyboardButton('THE LEGEND'),
)

top_up_methods_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='УКР 🇺🇦 Карты:'),
    KeyboardButton(text='RU 🇷🇺 Карты:'),
    KeyboardButton(text='TETHER $ “USDT”'),
).add(
    KeyboardButton(text='Отменить')
)

currencies_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='UAH'),
    KeyboardButton(text='RUB'),
).add(
    KeyboardButton(text='Отменить')
)

all_currencies_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='UAH'),
    KeyboardButton(text='RUB'),
    KeyboardButton(text='USD'),
).add(
    KeyboardButton(text='G'),
).add(
    KeyboardButton(text='Отменить')
)


confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Верно'),
    KeyboardButton(text='Отменить')
)

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Отменить')
)

yes_or_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Да'),
    KeyboardButton(text='Нет'),
).add(
    KeyboardButton(text='Отменить')

)

payment_confirmed = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Платеж подтвержден', callback_data='1')
)

payment_confirmed_by_hands = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Платеж начислен админом', callback_data='1')
)

payment_canceled = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Платеж отклонен', callback_data='1')
)

withdrawal_confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton(text='Подтвердить вывод'),
    KeyboardButton(text='Отменить'),
)


def withdrawal_admin_keyboard(withdrawal_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Отправлено', callback_data=f'admin_withdrawal_confirm_{withdrawal_id}'),
        InlineKeyboardButton(text='Отказ', callback_data=f'admin_withdrawal_reject_{withdrawal_id}')
    )


withdrawal_confirmed = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Вывод оплачен', callback_data='1')
)


withdrawal_canceled = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Вывод отказан', callback_data='1')
)

promo_code_types_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Начисление'),
    KeyboardButton(text='Процент к пополнению')
).add(
    KeyboardButton(text='Отменить'),
)

admin_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Добавить розыгрыш', callback_data='admin_create_lot'),
    InlineKeyboardButton(text='Просмотр профиля', callback_data='admin_user_profile'),
    InlineKeyboardButton(text='Редактировать данные', callback_data='admin_edit_bot_data'),
    InlineKeyboardButton(text='Количество пользователей', callback_data='admin_count_users'),
    InlineKeyboardButton(text='Рассылка', callback_data='admin_mail'),
    InlineKeyboardButton(text='Промокоды', callback_data='admin_promo_codes'),
    InlineKeyboardButton(text='Информация о дуэли', callback_data='admin_duel')
)

manager_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Информация о дуэли', callback_data='admin_duel')
)

admin_promo_codes_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Добавить промокод', callback_data='admin_add_promo_code'),
    InlineKeyboardButton(text='Список активных промокодов', callback_data='admin_promo_codes_list'),
    InlineKeyboardButton(text='Назад', callback_data='admin_back'),
)


def generate_active_promo_codes_keyboard(active_promo_codes: list):
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = []

    for promo_id, name in active_promo_codes:
        buttons.append(
            InlineKeyboardButton(text=name, callback_data=f'admin_edit_promo_{promo_id}')
        )

    keyboard.add(*buttons)

    return keyboard


def edit_promo_code(promo_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='Ред. кол. использований', callback_data=f'promo_edit_activations_{promo_id}'),
        InlineKeyboardButton(text='Ред. процент/кол-во монет', callback_data=f'promo_edit_amount_{promo_id}'),
        InlineKeyboardButton(text='Удалить', callback_data=f'promo_edit_delete_{promo_id}'),
    )

    return keyboard


def admin_edit_user_data(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Забанить/Разбанить', callback_data=f'admin_edit_user_ban_{user_id}'),
        InlineKeyboardButton(text='Редактировать Баланс', callback_data=f'admin_edit_user_balance_{user_id}'),
        InlineKeyboardButton(text='Редактировать Уровень', callback_data=f'admin_edit_user_level_{user_id}'),
        InlineKeyboardButton(text='Убрать временные лимиты на вывод', callback_data=f'admin_edit_user_w_limits_{user_id}'),
    )

    return keyboard


admin_edit_bot_data = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Реквизиты', callback_data='admin_edit_bot_requisites'),
    InlineKeyboardButton(text='КУРС', callback_data='admin_edit_bot_in_currency'),
    InlineKeyboardButton(text='Ссылка на Поддержку', callback_data='admin_edit_bot_help_link'),
    InlineKeyboardButton(text='Текст Правил', callback_data='admin_edit_bot_help_text'),
)


def admin_payment_keyboard(payment_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text='Подтвердить платеж', callback_data=f'admin_payment_confirm_{payment_id}'),
        InlineKeyboardButton(text='Оплатить в ручную', url=f'https://t.me/{bot_username}?start=payment_id={payment_id}'),
        InlineKeyboardButton(text='Отклонить платеж', callback_data=f'admin_payment_reject_{payment_id}'),
    )

    return keyboard


def admin_duel_set_result(duel_id):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(text='Победил игрок 1', callback_data=f'admin_duel_result_win1_{duel_id}'),
        InlineKeyboardButton(text='Победил игрок 2', callback_data=f'admin_duel_result_win2_{duel_id}')
    )

    keyboard.add(
        InlineKeyboardButton(text='Вернуть ставки', callback_data=f'admin_duel_result_draw_{duel_id}')
    )

    return keyboard
