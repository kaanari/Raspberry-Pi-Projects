import RPi.GPIO as GPIO
import time


class Car:
    speed = 0
    color = "blue"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# qtr sensor pins
sensor1 = 5
sensor2 = 6
sensor3 = 13
sensor4 = 19
sensor5 = 26
sensor6 = 12
sensor7 = 16
sensor8 = 20
avgvalarray = [-30, -20, -10, 0, 0, 10, 20, 30] # Average Value Array

# Motor Pins
leftm_fwd = 17
leftm_bck = 27
left_en = 22
rightm_fwd = 23
rightm_bck = 24
right_en = 25
# Global variables
# PID Parameters
P_K = 18
I_K = 0
D_K = 6

error = 0
error_lst = 0

p = 0
i = 0
d = 0
t = 0
sensorsreal = [0, 0, 0, 0, 0, 0, 0, 0]
toplam = 0
yer = 45
yer_son = 45
sayac = 0
black_line = 0
white_line = 0
SPEED_MAX = 40
SPEED = 28
sum_weights = 1
sum_values = 1
sensors = []
# SETUP

GPIO.setup(leftm_fwd, GPIO.OUT)
GPIO.setup(leftm_bck, GPIO.OUT)
GPIO.setup(left_en, GPIO.OUT)
GPIO.setup(rightm_fwd, GPIO.OUT)
GPIO.setup(rightm_bck, GPIO.OUT)
GPIO.setup(right_en, GPIO.OUT)

GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)
GPIO.setup(sensor4, GPIO.IN)
GPIO.setup(sensor5, GPIO.IN)
GPIO.setup(sensor6, GPIO.IN)
GPIO.setup(sensor7, GPIO.IN)
GPIO.setup(sensor8, GPIO.IN)
time.sleep(50 / 1000.0)

left_pwm = GPIO.PWM(left_en, 100)
right_pwm = GPIO.PWM(right_en, 100)

def read_qtr():
    global sum_weights
    global sum_values
    global error
    global sensors
    sensors = []
    sum_weights = 0
    sum_values = 0
    sensors.append(int(not GPIO.input(sensor1)))
    sensors.append(int(not GPIO.input(sensor2)))
    sensors.append(int(not GPIO.input(sensor3)))
    sensors.append(int(not GPIO.input(sensor4)))
    sensors.append(int(not GPIO.input(sensor5)))
    sensors.append(int(not GPIO.input(sensor6)))
    sensors.append(int(not GPIO.input(sensor7)))
    sensors.append(int(not GPIO.input(sensor8)))
    for i in range(0, 8):
        sum_weights = sum_weights + sensors[i] * i * avgvalarray[i]
        sum_values = sum_values + sensors[i]
    try:
        error = sum_weights / sum_values
    except:
        error = 0

def pid_control():
    global t
    global SPEED
    global error_lst
    global i
    global SPEED_MAX
    
    if SPEED_MAX > SPEED: # Soft Start
        SPEED = SPEED + 1
    error_dif = error - error_lst
    error_lst = error
    p = P_K * error
    i = i + (I_K * error_dif)
    d = D_K * error_dif
    t = p + d
    t = t
    GPIO.output(rightm_fwd, GPIO.HIGH)
    GPIO.output(rightm_bck, GPIO.LOW)
    
    if t + SPEED > 100:
        right_pwm.start(100)
    elif SPEED + t < 0:
        right_pwm.start(0)
    else:
        right_pwm.start(SPEED + t)

    GPIO.output(leftm_fwd, GPIO.HIGH)
    GPIO.output(leftm_bck, GPIO.LOW)
    
    if SPEED - t > 100:
        left_pwm.start(100)
    elif SPEED - t < 0:
        left_pwm.start(0)
    else:
        left_pwm.start(SPEED - t)


def hard_right():
    GPIO.output(leftm_fwd, GPIO.HIGH)
    GPIO.output(leftm_bck, GPIO.LOW)
    GPIO.output(rightm_fwd, GPIO.LOW)
    GPIO.output(rightm_bck, GPIO.LOW)
    left_pwm.start(25)
    right_pwm.start(0)
    time.sleep(0.5)
    while not (sensors[3] == 1 and sensors[4] == 1 and sensors[2] == 0):
        read_qtr()
    GPIO.output(leftm_fwd, GPIO.LOW)
    GPIO.output(leftm_bck, GPIO.LOW)
    GPIO.output(rightm_fwd, GPIO.LOW)
    GPIO.output(rightm_bck, GPIO.LOW)
    left_pwm.start(0)
    right_pwm.start(0)


