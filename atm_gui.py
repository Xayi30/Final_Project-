import tkinter as tk
from tkinter import messagebox


class ATMApp:
    def __init__(self, master: tk.Tk, data_manager):
        """Set up the ATM app."""
        self.root = master
        self.data_manager = data_manager
        self.current_account = None

        self.root.title("ATM System")

        # Search Section
        tk.Label(master, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        self.first_name_entry = tk.Entry(master, width=20)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Last Name:").grid(row=1, column=0, padx=10, pady=5)
        self.last_name_entry = tk.Entry(master, width=20)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="PIN:").grid(row=2, column=0, padx=10, pady=5)
        self.pin_entry = tk.Entry(master, show="*", width=20)
        self.pin_entry.grid(row=2, column=1, padx=10, pady=5)

        self.search_button = tk.Button(master, text="Login", command=self.search_account, bg="#a0a0a0", fg="black")
        self.search_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Create Account Button
        self.create_account_button = tk.Button(master, text="Create Account", command=self.open_create_account_window,
                                               bg="#a0a0a0", fg="black")
        self.create_account_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Account Information Section
        self.info_label = tk.Label(master, text="Enter your login information above", font=("Arial", 12))
        self.info_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.balance_label = tk.Label(master, text="Account Balance: $0.00", font=("Arial", 14, "bold"))
        self.balance_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Keypad and Amount Entry Section
        self.amount = tk.StringVar()
        self.amount_entry = tk.Entry(master, textvariable=self.amount, width=30, justify="center", font=("Arial", 14))
        self.amount_entry.grid(row=7, column=0, columnspan=2, pady=10)

        self.keypad_frame = tk.Frame(master)
        self.keypad_frame.grid(row=8, column=0, columnspan=2, pady=10)

        self.create_keypad()

        # Transaction Buttons
        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw, bg="#a0a0a0", fg="black")
        self.withdraw_button.grid(row=9, column=0, pady=10, padx=40)

        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit, bg="#a0a0a0", fg="black")
        self.deposit_button.grid(row=9, column=1, pady=10, padx=5)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit, bg="#a0a0a0", fg="black")
        self.exit_button.grid(row=10, column=0, columnspan=2, pady=10,)

    def create_keypad(self):
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]
        for (text, row, col) in buttons:
            button = tk.Button(self.keypad_frame, text=text, width=5, height=2,
                               command=lambda t=text: self.add_to_amount(t))
            button.grid(row=row, column=col, padx=5, pady=5)

        clear_button = tk.Button(self.keypad_frame, text="Clear", width=5, height=2, command=self.clear_amount,
                                 bg="yellow")
        clear_button.grid(row=3, column=0, padx=5, pady=5)

        delete_button = tk.Button(self.keypad_frame, text="Del", width=5, height=2, command=self.delete_last_digit,
                                  bg="red")
        delete_button.grid(row=3, column=2, padx=5, pady=5)

    def add_to_amount(self, digit: str):
        current_text = self.amount.get()
        new_text = current_text + digit
        self.amount.set(new_text)
        self.amount_entry.icursor(len(new_text))

    def clear_amount(self):
        """Clear the amount box."""
        self.amount.set("")

    def delete_last_digit(self):
        """Delete the last digit in the amount box."""
        self.amount.set(self.amount.get()[:-1])

    def search_account(self):
        """Find the account using name and PIN."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        pin = self.pin_entry.get()

        account_key = (first_name, last_name)
        if account_key in self.data_manager.accounts:
            account = self.data_manager.accounts[account_key]
            if account.pin == pin:
                self.current_account = account
                self.info_label.config(text=f"Welcome, {account.get_full_name()}!", fg="green")
                self.update_balance_display()
                return
        self.info_label.config(text="Invalid login. Please try again.", fg="red")

    def update_balance_display(self):
        """Show the account balance."""
        if self.current_account:
            self.balance_label.config(text=f"Account Balance: ${self.current_account.balance:.2f}")

    def withdraw(self):
        """Withdraw money from the account."""
        if self.current_account is None:
            messagebox.showerror("Error", "Please log in first.")
            return

        try:
            amount = float(self.amount.get())
            if self.current_account.withdraw(amount):
                self.update_balance_display()
                messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
            else:
                messagebox.showerror("Error", "Not enough money or invalid amount.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    def deposit(self):
        """Deposit money into the account."""
        if self.current_account is None:
            messagebox.showerror("Error", "Please log in first.")
            return

        try:
            amount = float(self.amount.get())
            if self.current_account.deposit(amount):
                self.update_balance_display()
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
            else:
                messagebox.showerror("Error", "Invalid amount.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    def open_create_account_window(self):
        """Open a window to make a new account."""
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Account")

        # Input fields
        tk.Label(create_window, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        first_name_entry = tk.Entry(create_window, width=20)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(create_window, text="Last Name:").grid(row=1, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(create_window, width=20)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(create_window, text="PIN (4 digits):").grid(row=2, column=0, padx=10, pady=5)
        pin_entry = tk.Entry(create_window, show="*", width=20)
        pin_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(create_window, text="Initial Balance:").grid(row=3, column=0, padx=10, pady=5)
        balance_entry = tk.Entry(create_window, width=20)
        balance_entry.grid(row=3, column=1, padx=10, pady=5)

        # Create account button
        def create_account_action():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            pin = pin_entry.get()
            balance = balance_entry.get()

            try:
                if balance:
                    balance = float(balance)
                else:
                    balance = 0.0

                self.data_manager.create_account(first_name, last_name, pin, balance)
                messagebox.showinfo("Success", "Account created successfully!")
                create_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for balance.")

        tk.Button(create_window, text="Create Account", command=create_account_action, bg="blue", fg="black").grid(
            row=4, column=0, columnspan=2, pady=10)
