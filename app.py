from datetime import datetime
from breezypythongui import EasyFrame

class myApp(EasyFrame):

    def __init__(self) -> None:
        self.total = float(self.getTotalToSpend())
        self.amountICanSpend = float(self.getAmountICanSpend())
        self.amountIHaveSpent = float(self.getAmountIHaveSpent())
        self.date = self.getCurrentDate()
        
        # Easy Frame
        EasyFrame.__init__(self, title="My Python Food App - Michael Howard")
        
        # Labels
        self.addLabel(text="", row=0, column=0)
        self.addLabel(text="", row=0, column=1)
        self.addLabel(text="", row=0, column=2)
        self.addLabel(text="", row=1, column=0)
        self.addLabel(text="My Food App", row=1, column=1)
        self.addLabel(text="", row=1, column=2)
        self.addLabel(text="Money I Spent So Far", row=2, column=0)
        self.addLabel(text="", row=2, column=1)
        self.addLabel(text="Money I still have left", row=2, column=2)
        
        # Fields
        self.amountSpentField = self.addFloatField(value=self.amountIHaveSpent, row=3, column=0, state="readonly", precision=2)
        self.addLabel(text="", row=3, column=1)
        self.amountLeftField = self.addFloatField(value=self.amountICanSpend, row=3, column=2, state="readonly", precision=2)
        self.addLabel(text="Cost of food: ", row=4, column=0)
        self.output = self.addFloatField(value="0.00", row=4, column=1, precision=2)
        
        # Button
        self.addButton(text="Compute", row=4, column=2, command=self.buyFood)

    def getCurrentDate(self):
        # Returns current day of the month as a string
        return str(datetime.now().day)

    def getTotalToSpend(self):
        with open('database.txt', 'r') as readHandle:
            data = readHandle.readlines()[1].strip()
        return float(format(float(data), '.2f'))  # Line 31

    def replaceLine(self, lineNum, newAmount):
        with open('database.txt', 'r+') as file:
            lines = file.readlines()
            lines[lineNum] = str(newAmount) + "\n"
            file.seek(0)
            file.writelines(lines)
            file.truncate()

    def setTotalToSpend(self, amount):
        date = self.getCurrentDate()
        if date == "01":
            self.total = amount
            self.replaceLine(1, amount)
        else:
            print("Can't change total!")

    def setAmountLeft(self, amount):
        self.amountICanSpend = amount
        self.replaceLine(3, amount)

    def setAmountSpent(self, amount):
        self.amountIHaveSpent = amount
        self.replaceLine(5, amount)

    def getAmountICanSpend(self):
        with open('database.txt') as Handle:
            data = Handle.readlines()[3].strip()
            if data == "":
                return 0.0
            return float(format(float(data), '.2f'))  # Line 58

    def getAmountIHaveSpent(self):
        with open('database.txt') as textHandle:
            data = textHandle.readlines()[5].strip()
            if data == "":
                return 0.0
            return float(format(float(data), '.2f'))  # Line 67

    def buyFood(self):
        # Check if amount is less than the amountIcanSpend
        # Minus amount from amountICanSpend
        # Add amount to amountIHaveSpent
        amount = float(self.output.getNumber())
        moneyLeft = self.amountICanSpend
        
        if amount <= moneyLeft:
            moneyLeft -= amount
            self.amountIHaveSpent += amount
            self.setAmountLeft(moneyLeft)
            self.setAmountSpent(self.amountIHaveSpent)
            self.amountSpentField.setNumber(self.amountIHaveSpent)
            self.amountLeftField.setNumber(moneyLeft)
            print(f"Successfully spent {amount}. Amount left: {moneyLeft}. Amount spent: {self.amountIHaveSpent}.")
        else:
            print("You don't have enough money!!")

####   Methods to call:           ####
####       getCurrentDate         #### 
####       getAmountICanSpend     ####
####       getAmountIHaveSpent    ####
####       getTotalToSpend        ####

instance = myApp().mainloop()