def hard_left():
    read_qtr()
    GPIO.output(leftm_fwd, GPIO.LOW)
    GPIO.output(leftm_bck, GPIO.LOW)
    GPIO.output(rightm_fwd, GPIO.HIGH)
    GPIO.output(rightm_bck, GPIO.LOW)
    left_pwm.start(0)
    right_pwm.start(25)
    time.sleep(0.2)
    while not (sensors[3] == 1 and sensors[4] == 1):
        read_qtr()
    GPIO.output(leftm_fwd, GPIO.LOW)
    GPIO.output(leftm_bck, GPIO.LOW)
    GPIO.output(rightm_fwd, GPIO.LOW)
    GPIO.output(rightm_bck, GPIO.LOW)
    left_pwm.start(0)
    right_pwm.start(0)


def handbrake():
    stateleftm_fwd = GPIO.input(leftm_fwd)
    stateleftm_bck = GPIO.input(leftm_bck)
    staterightm_fwd = GPIO.input(rightm_fwd)
    staterightm_bck = GPIO.input(rightm_bck)
    GPIO.output(leftm_fwd, int(not (stateleftm_fwd)))
    GPIO.output(leftm_bck, int(not (stateleftm_bck)))
    GPIO.output(rightm_fwd, int(not (staterightm_fwd)))
    GPIO.output(rightm_bck, int(not (staterightm_bck)))
    if SPEED + t > 100:
        left_pwm.start(100)
    elif SPEED + t < 0:
        left_pwm.start(0)
    else:
        left_pwm.start(SPEED + t)
    if SPEED - t > 100:
        right_pwm.start(100)
    elif SPEED - t < 0:
        right_pwm.start(0)
    else:
        right_pwm.start(SPEED - t)


def forward():
    GPIO.output(leftm_fwd, GPIO.HIGH)
    GPIO.output(leftm_bck, GPIO.LOW)
    GPIO.output(rightm_fwd, GPIO.HIGH)
    GPIO.output(rightm_bck, GPIO.LOW)
    left_pwm.start(20)
    right_pwm.start(20)


def stop():
    GPIO.output(leftm_fwd, GPIO.LOW)
    GPIO.output(leftm_bck, GPIO.LOW)
    GPIO.output(rightm_fwd, GPIO.LOW)
    GPIO.output(rightm_bck, GPIO.LOW)
    left_pwm.start(0)
    right_pwm.start(0)


def line_follow():
    global sensorsreal
    toplameski = 0
    read_qtr()
    if (sensors[0] == 0) and (sensors[7] == 0):
        pid_control()
    else:
        handbrake()
        time.sleep(0.02)
        stop()
        forward()
        count = 0
        toplam = sensors[0] + sensors[1] + sensors[2] + sensors[3] + sensors[4] + sensors[5] + sensors[6] + sensors[7]
        while toplam >= 3:
            read_qtr()
            toplam = sensors[0] + sensors[1] + sensors[2] + sensors[3] + sensors[4] + sensors[5] + sensors[6] + sensors[
                7]
            if toplam > toplameski:
                sensorsreal = sensors
            toplameski = sensorsreal[0] + sensorsreal[1] + sensorsreal[2] + sensorsreal[3] + sensorsreal[4] + \
                         sensorsreal[5] + sensorsreal[6] + sensorsreal[7]
        time.sleep(0.05)
        handbrake()
        stop()
        read_qtr()
        if sensorsreal[0] == 1 and sensorsreal[1] == 1 and sensorsreal[2] == 1 and sensorsreal[3] == 1 and sensorsreal[
            4] == 1 and sensorsreal[5] == 1 and sensorsreal[6] == 1 and sensorsreal[7] == 1:
            print("CROSSROADS")
            stop()
            for i in sensors:
                if i == 1:
                    count = 1
                    break
            if count == 1:
                choose = input("Where will I go? (L F R)")
                if (choose == 1):
                    hard_left()
                elif (choose == 2):
                    hard_right()
                elif (choose == 0):
                    forward()
                    time.sleep(0.1)
            else:
                choose = input("Where will I go? (L R)")
                if (choose == 1):
                    hard_left()
                elif (choose == 2):
                    hard_right()
                elif (choose == 0):
                    forward()
                    time.sleep(0.1)


        elif sensorsreal[0] == 1 and sensorsreal[1] == 1 and sensorsreal[2] == 1:
            stop()
            for i in sensors:
                if i == 1:
                    count = 1
                    break

            if count == 1:
                stop()
                choose = input("Where will I go? (F R)")
                if (choose == 2):
                    hard_right()
                elif (choose == 0):
                    forward()
                    time.sleep(0.1)

            else:
                handbrake()
                stop()
                time.sleep(1)
                hard_right()

        elif sensorsreal[7] == 1 and sensorsreal[6] == 1 and sensorsreal[5] == 1:
            stop()
            for i in sensors:
                if i == 1:
                    count = 1
                    break

            if count == 1:
                stop()
                choose = input("Where will I go? (L F)")
                if (choose == 1):
                    hard_left()
                elif (choose == 0):
                    forward()
                    time.sleep(0.1)

            else:
                handbrake()
                stop()
                hard_left()
                time.sleep(1)


while True:
    try:
        line_follow()
    except KeyboardInterrupt:
        GPIO.cleanup()
