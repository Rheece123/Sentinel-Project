# This is the main script which authenticates the valid driver's image aganist the negative
# images saved in the training.xml file. The first thing which happens is that the training
# data is loaded from the xml file (takes about 15 seconds with 90 positive images and 400
# negative images). Once the training data has been loaded, the script controlling the picam
# is ran. The camera will then images of the face and compare the detected face within the
# image aganist the positive model (saved within the training.xml file). If the detected face
# has a lower confidence score than the threshold, the script will end. Else if a negative face
# is detected, the camera will take 5 normal images and email those to a gmail account. 


import cv2
import random
import config
import face


if __name__ == "__main__":
	# Load training data into model. The detected face within
	# the image is compared to the model

	print "Loading training data..."
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print "Training data loaded!"
	print " "
	# Initialize camera from the config script
	camera = config.get_camera()

	for i in range(5):
		print "Attempt", i + 1
		
		# Check for the positive face
		image = camera.read()
		# Convert image to grayscale
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image to determine
		# whether there is a detected face within the image taken
		result = face.detect_single(image)

		# If no face is detected, then do not save this image and skip onto the
		# next one
		if result is None:
			print "Could not detect face!"
			print " "
			continue # Can only be nested in a while or for loop

		x, y, w, h = result
		# Crop and resize image to face and remove all of the background
		crop = face.resize(face.crop(image, x, y, w, h))
		# Test face against model
		label, confidence = model.predict(crop)

		# If a positive match is found, green LED light is activated
		if label == config.POSITIVE_LABEL:
			print "Hi Damien"
			print" "
			

		# If a negative face is detected, red LED light is activated and 5 images are taken
		# by camera. These 5 images are sent to gmail account
		else:
			print "Did not detect an authenticated driver"
			print " "
	
