# Updated for Python 3, Jun 11, 2019
#!/usr/bin/python
# OpenCV bindings
import cv2
# To performing path manipulations 
#import os
# Local Binary Pattern function
from skimage.feature import local_binary_pattern
# To calculate a normalized histogram 
from scipy.stats import itemfreq
#from sklearn.preprocessing import normalize
# To read class from file
import csv
# For plotting
import matplotlib.pyplot as plt
# For array manipulations
import numpy as np
# For saving histogram values
# from sklearn.externals import joblib # deprecated in 0.21 (Updated on Jun 11, 2019)
import joblib # pip3 install joblib
# For command line input
import argparse as ap
# Utility Package
import cvutils

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-t", "--testingSet", help="Path to Testing Set", required="True")
parser.add_argument("-l", "--imageLabels", help="Path to Image Label Files", required="True")
args = vars(parser.parse_args())

# Load the List for storing the LBP Histograms, address of images and the corresponding label 
X_name, X_test, y_test = joblib.load("lbp.pkl")

# Store the path of testing images in test_images
test_images = cvutils.imlist(args["testingSet"])
# Dictionary containing image paths as keys and corresponding label as value
test_dic = {}
# Jun 11, 2019: remove 'rb' to avoid this error: _csv.Error: iterator should return strings, not bytes
#with open(args["imageLabels"], 'rb') as csvfile:
with open(args["imageLabels"]) as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        test_dic[row[0]] = int(row[1])

# Dict containing scores
results_all = {}

for test_image in test_images:
    print "\nCalculating Normalized LBP Histogram for {}".format(test_image)
    # Read the image
    im = cv2.imread(test_image)
    # Convert to grayscale as LBP works on grayscale image
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    radius = 3
    # Number of points to be considered as neighbourers 
    no_points = 8 * radius
    # Uniform LBP is used
    lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
    # Calculate the histogram
    x = itemfreq(lbp.ravel())
    # Normalize the histogram
    hist = x[:, 1]/sum(x[:, 1])
    # Display the query image
    results = []
    # For each image in the training dataset
    # Calculate the chi-squared distance and the sort the values
    for index, x in enumerate(X_test):
        #score = cv2.compareHist(np.array(x, dtype=np.float32), np.array(hist, dtype=np.float32), cv2.cv.CV_COMP_CHISQR)
        #Jun 11, 2019 https://stackoverflow.com/questions/40451706/how-to-use-comparehist-function-opencv
        score = cv2.compareHist(np.array(x, dtype=np.float32), np.array(hist, dtype=np.float32), cv2.HISTCMP_CHISQR)
        results.append((X_name[index], round(score, 3)))
    results = sorted(results, key=lambda score: score[1])
    results_all[test_image] = results
    print ("Displaying scores for {} ** \n".format(test_image))# Jun 11, 2019
    for image, score in results:
        print ("{} has score {}".format(image, score)) # Jun 11, 2019

for test_image, results in results_all.items():
    # Read the image
    im = cv2.imread(test_image)
    # Display the results
    nrows = 2
    ncols = 3
    fig, axes = plt.subplots(nrows,ncols)
    fig.suptitle("** Scores for -> {}**".format(test_image))
    for row in range(nrows):
        for col in range(ncols):
            axes[row][col].imshow(cv2.imread(results[row*ncols+col][0]))
            axes[row][col].axis('off')
            axes[row][col].set_title("Score {}".format(results[row*ncols+col][1]))
    fig.canvas.draw()
    im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    cv2.imshow("** Query Image -> {}**".format(test_image), im)
    cv2.imshow("** Scores for -> {}**".format(test_image), im_ts)
    cv2.waitKey()
    cv2.destroyAllWindows()
