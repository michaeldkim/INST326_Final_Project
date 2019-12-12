#!/usr/bin/env python3

import csv
import sqlite3

menu = '''Do you want to:
1. Store an account
2. Retrieve account information
3. Update an existing account
4. Delete an account
5. Quit'''

# This function deletes the account information given a nickname
def delete_account(nickname, cursor):
    action='''DELETE FROM passwords WHERE nickname = '{}' '''.format(nickname)
    if (nickname_available(nickname, cursor) == False):
        cursor.execute(action)

# This function retrieves all of the information given a nickname
def retrieve_account(nickname, cursor):
    action='''SELECT * FROM passwords WHERE nickname = '{}' '''.format(nickname)
    cursor.execute(action)
    records = cursor.fetchall()
    print("\nNickname: " + str(records[0][0]) +
            "\nUsername: " + str(records[0][1]) +
            "\nPassword: " + str(records[0][2]))

# This function checks if a nickname is already present in the database.
def nickname_available(nickname, cursor):
    cursor.execute('''SELECT nickname FROM passwords''')
    list = cursor.fetchall()
    for i in list:
        if (nickname == ''.join(i)):
            return False
    return True

def main():
    conn = sqlite3.connect('password.db')
    cursor = conn.cursor()

    print('Welome to Password Saver')
    print('\n' + menu)
    user_input = input("Enter a number: ")

    while user_input != '5':
        # STORE PASSWORD
        if user_input == '1':
            # create table for first time users
            cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                    (nickname TEXT,
                    username TEXT,
                    password TEXT)''')

            nickname = input('Enter a nickname: ')
            if nickname_available(nickname.lower(), cursor):
                username = input('Enter a username or email address: ')
                password = input('Enter a password: ')

                cursor.execute('INSERT INTO passwords VALUES (?, ?, ?)',
                            (nickname.lower(), username, password))
            else:
                print('This nickname is already taken!')
            conn.commit()
        # RETRIEVE PASSWORD
        elif user_input == '2':
            nickname = input('Enter the nickname of the account: ')
            retrieve_account(nickname, cursor)
            conn.commit()

        # DELETE PASSWORD
        elif user_input == '4':
            nickname = input('Enter the nickname of the account: ')
            delete_account(nickname, cursor)
            print("Successfully Deleted!")
            conn.commit()

        print('\n' + menu)
        user_input = input("Enter a number: ")

    print('\nGoodbye!')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
