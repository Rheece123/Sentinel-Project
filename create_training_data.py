# This script will be used to collect all of the images in the positive
# and negative folder to create the model. The images saved in the positive
# and negative folder are loaded and read as greyscale. Then a mean value
# is took from all of the files and this is used to create the model. All
# of this data is saved as a XML file. 


import fnmatch
import os
import cv2
import numpy as np
import config
import face


MEAN_FILE = "mean.png"
POSITIVE_EIGENFACE_FILE = "positive_eigenface.png"
NEGATIVE_EIGENFACE_FILE = "negative_eigenface.png"


def walk_files(directory, match="*"):
	# This function will iterate through all of the images
	# within the positive and negative folders
	for root, dirs, files in os.walk(directory):
		for filename in fnmatch.filter(files, match):
			yield os.path.join(root, filename)

def prepare_image(filename):
	# Each of the images are converted into a greyscale image
	return face.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

def normalize(X, low, high, dtype=None):
	# This creates the mean value for the positive and negative image
	# model. This is done by normalising all of the data within each
	# image. Normalisation is done to reduce any repetitive data
	X = np.asarray(X)
	minX, maxX = np.min(X), np.max(X)
	# normalize to [0...1]
	X = X - float(minX)
	X = X / float((maxX - minX))
	# scale to [low...high]
	X = X * (high-low)
	X = X + low
	if dtype is None:
		return np.asarray(X)
	return np.asarray(X, dtype=dtype)

if __name__ == "__main__":
	print "Reading training images..."
	faces = []
	labels = []
	pos_count = 0
	neg_count = 0
	# Read all positive images within positive folder
	for filename in walk_files(config.POSITIVE_DIR, "*.pgm"):
		faces.append(prepare_image(filename))
		labels.append(config.POSITIVE_LABEL)
		pos_count += 1
	# Read all negative images within negative folder
	for filename in walk_files(config.NEGATIVE_DIR, "*.pgm"):
		faces.append(prepare_image(filename))
		labels.append(config.NEGATIVE_LABEL)
		neg_count += 1
	# This reads how the number of positive and negative images within
	# each folder
	print "Read", pos_count, "positive images and", neg_count, "negative images."

	# Train model
	print "Training model..."
	model = cv2.createEigenFaceRecognizer()
	model.train(np.asarray(faces), np.asarray(labels))

	# Save model results as XML file
	model.save(config.TRAINING_FILE)
	print "Training data saved to", config.TRAINING_FILE

	# Save mean and eignface images which summarize the face recognition model
	mean = model.getMat("mean").reshape(faces[0].shape)
	cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=np.uint8))
	eigenvectors = model.getMat("eigenvectors")
	pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
	cv2.imwrite(POSITIVE_EIGENFACE_FILE, normalize(pos_eigenvector, 0, 255, dtype=np.uint8))
	neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
	cv2.imwrite(NEGATIVE_EIGENFACE_FILE, normalize(neg_eigenvector, 0, 255, dtype=np.uint8))
