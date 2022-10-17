import sqlite3 as sq
from start_config import bot
def sql_start():
    global base, cur
    base = sq.connect('translate_base')
    cur = base.cursor()
    if base:
        print('Data base connected OK')

    base.execute('''CREATE TABLE IF NOT EXISTS own_user(
    user_name TEXT,
    user_id TEXT
    )''')

    base.execute('''CREATE TABLE IF NOT EXISTS u_data(
    from_user TEXT,
    to_user TEXT,
    language TEXT
    )''')

    base.commit()

#Добавление username and user_id после нажатия /start
async def sql_add_own_user(data):
    own = cur.execute('SELECT * FROM own_user WHERE user_id=?', (data[-1],))
    if own.fetchone() is None:
        cur.execute('INSERT INTO own_user VALUES (?, ?)', (data),)
        base.commit()
    else:
        return

# Добавление значений из FSM
async def sql_add_to_user(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO u_data VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

# Чтение own таблицы
async def sql_read_own_user(a):
    cur.execute('SELECT * FROM own_user WHERE user_name=(?)', (a,))
    return cur

# Чтение FSM таблицы
async def sql_read_to_user(a):
    cur.execute('SELECT * FROM u_data WHERE from_user=(?)', (a,))
    return cur

# Разрыв связи и удаление строк из FSM таблицы
async def sql_delete_command(dell):
    cur.execute('DELETE FROM u_data WHERE from_user=(?)', (dell, ))
    cur.execute('DELETE FROM u_data WHERE to_user=(?)', (dell, ))
    print(cur.fetchall())
    base.commit()


