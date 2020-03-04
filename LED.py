from gpiozero import LED
import time

red_led = LED (21) # pin 21
green_led = LED (20) # pin 20

def red_LED(self):
    for i in range(5):
        # Red LED
        red_led.on()
        time.sleep(0.1)
        red_led.off()
        time.sleep(0.1)
    

def green_LED(self):
    # Green LED
    green_led.on()
    time.sleep(1)
    
  
   
