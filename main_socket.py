#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import threading
import Queue
import sys
import socket
import senlib
#import logging


# 0 - out pin     1 - LED pin
xBandPins = {'signal_pin': 'P8_12', 'LED_pin': 'P8_11'}
# pir1Pins = {'signal_pin' : 'P8_14', 'LED_pin' : 'P8_13' }
pir1Pins = {'signal_pin': 'P8_15', 'LED_pin': 'P8_13'}
pir2Pins = {'signal_pin': 'P8_17', 'source_pin': 'P8_18'}

print 'Program starting...'

GPIO.setup(xBandPins['signal_pin'], GPIO.IN)
# GPIO.setup(xBandPins['LED_pin'], GPIO.OUT)
GPIO.setup(pir1Pins['signal_pin'], GPIO.IN)
# GPIO.setup(pirPins['LED_pin'], GPIO.OUT)
GPIO.setup(pir2Pins['signal_pin'], GPIO.IN)
GPIO.setup(pir2Pins['source_pin'], GPIO.OUT)
GPIO.output(pir2Pins['source_pin'], GPIO.HIGH)

xBand_raw_data_queue = Queue.Queue()
pir1_detect_signal_queue = Queue.Queue()
pir2_detect_signal_queue = Queue.Queue()

# socket part
# *******************
HOST = ''
PORT = 5566

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

while True:
    s.listen(10)
    print 'Socket now listening'
    conn, addr = s.accept()
    # now keep talking with the client
    data = conn.recv(64)
    print data
    # *******************
    args = data.split()

    if len(args) < 4:
        exp_parameter = {'number': 'test', 'duration': 30, 'fr_level': 20, 'std_level': 15}
        print '______________________________________________'
        print "parameters are set by default:%snumber - %s%stime duration = %i s%sfr_level = %i%sstd_level = %i%s" % (
            '\n', exp_parameter['number'], '\n', exp_parameter['duration'], '\n', exp_parameter['fr_level'], '\n',
            exp_parameter['std_level'], '\n')
    else:
        exp_parameter = {'duration': int(args[0]), 'fr_level': int(args[1]),
                         'std_level': int(args[2]), 'number': str(args[3])}
        print '______________________________________________'
        print "parameters are set manually:%snumber - %s%stime duration = %i s%sfr_level = %i%sstd_level = %i%s" % \
              ('\n', exp_parameter['number'], '\n', exp_parameter['duration'], '\n', exp_parameter['fr_level'], '\n',
               exp_parameter['std_level'], '\n')

    print 'Program starting...'

    xBandThread = threading.Thread(target=senlib.xband, args=(xBandPins, xBand_raw_data_queue, exp_parameter))
    pir1Thread = threading.Thread(target=senlib.pir, args=(pir1Pins, pir1_detect_signal_queue, exp_parameter, 'pir1'))
    pir2Thread = threading.Thread(target=senlib.pir, args=(pir2Pins, pir2_detect_signal_queue, exp_parameter, 'pir2'))

    xBandThread.start()
    pir1Thread.start()
    pir2Thread.start()

    xBandThread.join()
    pir1Thread.join()
    pir2Thread.join()
    conn.close()

    print "socket closed"

    xBand_raw_data = xBand_raw_data_queue.get()
    pir1_detect_signal = pir1_detect_signal_queue.get()
    pir2_detect_signal = pir2_detect_signal_queue.get()

    file = open("/root/ex_data/plot_data_%s.data" %(exp_parameter['number']), "w")
    file.write("exp_parameter" + '\n')
    sym = ' '
    file.write \
        (str(exp_parameter['duration']) + sym + str(exp_parameter['fr_level']) + sym + str(
            exp_parameter['std_level']) + '\n')
    file.write("/end_of_exp_parameter" + '\n')

    file.write("row_data" + '\n')
    sym = ' '
    for index in range(len(xBand_raw_data[0])): file.write \
        (str(xBand_raw_data[0][index]) + sym + str(xBand_raw_data[1][index]) + "\n")
    file.write("/end_of_row_data" + '\n')

    file.write("pir1_detect_signal" + '\n')
    for index in range(len(pir1_detect_signal[0])):
        file.write(str(pir1_detect_signal[0][index]) + sym + str(pir1_detect_signal[1][index]) + "\n")
    file.write("/end_of_pir1_detect_signal" + '\n')

    file.write("pir2_detect_signal" + '\n')
    for index in range(len(pir2_detect_signal[0])):
        file.write(str(pir2_detect_signal[0][index]) + sym + str(pir2_detect_signal[1][index]) + "\n")
    file.write("/end_of_pir2_detect_signal" + '\n')
    file.close()

s.close()
