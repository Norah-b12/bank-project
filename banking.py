import csv
print("------------------------------------------------------")
print("          🏦   Welcome to ACME Bank   🏦             ")
print("------------------------------------------------------")


def login():
    print("please write youre account info")
    userId=input("please write youre ID: ").strip()
    userPassword=input("please write youre password: ").strip()
    with open("bank.csv") as f:
        r=csv.reader(f, delimiter=",")
        for row in r:
            if not row or row[0].lower() =="id":
                continue
            if userId== row[0] and userPassword==row[3]:
                 print("Login successful")
                 return

    print("Login failed")



def creataccount():
    print("Do you want to create an account")
    answer=input()

def cheakUser():
    print("Do you have an account yes or no")
    answer=input()
    if answer== "yes":
        login()
    elif answer== "no":
        creataccount()
    else:
        print("invild plaese write yes or no")

cheakUser()




