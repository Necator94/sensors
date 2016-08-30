#!/usr/bin/env python
# Arguments to recieve by socket:
# 0 - experiment duration;
# 1 - frequency estimation criteria
# 2 - standard deviation criteria
# 3 - number of an experiment;
import Adafruit_BBIO.GPIO as GPIO
import threading
import Queue
import sys
import socket
import sen_lib_module
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main_app")

# 0 - out pin     1 - LED pin
xBandPins = {'signal_pin': 'P8_12', 'LED_pin': 'P8_11'}
pir1Pins = {'signal_pin': 'P8_15', 'LED_pin': 'P8_13'}
pir2Pins = {'signal_pin': 'P8_17', 'source_pin': 'P8_18'}

logger.info('Program start')

GPIO.setup(xBandPins['signal_pin'], GPIO.IN)
GPIO.setup(pir1Pins['signal_pin'], GPIO.IN)
GPIO.setup(pir2Pins['signal_pin'], GPIO.IN)
GPIO.setup(pir2Pins['source_pin'], GPIO.OUT)
GPIO.output(pir2Pins['source_pin'], GPIO.HIGH)

xBand_raw_data_queue = Queue.Queue()
pir1_detect_signal_queue = Queue.Queue()
pir2_detect_signal_queue = Queue.Queue()

# socket part**********************************************************************
HOST = ''
PORT = 5566
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.info('Socket created')
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    logger.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
while True:
    s.listen(10)
    logger.info('Socket now listening')
    conn, addr = s.accept()
    data = conn.recv(64)
# **********************************************************************************
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

    logger.info('Experiment start')

    xBandThread = threading.Thread(target=sen_lib_module.xband, args=(xBandPins, xBand_raw_data_queue, exp_parameter))
    pir1Thread = threading.Thread(target=sen_lib_module.pir, args=(pir1Pins, pir1_detect_signal_queue, exp_parameter, 'pir1'))
    pir2Thread = threading.Thread(target=sen_lib_module.pir, args=(pir2Pins, pir2_detect_signal_queue, exp_parameter, 'pir2'))
    xBandThread.start()
    pir1Thread.start()
    pir2Thread.start()
    xBandThread.join()
    pir1Thread.join()
    pir2Thread.join()

    conn.close()
    logger.info('Socket closed')

    xBand_raw_data = xBand_raw_data_queue.get()
    pir1_detect_signal = pir1_detect_signal_queue.get()
    pir2_detect_signal = pir2_detect_signal_queue.get()

# results writing into 'args[3].data' file
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
