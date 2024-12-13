class Account:
    def __init__(self, first_name: str, last_name: str, pin: str, balance: float = 0.0):
        """Set up account with name, PIN, and starting balance."""
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount: float) -> bool:
        """Add money to the account."""
        if type(amount) in [int, float] and amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount:.2f}")
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Take money from the account if there is enough balance."""
        if type(amount) in [int, float] and 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: ${amount:.2f}")
            return True
        return False

    def transfer(self, amount: float, recipient) -> bool:
        """Move money to another account."""
        if self.withdraw(amount):
            recipient.deposit(amount)
            self.transaction_history.append(f"Transferred: ${amount:.2f} to {recipient.get_full_name()}")
            return True
        return False

    def check_pin(self, input_pin: str) -> bool:
        """Check if the PIN is correct."""
        return self.pin == input_pin

    def get_full_name(self) -> str:
        """Get the full name of the account holder."""
        return f"{self.first_name} {self.last_name}"

    def show_transaction_history(self):
        """Show all account transactions."""
        for transaction in self.transaction_history:
            print(transaction)

