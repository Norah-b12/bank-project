import csv

class Account:
    def __init__(self, acc_id, first, last, pw, checking, savings, active, overdraft):
        self.acc_id = acc_id
        self.first = first
        self.last = last
        self.pw = pw
        
        try:
            self.checking=int(checking)
        except ValueError:
            self.checking=None
        
        try:
            self.savings=int(savings)
        except ValueError:
            self.savings=None
        self.has_checking = self.checking is not None
        self.has_savings = self.savings is not None

        self.active=str(active).strip().lower()=="true"
        self.overdraft= int(overdraft) if str(overdraft).isdigit() else 0

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
                    row[6] = "True" if self.active else "False"
                    row[7] = str(self.overdraft)
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
        elif kind =="savings":
            self.has_savings = True
            self.savings = initial_amount
            self._write_back()
            print(f"Savings account opened with balance = {self.savings}")
        else:
            print ("Invalid input")


    def view_info(self):
        print("\n== Your Info ==")
        print("ID: " + self.acc_id)
        print("Name: " + self.first + " " + self.last)
        print("Checking: " + str(self.checking))
        print("Savings: " + str(self.savings))
        print("Active: " + "True" if self.active else "False")
        print("Overdraft count: " + str(self.overdraft))
    
    def Status(self):
        print("\n== Account Status ==")
        print(f"Active: {'True' if self.active else 'False'}")
        print(f"Overdraft count: {self.overdraft}")

        if self.has_checking:
            print(f"Checking balance: {self.checking}")
        else:
            print("Checking: None")

        if self.has_savings:
            print(f"Savings balance: {self.savings}")
        else:
            print("Savings: None")


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

    def _write_back(self):
        rows = []
        with open("bank.csv") as f:
            r = csv.reader(f)
            for row in r:
                if not row or row[0].lower() == "id":
                    rows.append(row)
                    continue
                if row[0] == self.account.acc_id:
                    row[4] = str(self.account.checking) if self.account.checking is not None else "False"
                    row[5] = str(self.account.savings) if self.account.savings is not None else "False"
                    row[6] = "True" if self.account.active else "False"
                    row[7] = str(self.account.overdraft)
                rows.append(row)
        with open("bank.csv", "w", newline="") as f:
            csv.writer(f).writerows(rows)

    def do(self):
        print("\n== Withdraw ==")
        print("1) Withdraw from Checking")
        print("2) Withdraw from Savings")
        choice = input("Choose account [1/2]: ").strip()

        if not self.account.active:
            print("Account is deactivated, please deposit to reactivate.")
            return

        if choice == "1":
            if not self.account.has_checking:
                print("You don't have a checking account.")
                return

            amount = input("Enter amount to withdraw from Checking: ").strip()
            if not amount.isdigit():
                print("Invalid amount. Please enter a number.")
                return

            amount = int(amount)
            if amount > 100:
                print("You cannot withdraw more than $100 in one transaction.")
                return

            prev = self.account.checking
            fee = 35 if (prev >= 0 and amount > prev) else 0
            new_balance = prev - amount - fee
            if new_balance < -100:
                if prev >= 0:
                    max_amount = min(100, prev + 65)
                else:
                    max_amount = max(0, min(100, 100 + prev))
                print(f"You can withdraw at most ${max_amount} right now")
                return

            self.account.checking = new_balance
            if fee == 35:
                self.account.overdraft += 1
                print("Overdraft occurred")

            if self.account.overdraft >= 2:
                self.account.active = False
                print("Account deactivated due to multiple overdrafts.")

            self._write_back()
            print(f"Withdraw successful. New Checking balance = {self.account.checking}")

        elif choice == "2":
            if not self.account.has_savings:
                print("You don't have a savings account.")
                return

            amount = input("Enter amount to withdraw from Savings: ").strip()
            if not amount.isdigit():
                print("Invalid amount. Please enter a number.")
                return

            amount = int(amount)
            if amount > 100:
                print("You cannot withdraw more than $100 in one transaction.")
                return

            prev = self.account.savings
            fee = 35 if (prev >= 0 and amount > prev) else 0
            new_balance = prev - amount - fee
            if new_balance < -100:
                if prev >= 0:
                    max_amount = min(100, prev + 65)
                else:
                    max_amount = max(0, min(100, 100 + prev))
                print(f"You can withdraw at most ${max_amount} right now")
                return

            self.account.savings = new_balance
            if fee == 35:
                self.account.overdraft += 1
                print("Overdraft occurred")

            if self.account.overdraft >= 2:
                self.account.active = False
                print("Account deactivated due to multiple overdrafts.")

            self._write_back()
            print(f"Withdraw successful. New Savings balance = {self.account.savings}")

        else:
            print("Invalid choice.")

