cd /sys/class/gpio
echo 23 > export
cd /sys/class/gpio/gpio23
echo out > direction
echo 1 > value
