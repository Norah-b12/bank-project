import csv
class Account:
    def __init__(self, acc_id, first, last, pw, checking, savings, active, overdraft):
        self.acc_id = acc_id
        self.first = first
        self.last = last
        self.pw = pw
        self.checking = int(checking) if checking.isdigit()else 0
        self.savings = int(savings) if savings.isdigit()else 0
        self.active = active
        self.overdraft = int(overdraft)
        self.checking = int(checking) if checking.isdigit() else None
        self.savings = int(savings) if savings.isdigit() else None
        self.has_checking = (self.checking is not None)
        self.has_savings = (self.savings is not None)
    def _write_back(self):
        rows = []
        with open("bank.csv", "r", newline="") as f:
            r = csv.reader(f)
            for row in r:
                if not row:
                    rows.append(row)
                    continue
                if row[0].lower() == "id":
                    rows.append(row)
                    continue
                if row[0] == self.acc_id:
                    row[4] = str(self.checking) if self.has_checking else "False"
                    row[5] = str(self.savings) if self.has_savings else "False"
                rows.append(row)
        with open("bank.csv", "w", newline="") as f:
            csv.writer(f).writerows(rows)
    def open_subaccount(self, kind, initial_amount):
        initial_amount = int(initial_amount)
        if kind == "checking":
            self.has_checking = True
            self.checking = initial_amount
            self._write_back()
            print(f"Checking account opened with balance = {self.checking}")

        elif kind == "savings":
            self.has_savings = True
            self.savings = initial_amount
            self._write_back()
            print(f"Savings account opened with balance = {self.savings}")


    def view_info(self):
        print("\n== Your Info ==")
        print("ID: " + self.acc_id)
        print("Name: " + self.first + " " + self.last)
        print("Checking: " + str(self.checking))
        print("Savings: " + str(self.savings))
        print("Active: " + self.active)
        print("Overdraft count: " + str(self.overdraft))

class Deposit:
    def __init__(self, account):
        self.account = account  
    def do(self):
        print("\n== Deposit ==")
        print("1) Deposit to Checking")
        print("2) Deposit to Savings")
        choice = input("Choose account [1/2]: ").strip()

        if choice == "1":
            if not self.account.has_checking:
                print("You don’t have a checking account. Use option (6) to open one first.")
                return
            amount = input("Enter amount to deposit to Checking: ").strip()
            if amount.isdigit():
                self.account.checking += int(amount)
                self.account._write_back()
                print(f"Deposit successful. New Checking balance = {self.account.checking}")
            else:
                print("Invalid amount. Please enter a number.")
        elif choice == "2":
            if not self.account.has_savings:
                print("You don’t have a savings account. Use option (6) to open one first.")
                return
            amount = input("Enter amount to deposit to Savings: ").strip()
            if amount.isdigit():
                self.account.savings += int(amount)
                self.account._write_back()
                print(f"Deposit successful. New Savings balance = {self.account.savings}")
            else:
                print("Invalid amount. Please enter a number.")

        else:
            print("Invalid choice.")

class Withdraw:
    def __init__(self, account):
        self.account = account

    def do(self):
        print("\n== Withdraw ==")
        print("1) Withdraw from Checking")
        print("2) Withdraw from Savings")
        choice = input("Choose account [1/2]: ").strip()

        if choice == "1":
            if not self.account.has_checking:
                print("You don’t have a checking account.")
                return
            amount = input("Enter amount to withdraw from Checking: ").strip()
            if amount.isdigit():
                amount = int(amount)
                if amount > self.account.checking:
                    print("Insufficient funds in Checking.")
                else:
                    self.account.checking -= amount
                    self.account._write_back()
                    print(f"Withdraw successful. New Checking balance = {self.account.checking}")
            else:
                print("Invalid amount. Please enter a number.")

        elif choice == "2":
            if not self.account.has_savings:
                print("You don’t have a savings account.")
                return
            amount = input("Enter amount to withdraw from Savings: ").strip()
            if amount.isdigit():
                amount = int(amount)
                if amount > self.account.savings:
                    print("Insufficient funds in Savings.")
                else:
                    self.account.savings -= amount
                    self.account._write_back()
                    print(f"Withdraw successful. New Savings balance = {self.account.savings}")
            else:
                print("Invalid amount. Please enter a number.")

        else:
            print("Invalid choice.")

