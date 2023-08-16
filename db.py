from config import db_path, REF_BONUS, ADMIN_IDS
import sqlite3


def add_new_user(user_id, first_name, last_name, username):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        if not cursor.execute('SELECT user_id FROM users WHERE user_id = (?)', (user_id,)).fetchone():
            cursor.execute('INSERT INTO users (user_id, first_name, last_name, username) VALUES ((?), (?), (?), (?))', (user_id, first_name, last_name, username))
        else:
            cursor.execute('UPDATE users SET first_name = (?), last_name = (?), username = (?) WHERE user_id = (?)', (first_name, last_name, username, user_id))


def add_lot(lot_id, name, desc, one_bid_price, total_bids, need_level, image, max_user_bets, prize_amount, winners_amount):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO lots (id, name, desc, one_bid_price, total_bids, need_level, image, status,'
                       'max_user_bets, prize_amount, winners_amount) '
                       'VALUES ((?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?))',
                       (lot_id, name, desc, one_bid_price, total_bids, need_level, image, 'active', max_user_bets,
                        prize_amount, winners_amount))


def delete_lot(lot_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE lots SET status = ? WHERE id = ?', ('delete', lot_id))


def get_active_lots(user_lots=False):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        if user_lots:
            active_lots = cursor.execute(f"SELECT id, name FROM lots WHERE members LIKE '%{user_lots},%' AND status = ?", ('active',)).fetchall()
        else:
            active_lots = cursor.execute('SELECT id, name FROM lots WHERE status = ?', ('active',)).fetchall()

    return active_lots


def get_lot_data(lot_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        lot_data = cursor.execute('SELECT * FROM lots WHERE id = ?', (lot_id,)).fetchone()

    return lot_data


def get_lot_members(lot_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        return cursor.execute('SELECT members FROM lots WHERE id = (?)', (lot_id,)).fetchone()[0]


def get_winners_amount(lot_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        return cursor.execute('SELECT winners_amount FROM lots WHERE id = (?)', (lot_id,)).fetchone()[0]


def successful_bid(user_id, lot_id, one_bid_price):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute('UPDATE users SET balance = balance - (?) WHERE user_id = (?)', (one_bid_price, user_id))
        cursor.execute('UPDATE lots SET now_bids = now_bids + 1 WHERE id = (?)', (lot_id,))
        cursor.execute('UPDATE lots SET members = (?) WHERE id = (?)',
                            (f'{cursor.execute("SELECT members FROM lots WHERE id = (?)", (lot_id,)).fetchone()[0]}{user_id},', lot_id))


def set_complete_lot(lot_id, winner_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute('UPDATE lots SET status = "complete", winner = (?) WHERE id = (?)', (winner_id, lot_id))


def update_winner_post_id(lot_id, message_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE lots SET mes_in_channel_id = ? WHERE id = ?', (message_id, lot_id))


def get_lot_mes_id_in_channel(lot_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        mes_id_in_channel = cursor.execute('SELECT mes_in_channel_id FROM lots WHERE id = ?', (lot_id,)).fetchone()

    if mes_id_in_channel:
        return mes_id_in_channel[0]
    return False


def search_user(data):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        search_user_id = cursor.execute('SELECT user_id FROM users WHERE user_id = ? OR username = ?', (data, data)).fetchone()

    if search_user_id:
        return search_user_id[0]

    return False



def get_user_level(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        level = cursor.execute('SELECT level FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

    return level


def get_user_balance(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()

    try:
        return balance[0]

    except:
        if not cursor.execute('SELECT user_id FROM users WHERE user_id = (?)', (user_id,)).fetchone():
            cursor.execute('INSERT INTO users (user_id, first_name, last_name, username) VALUES ((?), (?), (?), (?))', (user_id, 'Name', 'Surname', ''))

        return 0


def get_user_balance_G(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        balance_G = cursor.execute('SELECT balance_G FROM users WHERE user_id = ?', (user_id,)).fetchone()

    try:
        return balance_G[0]

    except:
        return 0


def update_user_balance(user_id, amount):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

        new_balance = round(balance + amount, 2)

        cursor.execute('UPDATE users SET balance = (?) WHERE user_id = (?)', (new_balance, user_id))


def update_user_balance(user_id, amount):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

        new_balance = round(balance + amount, 2)

        cursor.execute('UPDATE users SET balance = (?) WHERE user_id = (?)', (new_balance, user_id))


def update_user_balance_G(user_id, amount):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        balance = cursor.execute('SELECT balance_G FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

        new_balance = round(balance + amount, 2)

        cursor.execute('UPDATE users SET balance_G = (?) WHERE user_id = (?)', (new_balance, user_id))


def get_user_participation(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        participation = cursor.execute('SELECT participation FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

    return participation


def user_add_participation(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE users SET participation = participation + 1 WHERE user_id = ?', (user_id,))
        participation = cursor.execute('SELECT participation FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

        if participation % 5 == 0:
            cursor.execute('UPDATE users SET level = level + 1 WHERE user_id = ?', (user_id,))


def get_user_full_name(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        first_name, last_name, username = cursor.execute('SELECT first_name, last_name, username FROM users WHERE user_id = ?',
                                                         (user_id,)).fetchone()

    full_name = '[' + first_name + last_name + ']' + f'(tg://user?id={user_id})'

    if username:
        full_name += f' @{username}'

    full_name = full_name.replace('_', '\_')
    full_name = full_name.replace('*', '\*')
    full_name = full_name.replace('`', '\`')
    # full_name = full_name.replace('[', '\[')

    return full_name


def filter_text_markdown(text):
    text = text.replace('_', '\_')
    text = text.replace('*', '\*')
    text = text.replace('`', '\`')
    text = text.replace('[', '\[')
    return text


def set_user_balance(user_id, balance):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE users SET balance = (?) WHERE user_id = (?)', (balance, user_id))


def set_user_level(user_id, level):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE users SET level = (?) WHERE user_id = (?)', (level, user_id))


def get_all_users_ids():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        all_users_ids = [i[0] for i in cursor.execute('SELECT user_id FROM users').fetchall()]

    return all_users_ids


def add_spent_balance(user_id, amount):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        spent_balance = cursor.execute('SELECT amount FROM spent_balance WHERE user_id = (?)', (user_id,)).fetchone()

        if spent_balance:
            new_spent_balance = spent_balance[0] + amount
            cursor.execute('UPDATE spent_balance SET amount = (?) WHERE user_id = (?)', (new_spent_balance, user_id))
        else:
            cursor.execute('INSERT INTO spent_balance (user_id, amount) VALUES ((?),(?))', (user_id, amount))


def get_top_users_spent_balance():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        top_users = cursor.execute('SELECT user_id, amount FROM spent_balance ORDER BY amount DESC LIMIT 10').fetchall()

    return top_users


def get_top_users_donations():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        donate_users = set([i[0] for i in cursor.execute('SELECT user_id FROM payments WHERE status = (?)', ("confirmed",)).fetchall()])

    data = {}

    for user_id in donate_users:
        if user_id in ADMIN_IDS:
            continue

        user_donates = sum([i[0] for i in cursor.execute('SELECT yc_amount FROM payments WHERE status = (?) AND user_id = (?)',
                                                         ("confirmed", user_id)).fetchall()])
        data.update({user_id: user_donates})

    return list(reversed(sorted(data.items(), key=lambda item: item[1])))[:10]


def get_top_duel_winners():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        duel_winners = [i[0] for i in cursor.execute('SELECT winner FROM duels WHERE bet > 0').fetchall()]

    data = {}

    for user_id in duel_winners:
        # if user_id in ADMIN_IDS:
        #     continue
        if user_id == 'Возврат ставок':
            continue
        if user_id == '':
            continue

        if user_id in data.keys():
            data.update({user_id: data[user_id]+1})
        else:
            data.update({user_id: 1})

    return list(reversed(sorted(data.items(), key=lambda item: item[1])))[:10]


def get_review(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        review = cursor.execute('SELECT text FROM reviews WHERE user_id = (?)', (user_id,)).fetchone()
    if review:
        return False
    else:
        return True


def add_review(user_id, text):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO reviews (user_id, text) VALUES ((?),(?))', (user_id, text))


def add_referral(referral_id, referrer_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        if not cursor.execute('SELECT user_id FROM users WHERE user_id = (?)',
                              (referral_id,)).fetchone():
            cursor.execute('INSERT INTO ref (referral_id, referrer_id) VALUES ((?), (?))',
                           (referral_id, referrer_id))


def user_referral_info(user_id):
    with sqlite3.connect('data.db') as con:
        cursor = con.cursor()

        referrals_count = len(cursor.execute('SELECT referral_id FROM ref WHERE referrer_id = (?)',
                                             (user_id,)).fetchall())

        bonus = sum([i[0] for i in cursor.execute('SELECT bonus FROM ref WHERE  referrer_id = (?)', (user_id,)).fetchall()])

    return referrals_count, bonus


def check_referral(referral_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        if cursor.execute('SELECT referral_id FROM ref WHERE referral_id = (?)', (referral_id,)).fetchone():
            if cursor.execute('SELECT bonus FROM ref WHERE referral_id = (?)', (referral_id,)).fetchone()[0] == 0:
                referrer_id = cursor.execute('SELECT referrer_id FROM ref WHERE referral_id = (?)', (referral_id,)).fetchone()[0]

                bonus = REF_BONUS

                cursor.execute('UPDATE ref SET bonus = (?) WHERE referral_id = (?)', (bonus, referral_id,))
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = (?)', (bonus, referrer_id))

                return referrer_id
    return False




def add_payment(payment_id, user_id, yc_amount, in_currency, currency, file_id, file_type, mes_in_channel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO payments (payment_id, user_id, yc_amount, in_currency, currency, file_id, file_type, mes_in_channel_id) '
                       'VALUES ((?),(?),(?),(?),(?),(?),(?),(?))',
                       (payment_id, user_id, yc_amount, in_currency, currency, file_id, file_type, mes_in_channel_id))


def get_payment_data(payment_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        payment_data = cursor.execute('SELECT * FROM payments WHERE payment_id = ?', (payment_id,)).fetchone()

    return payment_data


def update_payment_status(payment_id, status):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE payments SET status = ? WHERE payment_id = ?', (status, payment_id))


def add_withdrawal(withdrawal_id, user_id, yc_amount, in_currency, currency, bank_name, name, card, date):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO withdrawals (withdrawal_id, user_id, yc_amount, in_currency, currency, bank_name, name, card, date) '
                       'VALUES ((?),(?),(?),(?),(?),(?),(?),(?),(?))',
                       (withdrawal_id, user_id, yc_amount, in_currency, currency, bank_name, name, card, date))


def get_withdrawal_data(withdrawal_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        withdrawal_data = cursor.execute('SELECT * FROM withdrawals WHERE withdrawal_id = ?', (withdrawal_id,)).fetchone()

    return withdrawal_data


def update_withdrawal_status(withdrawal_id, status):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE withdrawals SET status = ? WHERE withdrawal_id = ?', (status, withdrawal_id))


def get_last_withdrawal_date(user_id):
    with sqlite3.connect('data.db') as con:
        cursor = con.cursor()
        last_withdrawal_date = cursor.execute('SELECT date FROM withdrawals WHERE user_id = (?) AND status = (?) OR status = (?)',
                                              (user_id, 'confirmed', 'created')).fetchall()

    return last_withdrawal_date



def add_non_limit_user(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO withdrawals_non_limits_users (user_id) VALUES (?)', (user_id,))


def is_non_limit_user(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        is_non_limit = cursor.execute('SELECT user_id FROM withdrawals_non_limits_users WHERE user_id = (?)', (user_id,)).fetchone()

    return is_non_limit


def is_baned_user(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        is_baned = cursor.execute('SELECT user_id FROM baned_users WHERE user_id = (?)', (user_id,)).fetchone()

    if is_baned:
        return True

    return False


def ban_or_unban_user(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        is_baned = cursor.execute('SELECT user_id FROM baned_users WHERE user_id = (?)', (user_id,)).fetchone()

        if is_baned:
            cursor.execute('DELETE FROM baned_users WHERE user_id = (?)', (user_id,))
            return False
        else:
            cursor.execute('INSERT INTO baned_users (user_id) VALUES (?)', (user_id,))
            return True


def get_baned_users():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        baned_users_list = [i[0] for i in cursor.execute('SELECT user_id FROM baned_users').fetchall()]

    return baned_users_list


def get_promo_code_data(name):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        promo_data = cursor.execute('SELECT * FROM promo_codes WHERE name = (?)', (name,)).fetchone()

    return promo_data


def get_promo_code_data_by_id(promo_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        promo_data = cursor.execute('SELECT * FROM promo_codes WHERE id = (?)', (promo_id,)).fetchone()

    return promo_data


def get_active_promo_codes():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        promo_codes = cursor.execute('SELECT id, name, activations, members FROM promo_codes').fetchall()

    active_promo_codes = []

    for promo_id, name, activations, members in promo_codes:
        members_list = members.split(',')
        if len(members_list) - 1 < activations:
            active_promo_codes.append((promo_id, name))

    return active_promo_codes


def add_promo_activation(name, members):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE promo_codes SET members = (?) WHERE name = (?)',
                       (members, name))


def add_promo_code(promo_id, name, promo_type, amount, activations):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO promo_codes (id, name, type, amount, activations) VALUES ((?),(?),(?),(?),(?))',
                       (promo_id, name, promo_type, amount, activations))


def update_promo_code_activations(promo_id, activations):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE promo_codes SET activations = (?) WHERE id = (?)',
                       (activations, promo_id))


def update_promo_code_amount(promo_id, amount):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE promo_codes SET amount = (?) WHERE id = (?)',
                       (amount, promo_id))


def delete_promo_code(promo_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('DELETE FROM promo_codes WHERE id = (?)', (promo_id,))


def get_user_active_promo_code(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        active_promo_code = cursor.execute('SELECT active_promo_code FROM users WHERE user_id = (?)', (user_id,)).fetchone()

    if active_promo_code:
        percent = cursor.execute('SELECT amount FROM promo_codes WHERE name = (?)', (active_promo_code[0],)).fetchone()
        if percent:
            return percent[0]

    return False


def update_user_active_promo_code(user_id, promo_code):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE users SET active_promo_code = (?) WHERE user_id = (?)', (promo_code, user_id))



def add_duel(duel_id, user_first, bet, st_id, game_mode, st_rank, st_name, status):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO duels (id, user_first, bet, st_id, game_mode, st_rank, st_name, status) '
                       'VALUES ((?),(?),(?),(?),(?),(?),(?),(?))',
                       (duel_id, user_first, bet, st_id, game_mode, st_rank, st_name, status))


def add_duel_request(duel_id, user_id, st_id, st_rank, st_name):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO duel_request (duel_id, user_id, st_id, st_rank, st_name) '
                       'VALUES ((?),(?),(?),(?),(?))',
                       (duel_id, user_id, st_id, st_rank, st_name))


def duel_update_to_progress(duel_id, user_second):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE duels SET user_second = (?), status = (?) WHERE id = (?)',
                       (user_second, 'progress', duel_id))
        cursor.execute('INSERT INTO duels_results (duel_id, user_first, user_second) VALUES ((?),(?),(?))',
                       (duel_id, '', ''))


def duel_update_to_end(duel_id, winner):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('UPDATE duels SET winner = (?), status = (?) WHERE id = (?)',
                       (winner, 'end', duel_id))


def duel_update_to_end(duel_id, winner=None):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        if winner:
            cursor.execute('UPDATE duels SET winner = (?), status = (?) WHERE id = (?)',
                           (winner, 'end', duel_id))


def has_duel_request(duel_id, user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        has_duel = cursor.execute('SELECT duel_id FROM duel_request WHERE duel_id = (?) AND user_id = (?)',
                                  (duel_id, user_id)).fetchone()

    if has_duel:
        return True
    else:
        return False


def get_active_duels(free=False):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        if free:
            active_duels = cursor.execute('SELECT id, status, bet, game_mode FROM duels WHERE status = (?) AND bet = 0 ORDER BY id DESC',
                                          ('wait',)).fetchall()
        else:
            active_duels = cursor.execute('SELECT id, status, bet, game_mode FROM duels WHERE status = (?) AND bet != 0 ORDER BY id DESC',
                                          ('wait',)).fetchall()

    return active_duels


def get_active_users_duels(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        active_duels = cursor.execute('SELECT * FROM duels WHERE '
                                      '(user_first = (?) OR user_second = (?)) AND status = (?)',
                                      (user_id, user_id, 'wait')).fetchall()

    return active_duels


def get_user_duels(user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        user_duels = cursor.execute('SELECT id, status, bet, game_mode FROM duels WHERE user_first = (?) OR user_second = (?)',
                                      (user_id, user_id)).fetchall()

    return user_duels


def get_duel_info(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        duel_info = cursor.execute('SELECT * FROM duels WHERE id = (?)',
                                      (duel_id,)).fetchone()

    return duel_info


def get_duel_status(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        status = cursor.execute('SELECT status FROM duels WHERE id = (?)', (duel_id,)).fetchone()

    if status:
        return status[0]
    else:
        return False


def get_duel_bet(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        bet = cursor.execute('SELECT bet FROM duels WHERE id = (?)', (duel_id,)).fetchone()

    if bet:
        return bet[0]
    else:
        return False


def get_duel_game_mode(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        game_mode = cursor.execute('SELECT game_mode FROM duels WHERE id = (?)', (duel_id,)).fetchone()

    if game_mode:
        return game_mode[0]
    else:
        return False


def get_duel_creator_id(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        user_first = cursor.execute('SELECT user_first FROM duels WHERE id = (?)', (duel_id,)).fetchone()

    if user_first:
        return user_first[0]
    else:
        return False


def duel_cancel(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        cursor.execute('DELETE FROM duels WHERE id = (?)', (duel_id,))


def duel_player_info(duel_id, user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        user_first, user_second = cursor.execute('SELECT user_first, user_second FROM duels WHERE id = (?)', (duel_id,)).fetchone()

        user_id = int(user_id)
        if user_id == user_first:
            user_data = cursor.execute(
                'SELECT st_id, st_rank, st_name FROM duels WHERE id = (?)',
                (duel_id,)).fetchone()

            return user_data

        elif user_id == user_second:
            user_data = cursor.execute('SELECT st_id, st_rank, st_name FROM duel_request WHERE duel_id = (?) AND user_id = (?)',
                                           (duel_id, user_id)).fetchone()

            return user_data

    return False


def duel_opponent_id(duel_id, user_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        user_first, user_second = cursor.execute('SELECT user_first, user_second FROM duels WHERE id = (?)', (duel_id,)).fetchone()

        if user_id == user_first:
            return user_second

        elif user_id == user_second:
            return user_first

    return False


def duel_set_result(duel_id, from_user_id, result):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        user_first, user_second = cursor.execute('SELECT user_first, user_second FROM duels WHERE id = (?)',
                                                 (duel_id,)).fetchone()
        if from_user_id == user_first:
            cursor.execute('UPDATE duels_results SET user_first = (?) WHERE duel_id = (?)', (result, duel_id))
        elif from_user_id == user_second:
            cursor.execute('UPDATE duels_results SET user_second = (?) WHERE duel_id = (?)', (result, duel_id))


def duel_check_result(duel_id):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        user_first_result, user_second_result = cursor.execute('SELECT user_first, user_second FROM duels_results WHERE duel_id = (?)',
                                                               (duel_id,)).fetchone()

        if user_first_result and user_second_result:
            user_first, user_second = cursor.execute('SELECT user_first, user_second FROM duels WHERE id = (?)',
                                                     (duel_id,)).fetchone()

            if user_first_result == 'win' and user_second_result == 'lose':
                return user_first
            elif user_first_result == 'lose' and user_second_result == 'win':
                return user_second

        return False


def duel_get_user_result(duel_id, user_first=None, user_second=None):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()

        if user_first:
            user_result = cursor.execute('SELECT user_first FROM duels_results WHERE duel_id = (?)',
                                          (duel_id,)).fetchone()
        elif user_second:
            user_result = cursor.execute('SELECT user_second FROM duels_results WHERE duel_id = (?)',
                                          (duel_id,)).fetchone()
        if user_result:
            return user_result[0]

        return False