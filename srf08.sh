#!/bin/bash
cd ~
while [ 1 = 1 ]
do
d=`i2cget -y 1 0x70 0x03`
f=`i2cget -y 1 0x70 0x02`
k=$(($f*$d+$d))

i2cset -y 1 0x70 0x00 0x51
sleep 0.06

i=`i2cget -y 1 0x70 0x02`
b=`i2cget -y 1 0x70 0x03`
c=$(($i*$b+$b))

l=$(($k-$c))
g=1
if [ "$l" -gt "$g"  ]
then
echo "motion detected, distance=" $c"sm"
else
 echo "..................."
fi


done


