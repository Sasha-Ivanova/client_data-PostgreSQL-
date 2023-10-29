import psycopg2

def get_cursor(conn):
    cur = conn.cursor()
    return cur
def get_structure_db(cur):
    cur = get_cursor(conn)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Client(
            client_id SERIAL PRIMARY KEY,
            last_name VARCHAR(30) NOT NULL,
            first_name VARCHAR(30) NOT NULL,
            email VARCHAR(20) NOT NULL,
            UNIQUE(last_name, first_name, email)
            );
            """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone(
            phone_id SERIAL PRIMARY KEY,
            number VARCHAR(12) UNIQUE,
            client_id INTEGER NOT NULL REFERENCES Client(client_id)
            );
            """)
    conn.commit()
    print('Создана структура базы данных!')

def add_client(conn, last_name, first_name,email):
    try:
        cur = get_cursor(conn)
        cur.execute("""
            INSERT INTO Client(last_name, first_name, email)
            VALUES (%s, %s, %s) RETURNING client_id;
            """, (last_name, first_name, email))
        conn.commit()
        print(f'Добавлен новый клиент (id = {cur.fetchone()[0]})')
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print('Клиент с таким именем существует!')

def get_client_id(conn, last_name=None, first_name=None, email=None, phone=None):
    cur = get_cursor(conn)
    if phone == None:
        cur.execute("""
            SELECT client_id FROM Client
            WHERE last_name iLIKE %s AND first_name iLIKE %s AND email iLIKE %s;
            """, (last_name, first_name, email))
        id = cur.fetchone()[0]
        return id
    else:
        cur.execute("""
                    SELECT client_id FROM Phone
                    WHERE number LIKE %s;
                    """, (phone, ))
        id = cur.fetchone()[0]
        return id

def add_phone(conn, client_id, phone):
    try:
        cur = get_cursor(conn)
        cur.execute("""
            INSERT INTO Phone(number, client_id) VALUES(%s, %s);
            """,  (phone, client_id))
        conn.commit()
        print(f'Добавлен номер телефона у клиента с id {client_id}')
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print('Такой номер телефона уже существует!')

def change_client(conn, client_id, last_name=None, first_name=None, email=None, phone=None):
    try:
        cur = get_cursor(conn)
        if phone != None:
            cur.execute("""
                UPDATE Phone SET number=%s WHERE client_id = %s;
                """, (phone, client_id))
            conn.commit()
            print('Номер телефона изменен!')
        else:
            if last_name != None:
                cur.execute("""
                    UPDATE Client SET last_name=%s WHERE client_id = %s;
                    """, (last_name, client_id))
                conn.commit()
                print('Фамилия клиента изменена!')
            elif first_name != None:
                cur.execute("""
                    UPDATE Client SET first_name=%s WHERE client_id = %s;
                    """, (first_name, client_id))
                conn.commit()
                print('Имя клиента изменено!')
            else:
                cur.execute("""
                    UPDATE Client SET email=%s WHERE client_id = %s;
                    """, (email, client_id))
                conn.commit()
                print('Email клиента изменен!')
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print('Такая запись уже существует!')

def delete_phone(conn, client_id, phone):
    cur = get_cursor(conn)
    cur.execute("""
            DELETE FROM Phone WHERE client_id = %s AND number = %s;
            """, (client_id, phone ))
    conn.commit()
    print(f'У клиента с id {client_id} удален телефонный номер {phone}')

def delete_client(conn, client_id):
    cur = get_cursor(conn)
    cur.execute("""
        DELETE FROM Client WHERE client_id = %s;
        """, (client_id, ))
    conn.commit
    print(f'Клиент с id {client_id} удален!')


last_n = 'Иванов'
first_n = 'Иван'
pat = 'Иванович'
email = 'III1@mail.ru'
phone = '+79111111111'


with psycopg2.connect(database="netolog_dz", user='postgres', password="23112019") as conn:
    get_structure_db(conn)
    add_client(conn, last_n, first_n, email)
    client_id = get_client_id(conn, last_name=last_n, first_name=first_n, email=email, phone=None)
    print(f'ID клиента: {client_id}')
    add_phone(conn, client_id, phone)
    client_id = get_client_id(conn, last_name=None, first_name=None, email=None, phone='+79111111111')
    print(f'ID клиента: {client_id}')
    add_phone(conn, client_id, phone)
    change_client(conn, client_id, last_name='Смирнов', first_name=None, email=None, phone=None)
    change_client(conn, client_id, last_name=None, first_name='Алексей', email=None, phone=None)
    change_client(conn, client_id, last_name=None, first_name=None, email='Alex22333@mail.ru', phone=None)
    change_client(conn, client_id, last_name=None, first_name=None, email=None, phone='+79114456234')
    delete_phone(conn, client_id, "+79114456234")
    delete_client(conn, client_id)














