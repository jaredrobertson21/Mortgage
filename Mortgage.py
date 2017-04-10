# Interface for a mortgage calculator tool

from tkinter import *
from tkinter import ttk

def calculatePayments(*args):
    try:
        monthlyIR = IR.get() / 12 / 100
        numPayments = amortization.get() * 12
        paymentMonthly.set(round(monthlyIR * principal.get() * (1 + monthlyIR)**numPayments /
                                 ((1 + monthlyIR)**numPayments - 1), 2))
    except:
        paymentMonthly.set("Error")

# Begin GUI design
root = Tk()
root.title("Mortgage Calculator")
mainframe = ttk.Frame(root, padding = "3 3 12 12")  # root does not inherit themed widgets, frame does
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)  # frame resizes with window
mainframe.rowconfigure(0, weight=1)

principal = DoubleVar()
principal.set(250000)
IR = DoubleVar()
IR.set(2.54)
amortization = DoubleVar()
amortization.set(25)
paymentMonthly = DoubleVar()

ttk.Label(mainframe, text = "Mortgage Payments").grid(column = 1, row = 1, columnspan = 2)
ttk.Label(mainframe, text = "Loan amount ($):").grid(column = 1, row = 2, sticky = (W))
ttk.Label(mainframe, text = "Annual interest rate (%):").grid(column = 1, row = 3, sticky = (W))
ttk.Label(mainframe, text = "Amortization period (years):").grid(column = 1, row = 4, sticky = (W))
ttk.Label(mainframe, text = "Monthly payment:").grid(column = 1, row = 5, sticky = (W))
ttk.Label(mainframe, textvariable = paymentMonthly).grid(column = 2, row = 5, sticky = (W))

principalEntry = ttk.Entry(mainframe, width = 10, textvariable = principal)
principalEntry.grid(column = 2, row = 2, sticky = (W))  # needs to be separated for focus attribute below
interestEntry = ttk.Entry(mainframe, width = 5, textvariable = IR).grid(column = 2, row = 3, sticky = (W))
amortizationEntry = ttk.Entry(mainframe, width = 5, textvariable = amortization).grid(column = 2, row = 4, sticky = (W))

ttk.Button(mainframe, text = "Calculate", command = calculatePayments).grid(column = 2, row = 6, sticky = (W))

for child in mainframe.winfo_children():  # Add padding for all widgets
    child.grid_configure(padx = 5, pady = 2)
principalEntry.focus()
root.bind('<Return>', calculatePayments)  # Pressing return calculates payments

root.mainloop()
