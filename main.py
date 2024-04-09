import psycopg2

from functions import get_structure_db, add_client, get_client_id, add_phone, change_client, delete_phone, delete_client


def main(last_n: str, first_n: str, email: str, phone: str):
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


if __name__ == "__main__":
    last_n = 'Иванов'
    first_n = 'Иван'
    email = 'III1@mail.ru'
    phone = '+79111111111'
    main(last_n, first_n, email, phone)
