# Interface for a mortgage calculator tool
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#from matplotlib import pyplot as plt
from tkinter import *
from tkinter import ttk
import numpy as np

# Calculate the monthly mortgage payment
def calculatePayments(*args):
    try:
        monthlyIR = IR.get() / 12 / 100
        numPayments = amortization.get() * 12
        paymentMonthly.set(round((monthlyIR * principal.get() * (1 + monthlyIR)**numPayments /
                                 ((1 + monthlyIR)**numPayments - 1)),2))

        calculateSchedule(paymentMonthly.get(), int(numPayments))
        return paymentMonthly.get()
    # if user input is invalid
    except TypeError:
       paymentMonthly.set("Enter Number")
    except ZeroDivisionError:
        paymentMonthly.set("#Div/0")

# Calculate interest, principal, and balance in each period
def calculateSchedule(paymentMonthly, numPayments):
    totalPaid = 0
    scheduleArray = np.zeros((numPayments + 1, 4))
    balance = principal.get()
    scheduleArray[0, 3] = balance
    for row in range(numPayments):
        interestPaid = round(balance * (IR.get() / 12 / 100), 2)
        principalPaid = round(paymentMonthly - interestPaid, 2)
        totalPaid += interestPaid + principalPaid
        balance = balance - principalPaid

        scheduleArray[row + 1, 0] = round(totalPaid, 2)
        scheduleArray[row + 1, 1] = round(interestPaid, 2) * 12
        scheduleArray[row + 1, 2] = round(principalPaid, 2) * 12
        # Ensure balance reads zero in the final period (in case of rounding errors)
        if (balance > 10):
            scheduleArray[row + 1, 3] = round(balance, 2)
        else:
            scheduleArray[row + 1, 3] = 0
    drawTable(scheduleArray)
    plotSchedule(scheduleArray)
    return scheduleArray

# Draw the mortgage payment schedule on the intereface
def drawTable(scheduleArray):

    # overwrite existing table
    tableframe = ttk.Frame(root, padding="3 3 12 12")
    tableframe.grid(column=4, row=0, rowspan=2, sticky=(N, W, E, S))
    ttk.Label(tableframe, text="Period").grid(column=1, row=0, sticky=(W))
    ttk.Label(tableframe, text="Total Paid").grid(column=2, row=0, sticky=(W))
    ttk.Label(tableframe, text="Interest").grid(column=3, row=0, sticky=(W))
    ttk.Label(tableframe, text="Principal").grid(column=4, row=0, sticky=(W))
    ttk.Label(tableframe, text="Balance").grid(column=5, row=0, sticky=(W))

    for row in range(0, len(scheduleArray), 12):  # table rows
        for column in range(5):  # table column
            if (column == 0):
                cell = ttk.Label(tableframe, text=int((row / 12)))
            else:
                cell = ttk.Label(tableframe, text="${0:.2f}".format((scheduleArray[row, column - 1])))
            cell.grid(column= (1 + column), row= (1 + row))

def plotSchedule(scheduleArray):

    # overwrite existing plot
    plotframe = ttk.Frame(root, padding="3 3 12 12")
    plotframe.grid(column=0, row=1, sticky=(N, W, E))

    plotContainer = Figure(figsize=(3, 3), dpi=100)
    plotContainer.subplots_adjust(bottom=0.14, left=0.28, right=0.98, top=0.98)
    plotMain = plotContainer.add_subplot(111)
    plotYears = np.arange(0, amortization.get() + 1)
    interestSlice = scheduleArray[:, 1][::12]
    principalSlice = scheduleArray[:, 2][::12]

    plotMain.bar(plotYears, principalSlice, color="green", bottom=interestSlice, label="Principal")
    plotMain.bar(plotYears, interestSlice, color="blue", label="Interest")
    plotMain.set_xlabel("Time (years)")
    plotMain.set_ylabel("Annual Payments ($)")
    plotMain.legend()

    canvas = FigureCanvasTkAgg(plotContainer, master=plotframe)
    canvas.show()
    canvas.get_tk_widget().grid()

# Begin GUI design
root = Tk()
root.title("Mortgage Calculator")

# Mainframe holds input fields for calculation
mainframe = ttk.Frame(root, padding = "3 3 12 12")  # root does not inherit themed widgets, frame does
mainframe.grid(column=0, row=0, sticky=(N, W, E))
mainframe.columnconfigure(0, weight=1)  # frame resizes with window
mainframe.rowconfigure(0, weight=1)

# Tableframe holds the mortgage payment schedule table
tableframe = ttk.Frame(root, padding = "3 3 12 12")
tableframe.grid(column = 4, row = 0, rowspan = 2, sticky=(N, W, E, S))

# Plotframe holds the payment schedule plot
plotframe = ttk.Frame(root, padding = "3 3 12 12")
plotframe.grid(column = 0, row = 1, sticky=(N, W, E))

# Initialize default input values
principal = DoubleVar()
principal.set(250000)
IR = DoubleVar()
IR.set(2.54)
amortization = DoubleVar()
amortization.set(25)
paymentMonthly = DoubleVar()
paymentMonthly.set(0)

ttk.Label(mainframe, text = "Mortgage Payments").grid(column = 1, row = 1, columnspan = 2)
ttk.Label(mainframe, text = "Loan amount ($):").grid(column = 1, row = 2, sticky = (W))
ttk.Label(mainframe, text = "Annual interest rate (%):").grid(column = 1, row = 3, sticky = (W))
ttk.Label(mainframe, text = "Amortization period (years):").grid(column = 1, row = 4, sticky = (W))
ttk.Label(mainframe, text = "Monthly payment ($):").grid(column = 1, row = 5, sticky = (W))
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

# Initialize the payment schedule table
scheduleArray = calculateSchedule(calculatePayments(), int(amortization.get() * 12))

root.mainloop()
# End GUI design
