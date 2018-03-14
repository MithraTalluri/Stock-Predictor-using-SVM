import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')

import subprocess
from Tkinter import *
import tkMessageBox
import Tkinter as tk
import sys

dates = []
prices = []

def get_data(filename):
	'''
	Reads data from a file (.csv file) and adds data to
	the lists dates and prices
	'''
	# Use the with as block to open the file and assign it to csvfile
	with open(filename, 'r') as csvfile:
		# csvFileReader allows us to iterate over every row in our csv file
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)	# skipping column names
		for row in csvFileReader:
			dates.append(int(row[0].split('-')[0])) # Only gets day of the month which is at index 0
			prices.append(float(row[1])) # Convert to float for more precision

	return


def gui_call(dates, prices, spreadV, volumeV):

	useSpread = False
	useVolume = False
	useAverage = False

	if (spreadV == 1):
		useSpread = True
	if (volumeV == 1):
		useVolume = True

	print  'The predicted stock price for ' + str(tickerResponse.get().upper()) + ' is ' + str(round(predict_price(dates, prices, 29),2)) + ' (RBF Kernel)'



def predict_price(dates, prices, x):
	dates = np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1

	# Linear support vector regression model.
	# Takes in 3 parameters:
	# 	1. kernel: type of svm
	# 	2. C: penalty parameter of the error term
	# 	3. gamma: defines how far too far is.

	# Two things are required when using an SVR, a line with the largest minimum margin
	# and a line that correctly seperates as many instances as possible. Since we can't have both,
	# C determines how much we want the latter.

	# Next we make a polynomial SVR because in mathfolklore, the no free lunch theorum states that there are no guarantees for one optimization to work better
	# than the other. So we'll try both.

	# Finally, we create one more SVR using a radial basis function. RBF defines similarity to be the eucledian distance between two inputs
	# If both are right on top of each other, the max similarity is one, if too far it is a ze
	svr_lin = SVR(kernel= 'linear', C= 1e3) # 1e3 denotes 1000
	svr_poly = SVR(kernel= 'poly', C= 1e3, degree= 2)
	svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1) # defining the support vector regression models

	svr_rbf.fit(dates, prices) # fitting the data points in the models
	svr_lin.fit(dates, prices)
	svr_poly.fit(dates, prices)
	return svr_rbf.predict(x)[0] # returns predictions from only the RBF model


'''
Class to redirect stdout to the GUI
'''
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        #self.widget.configure(state="disabled")


# Global variables
root            = tk.Tk()          # Creates the window pane for the GUI
tickerResponse  = StringVar()   # Creates a variable for string responses from GUI
text = tk.Text()
spreadV = IntVar()
volumeV = IntVar()
'''
Prints out the header

@param
    none
@return
    none
'''
def headerInfo():
    print "**************************************************"
    #print "*       Stock Predictor       *"
    #print "***************************************************"


def executeJob(dates, prices):
    subprocess.call('clear', shell = True)
    headerInfo()
    gui_call(dates, prices, spreadV.get(), volumeV.get())


def helpDisplay():
    HELP_TEXT = """Click on PREDICT to predict the stock price for a given company.

Click EXIT to quit the GUI. """
    tkMessageBox.showinfo("HELP", HELP_TEXT)

def grabSpecific():
    # Flag to indicate if it's legal or we can pass
    Tickername = str(tickerResponse.get().lower())

    if not Tickername:
	headerInfo()
        print "No Stock Ticker provided! Try again!"
    else:
		get_data('./Data/' + Tickername + '.csv') # calling get_data method by passing the csv file to it
		executeJob(dates, prices)

def exitGUI():
    subprocess.call('clear', shell = True)
    root.destroy()

def setGUI(root):
    # Modify dimensions of root window
    root.title("Stock Predictor")
    #root.geometry("400x400")


    # Add Frames
    leftFrame = Frame(root, bd = 5)
    leftFrame.pack(side=LEFT)

    rightFrame = Frame(root, bd = 10)
    rightFrame.pack(side=RIGHT)

    #------------------------------------------------------------------------#
    #            code to make stdout appear in the GUI                       #

    text.configure(background='dimgrey')
    text.tag_configure("stdout", foreground="white", font=("Arial", 11))
    text.pack(fill = 'both', expand = 'True')
    sys.stdout = TextRedirector(text, "stdout")
    #sys.stderr = TextRedirector(text, "stderr")
    #------------------------------------------------------------------------#

	# Add Information for User Input
    mLabel  = Label(leftFrame, text = "Stock Ticker", fg='blue', font=("Arial", 11), anchor = 'n').pack()
    mEntry  = Entry(leftFrame, width=15, textvariable = tickerResponse, font=("Arial", 11)).pack()


    # Actions for each of the buttons specified
    mbutton2 = Button(leftFrame, command = grabSpecific, text = "Predict", fg='red', anchor='s', font=("Arial", 11))
    mbutton4 = Button(leftFrame, command = helpDisplay, text = " HELP ", fg='red', anchor='s', font=("Arial",11))
    mbutton3 = Button(leftFrame, command = exitGUI,      text = "  EXIT ", fg='red', anchor='s', font=("Arial", 11))
    mbutton2.pack()
    mbutton4.pack()
    mbutton3.pack()


'''
Main function for the GUI. It sets up the GUI, clears screen, prints the header, activates the GUI loop

@param
    none
@returns
    none
'''
def main():
    # Set up the GUI
    setGUI(root)
    root.grid_propagate(False)

    # Clear Screen
    subprocess.call('clear', shell = True)

    # Calls Header
    #headerInfo()

    # Activate the GUI
    root.mainloop()


'''
Driver
'''

if __name__ == '__main__':
	main()
