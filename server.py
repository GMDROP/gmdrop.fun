from flask import Flask, request, g
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
cors = CORS(app)

DATABASE = 'data.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/get')
def query_example():
    user = request.args.get('username')
    balance = query_db('select balance from users where username = ?', [user], one=True)
    bal = 0

    if balance:
        bal = balance[0]

    return {"balance": bal}


@app.route('/update')
def form_example():
    con = sqlite3.connect("data.db")
    cursor = con.cursor()
    user = request.args.get('username')
    minus = request.args.get('minus')
    balance = query_db('select balance from users where username = ?', [user], one=True)
    minus = int(minus)
    balance = int(balance[0])

    if minus <= balance:
        num = balance - minus
        cursor.execute(f"update users set balance={num} WHERE username='{user}'")
        con.commit()

    balance = query_db('select balance from users where username = ?', [user], one=True)

    return {'balance': balance[0]}


@app.route('/sale')
def sale():
    con = sqlite3.connect("data.db")
    cursor = con.cursor()
    user = request.args.get('username')
    plus = request.args.get('plus')
    balance = query_db('select balance from users where username = ?', [user], one=True)
    plus = int(plus)
    balance = int(balance[0])

    num = balance + plus
    cursor.execute(f"update users set balance={num} WHERE username='{user}'")
    con.commit()

    balance = query_db('select balance from users where username = ?', [user], one=True)

    return {'balance': balance[0]}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
