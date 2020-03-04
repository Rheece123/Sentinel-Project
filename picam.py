# This script creates the Pi camera capture class for OpenCV. This class capture a single image
# from the pi camera and saves the image as an OpenCV image.

import io
import time
import cv2
import numpy as np
import picamera
import config


class OpenCVCapture(object):
        
	def read(self):
		# This fucntion reads a single frame from the camera and
		# return the data as an OpenCV image
		
		# Capture a frame from the camera and save it as bytes
		data = io.BytesIO()
		with picamera.PiCamera() as camera:
			camera.capture(data, format='jpeg')
		data = np.fromstring(data.getvalue(), dtype=np.uint8)
		# Decode the image data and return an OpenCV image
		image = cv2.imdecode(data, 1)
		# Save captured image for debugging. Useful if the picamera
		# constantly takes invalid images 
		cv2.imwrite(config.DEBUG_IMAGE, image)
		# Return the captured image data for debugging purposes
		return image
