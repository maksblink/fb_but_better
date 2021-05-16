from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"


def create_db():
    result = None
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST)
        cnx.autocommit = True
        cursor = cnx.cursor()
        try:
            cursor.execute("create database Users_db;")
            print("Success with database.")
        except DuplicateDatabase as e:
            print("Error, that database is already exist.\n", e)
            return result
    except OperationalError as e:
        print("Connection error. ", e)
    cursor.close()
    cnx.close()
    return result


def create_tables(db_name):
    result = None
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        try:
            cursor.execute("""create table users (
            id serial,
            username varchar(255) unique,
            hashed_password varchar(80),
            primary key(id)
            );""")
            print("Success with users table.")
        except DuplicateTable as e:
            print("Error, that table is already exist.\n", e)
            return result
        try:
            cursor.execute("""create table messages (
            id serial,
            from_id int not null,
            to_id int not null,
            text varchar(255),
            creation_date timestamp default current_timestamp,
            primary key(id),
            foreign key(from_id) references users(id) on delete cascade,
            foreign key(to_id) references users(id) on delete cascade 
            );""")
            print("Success with messages table.")
        except DuplicateTable as e:
            print("Error, that table is already exist.\n", e)
            return result
    except OperationalError as e:
        print("Connection error. ", e)
    cursor.close()
    cnx.close()
    return result


if __name__ == '__main__':
    create_db()
    create_tables('users_db')
