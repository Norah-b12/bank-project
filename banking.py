import csv

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
                
        print("Information is not correct.\n")

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
    

