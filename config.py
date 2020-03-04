# This script is responsible for setting the threshold for the positive image which
# will be compared when taking images of potential intruders. It loads the training
# data from the training.xml file which holds all of the data for the positive face model
# compared to the negative face model. The labels are created for the positive and
# negative images and these are compared during the main script. When the main script
# runs, a image is saved for debugging purposes incase the camera is repeatidly not
# detecting a face within the image.

# File to save and load face recognizer model. Uses xml file to compare the positive
# and negative face models
TRAINING_FILE = 'training.xml'

# Directories which contain the positive and negative training images
POSITIVE_DIR = './training/positive'
NEGATIVE_DIR = './training/negative'

# Value for positive and negative labels passed to face recognition model. These are used
# to print if the detected face is a positive or negative match
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2

# Size (in pixels) to resize images for training and prediction. This removes most of the background
# in the image. Suitable size to detect all of Damien's facial features
FACE_WIDTH  = 92
FACE_HEIGHT = 112

# Face detection cascade classifier configuration for the Haar algorithm
# See: http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html
HAAR_FACES         = 'haarcascade_frontalface_alt.xml'
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)

# Filename to use when saving the most recently captured image for debugging purposes if the Picamera
# is constantly not detecting a face within the image. This is saved within the root of the folder
DEBUG_IMAGE = 'capture.pgm'


# This function imports the Picamera module and uses the OpenCVCapture() in the picam function
# to read the image taken on the Raspberry Pi camera as an OpenCV image file
def get_camera():	
	import picam
	return picam.OpenCVCapture()
