import random
import sqlite3

conn = sqlite3.connect("card.s3db")

cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS card (id INTEGER AUTO INCREMENT, number VARCHAR(16), pin VARCHAR(4), balance INTEGER "
    "DEFAULT 0)")
conn.commit()


def insert_card_num(account, pin_num):  # Inserts card into the DB
    with conn:
        cur.execute("INSERT INTO card (number, pin) VALUES (?,?)", (account, pin_num,))


def get_card_num(account, pin_num):
    with conn:
        return (cur.execute("SELECT number, pin FROM card WHERE number = ? AND pin = ?",
                            (account, pin_num,)).fetchone())


def delete_card(account, pin_num):
    with conn:
        cur.execute("DELETE FROM card WHERE number = ? AND pin = ?", (account, pin_num,))


class CreditCard:
    database = dict()

    def __init__(self):
        self.account_num = None
        self.pin = None
        self.get_account_num()
        self.get_pin()

    def luhn_algorithm(self):
        temp_account_num = ""
        sums = 0
        for i in range(0, 15):  # step one, DO NOT HAVE A 16th DIGIT!
            if i % 2 == 0:  # step two, multiply each even index by 2
                if int(self.account_num[i]) * 2 > 9:  # optional step three, subtract 9 from those over 9
                    temp_account_num += str(int(self.account_num[i]) * 2 - 9)
                else:  # or continue step two
                    temp_account_num += str(int(self.account_num[i]) * 2)
            else:  # step two-b, don't adjust the odd indexes, just add them to our modified account_num
                temp_account_num += self.account_num[i]
            sums += int(temp_account_num[i])  # step four, add the current adjusted num to sum and repeat!
        temp_account_num += str(
            10 - (sums % 10)) if sums % 10 != 0 else "0"  # gets the checksum, which is what ever the sum is % 10
        return temp_account_num[15]  # returns the checksum to our account number as the final digit

    def get_account_num(self):
        self.account_num = "400000"  # our IIN from the given bank in the problem (4 = bank though)
        for _ in range(6, 15):  # 16th digit will be checksum from luhn_algo
            self.account_num += str(random.randint(0, 9))
        self.account_num += self.luhn_algorithm()

    def get_pin(self):
        self.pin = ""
        for _ in range(0, 4):
            self.pin += str(random.randint(0, 9))


terminate = False
logged_in = False
while not terminate:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice = int(input())
    if choice == 1:
        tempCard = CreditCard()
        print("\nYour card has been created")
        print("Your card number:")
        print(tempCard.account_num)
        print("Your card PIN:")
        print(tempCard.pin + "\n")
        insert_card_num(tempCard.account_num, tempCard.pin)  # inserts new user into DB
    elif choice == 2 and terminate == False:
        print("Enter your card number:")
        card_number = str(input())
        print("Enter your PIN:")
        attempt_pin = str(input())
        if get_card_num(card_number, attempt_pin) is None:
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            logged_in = True
    elif choice == 0:
        print("Bye!")
        terminate = True
    else:
        print("\nI'm not sure what you mean, try again\n")

    while logged_in:
        print("1. Balance")
        print("2. Log out")
        print("0. Quit")
        choice = int(input())
        if choice == 1:
            print("\nBalance: 0\n")
        elif choice == 2:
            logged_in = False
            print("\nYou have successfully logged out!\n")
        elif choice == 0:
            print("Bye!")
            terminate = True
            break
