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
import sys


from gpiozero import LED
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from gpiozero import MotionSensor



red_led = LED (17) # pin 17
green_led = LED (26) # pin 26
pir = MotionSensor(14) # 14 is the GPIO pin on the Pi


# This takes 5 photos when movement is detected by PIR
def motion_camera ():
	from picamera import PiCamera
	camera = PiCamera()
	print "--------------------------------------------------------------------------------"
	print "Photos are now being captured"
	print " "
	for i in range(5): # 5 is the number of photos being taken
		camera.capture("/home/pi/Desktop/image.jpg") # file path for image 
		print "Photo", i + 1 ,"has been taken" # i numbers the photos
		time.sleep(1) # wait 5 seconds before taking another photo
		
		send_attachment() # once photo has been taken, send to gmail account

		if i == 4:
			sys.exit()


# Once the photo has been taken, this sends the image to the gmail address               
def send_attachment():
    print "Email has been sent"
    print " "

    sender = ("sentrypi123@gmail.com") 
    receiver = ("pi.bloggs@gmail.com")

    message = MIMEMultipart()

    # This will appear in the header of the email
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = "AN INTRUDER HAS BEEN DETECTED!"

    # Text sent to email address
    body = ("Here is an image of the intruder") 
     
    message.attach(MIMEText(body, 'plain'))
     
    filename = ("image.jpg") # filename of the image defined in motion_camera function
    attachment = open("/home/pi/Desktop/image.jpg", "rb") # rb opens the binary file

    # This converts the attachment into Base64 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    message.attach(part)

    # Google server details 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() # this protects the password

    # Gives access to the gmail account
    server.login(sender, "$entry123")

    # This sends the message from the sender to the receiver
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


# This makes the red led flash 30 times when an intruder has been detected
def red_LED():
	for i in range(30):
		red_led.on()
		time.sleep(0.1)
		red_led.off()
		time.sleep(0.1)

		if i == 29:
			motion_camera()


# This tuens the green led on for 10 seconds when the valid driver
# has been detected
def green_LED():
	green_led.on()
	time.sleep(10)
	green_led.off()

	sys.exit()

# Once the valid driver has been detected, it will ask them for an
# username and password. If they get it right, the green led will turn on.
# If the wrong password is typed in 3 times, the red_LED function runs.

def password():
	password_attempts = 3
	print " "
	
	for i in range(3):
		
		password_attempts -= 1
		UserName = raw_input ("Enter Username: ")
		PassWord = raw_input ("Enter Password: ")

		if UserName == "damien_w145" and PassWord == "Sentinel":
			print "Login successful!"
			green_LED()
			break
		
		else:
			print "Password did not match!"
			if password_attempts == 1:
				print password_attempts, "attempt left"
				print " "
				
			else:
				print password_attempts, "attempts left"
				print " "

			# Once the user has had 3 attempts, run red_LED as if
			# they are an intruder
			if i == 2:
				print "Intruder Detected"
				red_LED()
	

if __name__ == "__main__":# Will check for motion detection
	for i in range(1):
		while True:
			if pir.motion_detected:
				print "Motion detected!"
				print" "
	    

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

						# If a face has not been detected for 5 times, run red_LED
						if i == 4:
							red_LED()
							
						continue # Can only be nested in a while or for loop

					
					
					x, y, w, h = result
					# Crop and resize image to face and remove all of the background
					crop = face.resize(face.crop(image, x, y, w, h))
					# Test face against model
					label, confidence = model.predict(crop)

					# If a positive match is found, green LED light is activated
					if label == config.POSITIVE_LABEL:
						print "Hi Damien, please insert valid credentials"

						# Ask the valid driver for a username and password
						password()
						break

					# If a negative face is detected, red LED light is activated and 5 images are taken
					# by camera. These 5 images are sent to gmail account
					else:
						print "Did not detect an authenticated driver"
						print " "

						# If a negative face has been detected for 5 times, run red_LED
						if i == 4:
							red_LED()
						
				
			
				
