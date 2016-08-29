import time
import Adafruit_BBIO.GPIO as GPIO
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("senlib_module")

def xband(gpio_pins, out_raw_data, exp_parameter):
    periods = []
    temp = []
    for i in range(2): temp.append([])
    raw_data = []
    for i in range(2): raw_data.append([])

    t_time = 0
    slide_window = []
    st_dev = 0
    mean_vol = 0
    logger.info('X-Band started')
    startTime = time.time()

    while t_time < exp_parameter['duration']:
        check = GPIO.input(gpio_pins['signal_pin'])
        t_time = time.time() - startTime
        raw_data[0].append(t_time)
        raw_data[1].append(check)

        # frequency transformation
        temp[0].append(check)
        temp[1].append(t_time)
        if len(temp[0]) > 1 and temp[0][-1] > temp[0][-2]:
            periods.append(temp[1][-2])
            if len(periods) > 1:
                freq = 1 / (periods[-1] - periods[-2])
                slide_window.append(freq)
                if len(slide_window) > 3:
                    slide_window = []
                if len(slide_window) == 3:
                    st_dev = np.std(slide_window)  # standard deviation
                    mean_vol = np.mean(slide_window)

                # if mean_vol > exp_parameter['fr_level'] and st_dev <  exp_parameter['std_level']:
                # GPIO.output(gpio_pins['LED_pin'], GPIO.HIGH)
                # else:
                # GPIO.output(gpio_pins['LED_pin'], GPIO.LOW)
                del periods[0]
            del temp[0][:-1]
            del temp[1][:-1]
        time.sleep(0.001)
    logger.info('X-Band finished')
    out_raw_data.put(raw_data)


def pir(gpio_pins, out_detect_signal, exp_parameter, name):
    t_time = 0
    detect_signal = []
    for i in range(2): detect_signal.append([])
    logger.info(name + ' started')

    startTime = time.time()
    while t_time < exp_parameter['duration']:
        check = GPIO.input(gpio_pins['signal_pin'])
        t_time = time.time() - startTime
        detect_signal[0].append(t_time)
        detect_signal[1].append(check)
        time.sleep(0.1)
    logger.info(name + ' finished')
    out_detect_signal.put(detect_signal)