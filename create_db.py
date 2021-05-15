from psycopg2 import connect
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
        cursor.execute("create database Users_db;")
        print("Success with database.")
    except DuplicateDatabase as e:
        print("Error, that database is already exist.\n", e)
        return result
    cursor.close()
    cnx.close()
    return result


def create_tables(db_name):
    result = None
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute("""create table users (
        id serial,
        username varchar(255),
        hashed_password varchar(60),
        primary key(id)
        );
        create table messages (
        id serial,
        from_id int not null,
        to_id int not null,
        creation_date timestamp,
        primary key(id),
        foreign key(from_id) references users(id),
        foreign key(to_id) references users(id)  
        );
        """)
        print("Success with tables.")
    except DuplicateTable as e:
        print("Error, one of these tables is already exist or both of these tables are already exist.\n", e)
        return result
    cursor.close()
    cnx.close()
    return result


if __name__ == '__main__':
    create_db()
    create_tables('users_db')
