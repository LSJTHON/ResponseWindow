import board
import adafruit_dht
import RPi.GPIO as GPIO




def dht():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(17, GPIO.OUT)


    pwm=GPIO.PWM(17, 50)
    dhtDevice = adafruit_dht.DHT22(board.D18)

    try:
        temp = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humi = dhtDevice.humidity
        
    except RuntimeError as error:
        print(error.args[0])
    time.sleep(1)
        
return temp, humi
