import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
	"""
	Load shopping data from a CSV file `filename` and convert into a list of
	evidence lists and a list of labels. Return a tuple (evidence, labels).

	evidence should be a list of lists, where each list contains the
	following values, in order:
		- Administrative, an integer
		- Administrative_Duration, a floating point number
		- Informational, an integer
		- Informational_Duration, a floating point number
		- ProductRelated, an integer
		- ProductRelated_Duration, a floating point number
		- BounceRates, a floating point number
		- ExitRates, a floating point number
		- PageValues, a floating point number
		- SpecialDay, a floating point number
		- Month, an index from 0 (January) to 11 (December)
		- OperatingSystems, an integer
		- Browser, an integer
		- Region, an integer
		- TrafficType, an integer
		- VisitorType, an integer 0 (not returning) or 1 (returning)
		- Weekend, an integer 0 (if false) or 1 (if true)

	labels should be the corresponding list of labels, where each label
	is 1 if Revenue is true, and 0 otherwise.
	"""
	f = open(filename, "r")
	evidence = []
	labels = []
	first = True
	count = 0
	for line in f:
		if first == True:
			first = False
		else:
			i = 0
			temp = []
			while i < 17:
				if i == 10:
					indx = 0
					for month in ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
						if month == line.split(',')[i]:
							temp.append(indx)
						indx += 1
				elif line.split(',')[i] == "Returning_Visitor" or line.split(',')[i] == "TRUE":
					temp.append(1)
				elif line.split(',')[i] == "New_Visitor" or line.split(',')[i] == "Other" or line.split(',')[i] == "FALSE":
					temp.append(0)
				elif i == 1 or i == 3 or (i >= 5 and i <= 9):
					temp.append(float(line.split(',')[i]))
				else:
					temp.append(int(line.split(',')[i]))
				i += 1
			remain = line.split(',')[i]
			if (remain == "TRUE\n"):
				labels.append(1)
			else:
				labels.append(0)
			evidence.append(temp)
	thistuple = (evidence, labels)
	return (thistuple)


def train_model(evidence, labels):
	"""
	Given a list of evidence lists and a list of labels, return a
	fitted k-nearest neighbor model (k=1) trained on the data.
	"""
	model = KNeighborsClassifier(n_neighbors=1)
	model.fit(evidence, labels)
	return model

def evaluate(labels, predictions):
	"""
	Given a list of actual labels and a list of predicted labels,
	return a tuple (sensitivity, specificity).

	Assume each label is either a 1 (positive) or 0 (negative).

	`sensitivity` should be a floating-point value from 0 to 1
	representing the "true positive rate": the proportion of
	actual positive labels that were accurately identified.

	`specificity` should be a floating-point value from 0 to 1
	representing the "true negative rate": the proportion of
	actual negative labels that were accurately identified.
	"""
	# collect information of True positive, true negative,
	# false positive and false negative
	total = 0
	truePositive = 0
	trueNegative = 0
	falsePositive = 0
	falseNegative = 0
	for actual, predicted in zip(labels, predictions):
		total += 1
		if actual == predicted:
			if predicted == 1:
				truePositive += 1
			else:
				trueNegative += 1
		else:
			if predicted == 1:
				falsePositive += 1
			else:
				falseNegative += 1
	sensitivity = truePositive / (truePositive + falseNegative)
	specificity = trueNegative / (trueNegative + falsePositive)
	thistuple = (sensitivity, specificity)
	return thistuple

if __name__ == "__main__":
    main()
