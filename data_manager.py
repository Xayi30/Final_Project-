import json
from account import Account

class DataManager:
    def __init__(self, filename: str):
        """Set up the data manager with the file name."""
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self) -> dict:
        """Read accounts from a JSON file."""
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            accounts = {}
            for acc in data:
                key = (acc['first_name'], acc['last_name'])
                accounts[key] = Account(acc['first_name'], acc['last_name'], acc['pin'], acc['balance'])
            return accounts
        except FileNotFoundError:
            return {}

    def save_accounts(self):
        """Write accounts to a JSON file."""
        data = [
            {
                'first_name': acc.first_name,
                'last_name': acc.last_name,
                'pin': acc.pin,
                'balance': acc.balance,
            }
            for acc in self.accounts.values()
        ]
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def create_account(self, first_name: str, last_name: str, pin: str, balance: float = 0.0):
        """Add a new account and save it."""
        if not first_name or not last_name or not pin:
            raise ValueError("All fields must be filled.")
        if len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be 4 numbers.")
        if balance < 0:
            raise ValueError("Balance can't be negative.")

        key = (first_name, last_name)
        if key in self.accounts:
            raise ValueError("This account already exists.")

        self.accounts[key] = Account(first_name, last_name, pin, balance)
        self.save_accounts()

