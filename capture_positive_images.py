# This script is the first step and captures images of the authorised person's face. The image is then cropped
# to only include the person's first and remove as much of the background as possible. The image is then
# saved as a pgm and saved within the positive directory within the training folder.


import glob
import os
import sys
import select
import cv2
import config
import face


# Prefix for positive training image filename within the training folder
POSITIVE_FILE_PREFIX = "positive_"


if __name__ == "__main__":
	# get_camera imports the picam module and captures an image
	camera = config.get_camera()
	# Find the largest ID of existing positive images and start
	# new images after this ID value
	files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, 
		POSITIVE_FILE_PREFIX + "[0-9][0-9][0-9].pgm")))
	count = 0
	image_number = 0
	if len(files) > 0:
		# Grab the count from the last filename and save next image
		# as positive_00(+1)
		count = int(files[-1][-7:-4])+1
		
	print "Capturing positive training images. Check positive training folder."
	print " "
	# Infinite loop, press Ctrl+c to interupt this 
	while True:
		image_number += 1
		print "Please look at the camera! Capturing image %s" % image_number 
		image = camera.read()
		# Convert image to grayscale using OpenCV libary
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image using
		# detect_single function. This will only work if there
		# is one face detected by the camera
		result = face.detect_single(image)

		# If no face was detected when the detect_single fucntion
		# was trying to find the coordinates of the image, this will
		# skip the image and just take another one
		if result is None:
			print "Could not detect single face!"
			print " " 
			continue

		# result uses the Haar algorithm used by OpenCV to detect objects.
		# x, y, represent the corners of the image and w, h are the width
		# and the height of the image
		x, y, w, h = result
		# This crops the image so that as much of the background is taken out
		# and that the only thing in focus is the face within the image
		crop = face.crop(image, x, y, w, h)
		# Save image to file within the positive folder
		filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + "%03d.pgm" % count)
		cv2.imwrite(filename, crop)
		print "Found face and wrote training image", filename
		print " " 
		# Increment the count variable by 1 each time an image is taken, ready for the next image
		count += 1
