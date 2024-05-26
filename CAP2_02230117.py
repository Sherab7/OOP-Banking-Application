import random

# Base class for Bank Accounts
class BankAcc:
    def __init__(self, account_num, password, account_type, balance=0):
        self.account_num = account_num
        self.password = password
        self.account_type = account_type
        self.balance = balance

    # Method to withdraw money from the account
    def withdraw(self, amount):
        if amount > self.balance:
            print("INSUFFICIENT FUND!!! PLEASE CHECK YOUR AMOUNT!!")
        else:
            self.balance -= amount
            print(f"Withdraw Nu.{amount}. New balance is NU.{self.balance}")
            save_acc(self)

    # Method to deposit money into the account
    def deposit(self, amount):
        self.balance += amount
        print(f"Ngultrum deposited= NU.{amount} New balance =NU.{self.balance}")
        save_acc(self)

# Business account class inheriting from BankAcc
class Business(BankAcc):
    def __init__(self, account_num, password, balance=0):
        super().__init__(account_num, password, "Business Account", balance)

# Saving account class inheriting from BankAcc
class Saving(BankAcc):
    def __init__(self, account_num, password, balance=0):
        super().__init__(account_num, password, "Saving Account", balance)

# Function to save account details to a file
def save_acc(bank_acc):
    bank_accs = load_accounts()
    bank_accs[bank_acc.account_num] = bank_acc
    with open('account.txt', 'w') as f:
        for acc in bank_accs.values():
            f.write(f"{acc.account_num},{acc.password},{acc.account_type},{acc.balance}\n")

# Function to load accounts from a file
def load_accounts():
    bank_accs = {}
    try:
        with open("account.txt", "r") as f:
            for line in f:
                account_num, password, account_type, balance = line.strip().split(',')
                balance = float(balance)
                if account_type == 'Business Account':
                    bank_accs[account_num] = Business(account_num, password, balance)
                else:
                    bank_accs[account_num] = Saving(account_num, password, balance)
    except FileNotFoundError:
        pass
    return bank_accs

# Function to create a new account
def create_acc():
    bank_accs = load_accounts()
    while True:
        account_num = str(random.randint(100000000, 999999999))
        if account_num not in bank_accs:
            break
    password = str(random.randint(1000, 9999))
    account_type = input("WHICH ACCOUNT DO YOU WANT TO CREATE:\n1. Saving\n2. Business\n---->").strip().lower()
    if account_type in ['2', 'business']:
        bank_acc = Business(account_num, password)
    else:
        bank_acc = Saving(account_num, password)
    save_acc(bank_acc)
    print(f"ACCOUNT CREATED SUCCESSFULLY!!! \nACCOUNT NUMBER--->{account_num}\nPASSWORD-->{password}")
    return bank_acc

# Function to login to an existing account
def login(bank_accs):
    account_num = input("PLEASE ENTER YOUR ACCOUNT NUMBER!!!---->")
    password = input("PLEASE ENTER YOUR PASSWORD!!!--->")
    acc = bank_accs.get(account_num)
    if acc and acc.password == password:
        print("KUZU ZANGPOLA!! YOUR MONEY UNDER ONE APPLICATION TRUSTED!!\nSuccessfully logged in!!")
        return acc
    else:
        print("PLEASE CHECK YOUR ACCOUNT NUMBER/PASSWORD!!!")
        return None

# Function to send money from one account to another
def send_money(bank_accs, sender):
    recipient_num = input("Enter recipient account number: ")
    recipient = bank_accs.get(recipient_num)
    if not recipient:
        print("PLEASE CHECK THE RECIPIENT ACCOUNT!!!")
        return

    amount = float(input("Enter amount to send: "))
    if sender.balance < amount:
        print("PLEASE CHECK YOUR FUND!!")
        return
    
    sender.withdraw(amount)
    recipient.deposit(amount)
    save_acc(sender)
    save_acc(recipient)
    print(f"Sent Nu.{amount} to account {recipient_num}.")

# Function to delete an account
def delete_account(bank_accs, account):
    del bank_accs[account.account_num]
    with open('account.txt', 'w') as f:
        for acc in bank_accs.values():
            f.write(f"{acc.account_num},{acc.password},{acc.account_type},{acc.balance}\n")
    print(f"Account {account.account_num} deleted successfully.")

# Main function to run the application
def main():
    while True:
        bank_accs = load_accounts()
        print("\n---------------WELCOME TO CST STUDENT BANK----------------------------")
        print("1. Create Account\n2. Login\n3. Exit\n----------------------------------")
        choice = input("Enter choice: ")
        
        if choice == '1':
            create_acc()
        elif choice == '2':
            account = login(bank_accs)
            if account:
                while True:
                    print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Send Money\n5. Delete Account\n6. Logout\n-------------------------------------------------------------------")
                    choice = input("Enter choice: ")
                    if choice == '1':
                        print(f"Your balance is Nu.{account.balance}.")
                    elif choice == '2':
                        account.deposit(float(input("Enter amount to deposit: ")))
                    elif choice == '3':
                        account.withdraw(float(input("Enter amount to withdraw: ")))
                    elif choice == '4':
                        send_money(bank_accs, account)
                    elif choice == '5':
                        delete_account(bank_accs, account)
                        break
                    elif choice == '6':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