class Transfer:
    def __init__(self, account):
        self.account = account  

    def _load_account_by_id(self, acc_id):
      
        with open("bank.csv", "r", newline="") as f:
            r = csv.reader(f)
            for row in r:
                if not row or row[0].lower() == "id":
                    continue
                if row[0] == acc_id:
                    return Account(*row)
        return None

    def _write_two(self, a1: 'Account', a2: 'Account'):
      
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

                if row[0] == a1.acc_id:
                    row[4] = str(a1.checking) if a1.has_checking else "False"
                    row[5] = str(a1.savings) if a1.has_savings else "False"
                elif row[0] == a2.acc_id:
                    row[4] = str(a2.checking) if a2.has_checking else "False"
                    row[5] = str(a2.savings) if a2.has_savings else "False"

                rows.append(row)

        with open("bank.csv", "w", newline="") as f:
            csv.writer(f).writerows(rows)

    def do(self):
        print("\n== Transfer ==")
        print("1) Internal: Checking -> Savings")
        print("2) Internal: Savings -> Checking")
        print("3) To another customer by ID")
        choice = input("Choose [1/2/3]: ").strip()

        if choice == "1":
            if not self.account.has_checking:
                print("You don’t have a checking account.")
                return
            if not self.account.has_savings:
                print("You don’t have a savings account.")
                return

            amt = input("Amount to transfer (Checking -> Savings): ").strip()
            if not amt.isdigit():
                print("Invalid amount.")
                return
            amt = int(amt)

            if amt > self.account.checking:
                print("Insufficient funds in Checking.")
                return

            self.account.checking -= amt
            self.account.savings += amt
            self.account._write_back()
            print(f"Done. Checking={self.account.checking}, Savings={self.account.savings}")

        elif choice == "2":

            if not self.account.has_savings:
                print("You don’t have a savings account.")
                return
            if not self.account.has_checking:
                print("You don’t have a checking account.")
                return

            amt = input("Amount to transfer (Savings -> Checking): ").strip()
            if not amt.isdigit():
                print("Invalid amount.")
                return
            amt = int(amt)

            if amt > self.account.savings:
                print("Insufficient funds in Savings.")
                return

            self.account.savings -= amt
            self.account.checking += amt
            self.account._write_back()
            print(f"Done. Checking={self.account.checking}, Savings={self.account.savings}")

        elif choice == "3":
            target_id = input("Enter recipient ID: ").strip()
            target = self._load_account_by_id(target_id)
            if not target:
                print("Target customer not found.")
                return

            print("\nFrom which of your accounts?")
            print("1) From Checking")
            print("2) From Savings")
            from_choice = input("Choose [1/2]: ").strip()

            if from_choice == "1":
                if not self.account.has_checking:
                    print("You don’t have a checking account.")
                    return
                src_attr = "checking"
            elif from_choice == "2":
                if not self.account.has_savings:
                    print("You don’t have a savings account.")
                    return
                src_attr = "savings"
            else:
                print("Invalid choice.")
                return

            print("\nTo which account of the recipient?")
            print("1) To Checking")
            print("2) To Savings")
            to_choice = input("Choose [1/2]: ").strip()

            if to_choice == "1":
                if not target.has_checking:
                    print("Recipient does not have a checking account.")
                    return
                dst_attr = "checking"
            elif to_choice == "2":
                if not target.has_savings:
                    print("Recipient does not have a savings account.")
                    return
                dst_attr = "savings"
            else:
                print("Invalid choice.")
                return

            amt = input("Amount to transfer: ").strip()
            if not amt.isdigit():
                print("Invalid amount.")
                return
            amt = int(amt)

            if getattr(self.account, src_attr) < amt:
                print("Insufficient funds.")
                return

            setattr(self.account, src_attr, getattr(self.account, src_attr) - amt)
            setattr(target, dst_attr, getattr(target, dst_attr) + amt)

          
            self._write_two(self.account, target)
            print("Transfer completed successfully.")

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
            elif userchoice =="4":
                t=Transfer(acc)
                t.do()
                input("Press Enter to continue...")
            elif userchoice == "5":
                acc.Status()
                input("Press Enter to continue...")
            elif userchoice == "6":
                print("\n== Open Accounts ==")
                print("1) Open Checking")
                print("2) Open Savings")
                ch = input("Choose [1/2]: ").strip()
                if ch == "1":
                    if acc.has_checking:
                        print("you already have a checking account")
                    else:
                        amt = input("Initial deposit for Checking (0 or more): ").strip()
                        if amt.isdigit():
                            acc.open_subaccount("checking", amt)
                        else:
                            print("Amount must be a number.")

                elif ch == "2":
                    if acc.has_savings:
                        print("you already have a Saving account")

                    amt = input("Initial deposit for Savings (0 or more): ").strip()
                    if amt.isdigit():
                        acc.open_subaccount("savings", amt)
                    else:
                        print("Amount must be a number.")

                else:
                    print("Invalid choice.")


            elif userchoice =="7":
                print("you are loged out ")
                break
            else:
                print("Incorrect option. enter a valid number from the menu" )
                input("Press Enter to continue...")
                
            
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

        print("Account created successfully. Your ID is " + new_id + "\n---------------you can now log in by useing option (1) ---------------c")

if __name__=="__main__": 
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
            print("Have a good day ")
            break
    

