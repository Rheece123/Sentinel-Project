# The main purpose of this script is to help with the detection and cropping of faces.
# The first thing which happens is that the Viola-Jones object detection framework
# (used by Haar in OpenCV) detects object classes (facial features) in the image.
# The detect_single fucntion runs next and this is responsible for returning the
# x, y (upper corner) coordinates and the width, height of the image. This image
# is then cropped to the same size as the training image. 


import cv2
import config


# Haar is the algorithm used by OpenCV to detect objects.
# This variable is provided by OpenCV under the Haar section
haar_faces = cv2.CascadeClassifier(config.HAAR_FACES)


def detect_single(image):
	# This function returns the x, y, width, height coordinates of the detected face
        # found within the grayscale image
	faces = haar_faces.detectMultiScale(image, scaleFactor=config.HAAR_SCALE_FACTOR, 
		minNeighbors=config.HAAR_MIN_NEIGHBORS, minSize=config.HAAR_MIN_SIZE, 
		flags=cv2.CASCADE_SCALE_IMAGE)

	# If no face is detected, no coordinates are returned
	if len(faces) != 1:
		return None
	return faces[0]


def crop(image, x, y, w, h):
	# This crops the image taken on camera to the same size as the training images	
	crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
	midy = y + h/2
	y1 = max(0, midy-crop_height/2)
	y2 = min(image.shape[0]-1, midy+crop_height/2)
	return image[y1:y2, x:x+w]


def resize(image):
	# Resize a face image to the proper size for training and detection
	return cv2.resize(image,(config.FACE_WIDTH, config.FACE_HEIGHT),
                          interpolation=cv2.INTER_LANCZOS4)
