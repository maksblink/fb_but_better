from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
import argparse
from models import User
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list of users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()

username = args.username
password = args.password
new_password = args.new_pass


def create_user(cursor, username, password):
    if len(password) < 8:
        print("Password is too short, it should be at least 8 characters.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print("User created")
        except UniqueViolation as e:
            print("That user is already exist. ", e)


def list_users(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)


def delete_users(cursor, username, password):
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("User deleted")
    else:
        print("Incorrect password.")


def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is too short, it should be at least 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print("Password changed.")
    else:
        print("Incorrect password.")


if __name__ == '__main__':
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database='users_db')
        cnx.autocommit = True
        cursor = cnx.cursor()

        if username and password and args.edit and new_password:
            edit_user(cursor, username, password, new_password)
        elif username and password and args.delete:
            delete_users(cursor, username, password)
        elif username and password:
            create_user(cursor, username, password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        cursor.close()
        cnx.close()
    except OperationalError as e:
        print("Connection error. ", e)
