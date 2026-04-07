# =============================================================================
# Python OOPs Assignment - main.py
# Problems: Bank Account | Employee Management | Vehicle Rental
# =============================================================================


# =============================================================================
# Problem 1: Bank Account
# =============================================================================

class BankAccount:
    """Base class representing a generic bank account."""

    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.__balance = initial_balance  # Encapsulated balance (private)

    @property
    def balance(self):
        """Read-only access to the private balance."""
        return self.__balance

    def deposit(self, amount):
        """Deposit a positive amount into the account."""
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.__balance += amount
        print(f"Deposited ₹{amount:.2f}. New balance: ₹{self.__balance:.2f}")

    def withdraw(self, amount):
        """Withdraw amount; subclasses may add extra constraints."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.__balance:
            print("Insufficient funds.")
            return False
        self.__balance -= amount
        print(f"Withdrawn ₹{amount:.2f}. New balance: ₹{self.__balance:.2f}")
        return True

    def __str__(self):
        return (f"Account No: {self.account_number} | "
                f"Balance: ₹{self.__balance:.2f}")


class SavingsAccount(BankAccount):
    """Savings account with an interest rate."""

    def __init__(self, account_number, initial_balance=0, interest_rate=0.04):
        super().__init__(account_number, initial_balance)
        self.interest_rate = interest_rate  # e.g. 0.04 = 4%

    def calculate_interest(self):
        """Calculate and return annual interest on current balance."""
        interest = self.balance * self.interest_rate
        print(f"Interest ({self.interest_rate * 100}%): ₹{interest:.2f}")
        return interest

    def __str__(self):
        return (f"[Savings] {super().__str__()} | "
                f"Interest Rate: {self.interest_rate * 100}%")


class CurrentAccount(BankAccount):
    """Current account with a minimum balance requirement."""

    def __init__(self, account_number, initial_balance=0, min_balance=1000):
        super().__init__(account_number, initial_balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        """Override withdraw to enforce minimum balance."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if (self.balance - amount) < self.min_balance:
            print(f"Cannot withdraw. Minimum balance of ₹{self.min_balance} "
                  f"must be maintained.")
            return False
        # Reuse parent logic (balance check already handled above)
        return super().withdraw(amount)

    def __str__(self):
        return (f"[Current] {super().__str__()} | "
                f"Min Balance: ₹{self.min_balance:.2f}")


# =============================================================================
# Problem 2: Employee Management
# =============================================================================

class Employee:
    """Base class representing a generic employee."""

    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_salary(self):
        """Return the salary; overridden by subclasses."""
        return self.base_salary

    def __str__(self):
        return (f"Employee: {self.name} | "
                f"Salary: ₹{self.calculate_salary():,.2f}")


class RegularEmployee(Employee):
    """Full-time employee with a fixed bonus."""

    def __init__(self, name, base_salary, bonus=5000):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        """Base salary + fixed bonus."""
        return self.base_salary + self.bonus

    def __str__(self):
        return (f"[Regular] {self.name} | Base: ₹{self.base_salary:,.2f} | "
                f"Bonus: ₹{self.bonus:,.2f} | "
                f"Total: ₹{self.calculate_salary():,.2f}")


class ContractEmployee(Employee):
    """Contract employee paid by hours worked."""

    def __init__(self, name, hourly_rate, hours_worked):
        # base_salary is not fixed; store components separately
        super().__init__(name, base_salary=0)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self):
        """Salary = hourly rate × hours worked."""
        return self.hourly_rate * self.hours_worked

    def __str__(self):
        return (f"[Contract] {self.name} | Rate: ₹{self.hourly_rate}/hr | "
                f"Hours: {self.hours_worked} | "
                f"Total: ₹{self.calculate_salary():,.2f}")


class Manager(Employee):
    """Manager with base salary, bonus, and team allowance."""

    def __init__(self, name, base_salary, bonus=10000, team_size=5):
        super().__init__(name, base_salary)
        self.bonus = bonus
        self.team_size = team_size
        self.team_allowance_per_member = 1000  # ₹1000 per team member

    def calculate_salary(self):
        """Salary = base + bonus + team allowance."""
        team_allowance = self.team_size * self.team_allowance_per_member
        return self.base_salary + self.bonus + team_allowance

    def __str__(self):
        team_allowance = self.team_size * self.team_allowance_per_member
        return (f"[Manager] {self.name} | Base: ₹{self.base_salary:,.2f} | "
                f"Bonus: ₹{self.bonus:,.2f} | "
                f"Team Allowance: ₹{team_allowance:,.2f} | "
                f"Total: ₹{self.calculate_salary():,.2f}")