class Bank:
    def __init__(self):
        pass  

    def login(self):
        print("\n== Log in ==")
        user_id = input("Please Enter your ID: ").strip()
        user_pw = input("Please Enter your password: ").strip()
        
        with open("bank.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].lower() == "id":
                    continue
                if user_id == row[0] and user_pw == row[3]:
                    print("Login successful Welcome " + row[1] + " " + row[2])
                    acc=Account(*row)
                    self.user_menu(acc)
                    return
        print("Information is not correct.\n")
    def user_menu(self, acc):
        while True:
            print("Welcome")
            print("1) View my info")
            print("2) Deposite")
            print("3) Withdraw")
            print("4) Transfer")
            print("5) Overdraft / Account status")
            print("6) open new account Checking / Savings")
            print("7) Logout ")
            userchoice = input("Choose: ").strip()
            if userchoice == "1":
                acc.view_info()
            
                input("\nPress Enter to continue...")  

            elif userchoice == "2":
                d=Deposit(acc)
                d.do()
                input("Press Enter to continue...")
            elif userchoice == "3":
                w=Withdraw(acc)
                w.do()
                input("Press Enter to continue...")
            elif userchoice == "6":
                print("\n== Open Accounts ==")
                print("1) Open Checking")
                print("2) Open Savings")
                ch = input("Choose [1/2]: ").strip()

                if ch == "1":
                    if acc.has_checking:
                        print("You already have a checking account.")
                    else:
                        amt = input("Initial deposit for Checking (0 or more): ").strip()
                        if amt.isdigit():
                            acc.open_subaccount("checking", amt)
                        else:
                            print("Amount must be a number.")

                elif ch == "2":
                    if acc.has_savings:
                        amt = input("Initial deposit for Savings (0 or more): ").strip()
                        if amt.isdigit():
                            acc.open_subaccount("savings", amt)
                        else:
                            print("Amount must be a number.")
                    else:
                        print("Invalid choice.")
    def create_account(self):
        print("\n== Create Account ==")
        first = input("Enter your First name: ").strip()
        last = input("Enter your Last name : ").strip()
        pw = input("Enter your Password : ").strip()

        print("Choose account type:")
        print(" 1) Checking only")
        print(" 2) Savings only")
        print(" 3) Both")
        choice = input("Select [1/2/3]: ").strip().upper()
        while choice not in ("1", "2", "3"):
            print("Invalid choice. Please enter 1, 2, or 3.")
            choice = input("Select [1/2/3]: ").strip().upper()

        def ask_amount(label):
            while True:
                raw = input("Initial deposit for " + label + ": ").strip()
                if raw.isdigit():  
                    return raw
                print("Invalid amount. Please enter a number (0 or more).")

        checking = "False"
        savings = "False"
        if choice == "1":
            checking = ask_amount("checking")
        elif choice == "2":
            savings = ask_amount("savings")
        else: 
            checking = ask_amount("checking")
            savings = ask_amount("savings")

        with open("bank.csv") as f:
            r = csv.reader(f)
            ids = [int(row[0]) for row in r if row and row[0].isdigit()]
            new_id = str(max(ids) + 1) if ids else "10001"

        with open("bank.csv", "a+", newline="") as f:
            w = csv.writer(f)
            w.writerow([new_id, first, last, pw, checking, savings, "True", "0"])

        print("Account created successfully. Your ID is " + new_id + "\n")


bank = Bank()
while True:
    
    print("------------------------------------------------------")
    print("          🏦   Welcome to ACME Bank   🏦             ")
    print("------------------------------------------------------")
    print("1) Log in")
    print("2) Create Account")
    print("3) Exit")
    choice = input("Choose: ").strip()

    if choice == "1":
        bank.login()
        input("press anything to continue")
    elif choice == "2":
        bank.create_account()
        input("press anything to continue")
    elif choice == "3":
        print("Bye")
        break
    

