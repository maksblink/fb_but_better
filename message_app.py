import argparse
from models import User, Messages
from psycopg2 import connect, OperationalError
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="send to <username>")
parser.add_argument("-s", "--send", help="content of message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()

username = args.username
password = args.password
to_user = args.to
content = args.send


def list_messages(cursor, username, password):
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        messsages = Messages.load_all_messages(cursor, user.id)
        for message in messsages:
            sender = User.load_user_by_id(cursor, message.from_id)
            print(f"{sender.username, message.text, message.creation_date}")
    else:
        print("Incorrect password.")


def send_message(cursor, username, password, to_user, content):
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        user2 = User.load_user_by_name(cursor, to_user)
        if not user2:
            print("That user does not exist.")
        else:
            if len(content) < 255:
                message = Messages(from_id=user.id, to_id=user2.id, text=content)
                message.save_to_db(cursor)
    else:
        print("Incorrect password.")


if __name__ == '__main__':
    cnx = connect(user="postgres", password="coderslab", host="localhost", database='users_db')
    cnx.autocommit = True
    cursor = cnx.cursor()

    list_messages(cursor, username, password)

    send_message(cursor, username, password, to_user, content)

    cursor.close()
    cnx.close()
