# Bank Project

I built this project as part of my coursework to practice Python, mainly Object-Oriented Programming and file handling.  
It’s a simple banking system where a user can create an account, log in, and do basic banking operations.

---

## Features
### Account Management
- Create a new account (Checking, Savings, or both).
- Open a sub-account later if needed (for example, add Savings if you only had Checking).
- Log in with ID and password.

### Banking Operations
- Deposit money into Checking or Savings.
- Withdraw money:
  - Maximum $100 per transaction.
  - $35 overdraft fee if the balance is not enough.
  - After 2 overdrafts, the account becomes inactive until enough money is deposited.
- Transfer money:
  - Between your own accounts (Checking ↔ Savings).
  - To another customer using their ID.

### Other
- View account information (ID, name, balances, status, overdrafts).
- Log out safely.

---

## How It Works
All account data is saved in a **`bank.csv`** file.  
Every action (deposit, withdraw, transfer, etc.) updates the file right away.  
This way the program stays simple and doesn’t need a database.

---

## Tools Used
| Tool        | Purpose                 |
|-------------|-------------------------|
| Python      | Main programming        |
| CSV         | Store accounts/balances |
| Git & GitHub| Version control         |
| VS Code     | Writing and testing     |

---

## Challenges
The hardest parts were handling different cases, not just the easy ones.  
For example:
- Trying to deposit into a Savings account that doesn’t exist.  
- Transferring money to another user who doesn’t have the requested account.  
- Making overdrafts work correctly (fees, limits, deactivation).  
- Making sure the system always shows the right messages.  

---

## What I Learned
- How to read from and update CSV files in Python.  
- How to organize code with classes and methods.  
- The importance of checking edge cases.  
- How overdrafts and account status can be tracked step by step.  
- Using Git/GitHub to keep track of progress.  
- Testing features one by one.  

---

## Future Ideas
- Add a transaction history.  
- Allow viewing details of a specific transaction.  
- Write automated tests for deposits, withdrawals, and transfers.  

---