# =============================================================================
# Problem 3: Vehicle Rental
# =============================================================================

class Vehicle:
    """Base class representing a rentable vehicle."""

    def __init__(self, model, rental_rate):
        self.model = model
        self.rental_rate = rental_rate  # Rate per day

    def calculate_rental(self, days):
        """Base rental cost = rate × days."""
        return self.rental_rate * days

    def __str__(self):
        return f"Vehicle: {self.model} | Rate: ₹{self.rental_rate}/day"


class Car(Vehicle):
    """Car with an optional driver charge."""

    def __init__(self, model, rental_rate, with_driver=False):
        super().__init__(model, rental_rate)
        self.with_driver = with_driver
        self.driver_charge_per_day = 500  # ₹500/day for driver

    def calculate_rental(self, days):
        """Car rental + optional driver charge."""
        base = super().calculate_rental(days)
        driver_cost = (self.driver_charge_per_day * days) if self.with_driver else 0
        return base + driver_cost

    def __str__(self):
        driver = "With Driver" if self.with_driver else "Self Drive"
        return f"[Car] {self.model} | {driver} | Rate: ₹{self.rental_rate}/day"


class Bike(Vehicle):
    """Bike with a per-km fuel surcharge."""

    def __init__(self, model, rental_rate, km_per_day=50):
        super().__init__(model, rental_rate)
        self.km_per_day = km_per_day   # Expected km/day
        self.fuel_rate_per_km = 5      # ₹5 per km

    def calculate_rental(self, days):
        """Bike rental + estimated fuel cost."""
        base = super().calculate_rental(days)
        fuel_cost = self.km_per_day * self.fuel_rate_per_km * days
        return base + fuel_cost

    def __str__(self):
        return (f"[Bike] {self.model} | Rate: ₹{self.rental_rate}/day | "
                f"Est. {self.km_per_day} km/day")


class Truck(Vehicle):
    """Truck with weight-based surcharge."""

    def __init__(self, model, rental_rate, load_tons=1):
        super().__init__(model, rental_rate)
        self.load_tons = load_tons
        self.surcharge_per_ton = 200   # ₹200 per ton per day

    def calculate_rental(self, days):
        """Truck rental + load surcharge."""
        base = super().calculate_rental(days)
        load_cost = self.load_tons * self.surcharge_per_ton * days
        return base + load_cost

    def __str__(self):
        return (f"[Truck] {self.model} | Rate: ₹{self.rental_rate}/day | "
                f"Load: {self.load_tons} ton(s)")


# =============================================================================
# Demo / Testing
# =============================================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PROBLEM 1: BANK ACCOUNT")
    print("=" * 60)

    savings = SavingsAccount("SA001", initial_balance=10000, interest_rate=0.05)
    print(savings)
    savings.deposit(5000)
    savings.withdraw(3000)
    savings.calculate_interest()

    print()

    current = CurrentAccount("CA001", initial_balance=5000, min_balance=1000)
    print(current)
    current.withdraw(4500)   # Should fail (would breach min balance)
    current.withdraw(3000)   # Should succeed
    current.deposit(2000)

    print("\n" + "=" * 60)
    print("PROBLEM 2: EMPLOYEE MANAGEMENT")
    print("=" * 60)

    employees = [
        RegularEmployee("Arun Kumar", base_salary=30000, bonus=6000),
        ContractEmployee("Priya Nair", hourly_rate=500, hours_worked=160),
        Manager("Suresh Raj", base_salary=60000, bonus=15000, team_size=8),
    ]

    for emp in employees:
        print(emp)

    print("\n" + "=" * 60)
    print("PROBLEM 3: VEHICLE RENTAL")
    print("=" * 60)

    rental_days = 5
    vehicles = [
        Car("Toyota Innova", rental_rate=2000, with_driver=True),
        Bike("Royal Enfield", rental_rate=500, km_per_day=80),
        Truck("Tata Ace", rental_rate=3000, load_tons=2),
    ]

    for vehicle in vehicles:
        cost = vehicle.calculate_rental(rental_days)
        print(f"{vehicle}")
        print(f"   Rental for {rental_days} days: ₹{cost:,.2f}")

    print("=" * 60)
