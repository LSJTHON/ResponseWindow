import RPi.GPIO as GPIO # 라즈베리파이 GPIO 핀을 쓰기위해 임포트
import time # 시간 간격으로 제어하기 위해 임포트
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # 핀의 번호를 보드 기준으로 설정, BCM은 GPIO 번호로 호출함
GPIO.setup(pin, GPIO.OUT)
pwm=GPIO.PWM(17, 50)

def motor(openclose):
    if openclose == "open":
        result2 = "열림"
        pwm.start(2.5)
        pwm.stop() 
        GPIO.cleanup(17)
        return result2
    elif openclose == "close":
        result2 = "닫힘"
        pwm.start(6)
        pwm.stop() 
        GPIO.cleanup(17)
        return result2



