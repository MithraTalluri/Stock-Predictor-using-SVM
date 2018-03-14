'''
Usage:
	predictor.py <ticker>


Arguments:
	<ticker> - ticker symbol for the company

Examples:
	python predictor.py aapl
	python predictor.py tsla
'''

from docopt import docopt
import sys
import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')

# Initialize two empty lists
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

	predict_price(dates, prices, 29)


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

	# This plots the initial data points as black dots with the data label and plot
	# each of our models as well


	plt.scatter(dates, prices, color= 'black', label= 'Data') # plotting the initial datapoints
	# The graphs are plotted with the help of SVR object in scikit-learn using the dates matrix as our parameter.
	# Each will be a distinct color and and give them a distinct label.
	plt.plot(dates, svr_rbf.predict(dates), color= 'red', label= 'RBF model') # plotting the line made by the RBF kernel
	plt.plot(dates,svr_lin.predict(dates), color= 'green', label= 'Linear model') # plotting the line made by linear kernel
	plt.plot(dates,svr_poly.predict(dates), color= 'blue', label= 'Polynomial model') # plotting the line made by polynomial kernel
	plt.xlabel('Date') # Setting the x-axis
	plt.ylabel('Price') # Setting the y-axis
	plt.title('Support Vector Regression') # Setting title
	plt.legend() # Add legend
	plt.show() # To display result on screen

	return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0] # returns predictions from each of our models

def main(args):

	ticker = args['<ticker>']

	get_data('./Data/' + ticker + '.csv') # calling get_data method by passing the csv file to it

	predicted_price = predict_price(dates, prices, 29)

	print('The predicted prices are:', predicted_price)


'''
Calls Main.
Uses Docopt module to parse the command line arguments
'''
if __name__ == '__main__':
	args = docopt(__doc__)
	main(args)
