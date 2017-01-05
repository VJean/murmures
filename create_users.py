import sys
from murmures import app, User, db, bcrypt
from getpass import getpass


def main():
    with app.app_context():
        nbusers = len(User.query.all())
        if nbusers > 0:
            print(str(nbusers) + ' user(s) already exist! Create another? (y/n):')
            create = input()
            if create == 'n':
                return

        print('Enter username: ')
        username = input()
        password = getpass()
        assert password == getpass('Password again:')

        user = User()
        user.username = username
        user.password = bcrypt.generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        print('user ' + user.get_id() + ' successfully added.')


if __name__ == '__main__':
    sys.exit(main())
