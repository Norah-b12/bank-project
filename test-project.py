import os
import io
import csv
import unittest
import tempfile
from contextlib import redirect_stdout
from unittest.mock import patch

from banking import Account, Deposit, Withdraw, Bank


def write_rows(path, rows):
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)


def read_row_by_id(path, acc_id):
    with open(path, "r", newline="") as f:
        r = csv.reader(f)
        for row in r:
            if row and row[0] == str(acc_id):
                return row
    return None


class SimpleBankTests(unittest.TestCase):
    def setUp(self):
     
        self.tmpdir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir.name)

        self.csv_path = os.path.join(self.tmpdir.name, "bank.csv")
        rows = [
            ["id","first_name","last_name","password","checking","savings","active","overdraft_count"],
            ["10001","Norah","Almana","pw1","500","False","True","0"],  # checking فقط
        ]
        write_rows(self.csv_path, rows)

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.tmpdir.cleanup()

   
    def test_login_success_and_fail(self):
        bank = Bank()
        with patch.object(Bank, "user_menu", lambda self, acc: None):
            
            fake_in = ["10001", "pw1"]
            out = io.StringIO()
            with patch("builtins.input", side_effect=fake_in), redirect_stdout(out):
                bank.login()
            self.assertIn("Login successful", out.getvalue())

           
            fake_in = ["10001", "wrong"]
            out = io.StringIO()
            with patch("builtins.input", side_effect=fake_in), redirect_stdout(out):
                bank.login()
            self.assertIn("Information is not correct", out.getvalue())

    
    def test_deposit_checking(self):
        acc = Account(*read_row_by_id(self.csv_path, "10001"))
        d = Deposit(acc)
        fake_in = ["1", "200"]  
        out = io.StringIO()
        with patch("builtins.input", side_effect=fake_in), redirect_stdout(out):
            d.do()
        row_after = read_row_by_id(self.csv_path, "10001")
        self.assertEqual(row_after[4], "700")  


    def test_withdraw_overdraft(self):
        acc = Account(*read_row_by_id(self.csv_path, "10001"))
        w = Withdraw(acc)
        fake_in = ["1", "600"] 
        out = io.StringIO()
        with patch("builtins.input", side_effect=fake_in), redirect_stdout(out):
            w.do()
        self.assertIn("Overdraft occurred", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
