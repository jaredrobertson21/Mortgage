# Interface for a mortgage calculator tool

from tkinter import *
from tkinter import ttk

IR = 0.0254 # quoted yearly interest rate
monthlyIR = IR / 12
amortization = 25  # amortization period in years
numPayments = amortization * 12
principal = 238000
paymentMonthly = monthlyIR * principal * (1 + monthlyIR)**numPayments / ((1 + monthlyIR)**numPayments - 1)

root = Tk()
root.title("Mortgage Calculator")
mainframe = ttk.Frame(root, padding = "3 3 12 12")  # root does not inherit themed widgets, frame does
#root.config(bg="blue")
mainframe.columnconfigure(0, weight=1)  # frame resizes with window
mainframe.rowconfigure(0, weight=1)
root.mainloop()
print(paymentMonthly)
