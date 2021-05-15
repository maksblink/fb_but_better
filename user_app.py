import argparse
import models

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
args = parser.parse_args()
hhh = args.username
print(hhh)
print(args.password)

if __name__ != '__main__':
    USER = "postgres"
    HOST = "localhost"
    PASSWORD = "coderslab"

    models.User.load_user_by_name(args.username)

    cnx = connect(user=USER, password=PASSWORD, host=HOST, database='users_db')
    cnx.autocommit = True
    cursor = cnx.cursor()





    cursor.close()
    cnx.close()
