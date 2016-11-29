timeout 55 rtl_fm -M am -f 434.0M -s 30k -g 50 > /tmp/rtl.dat
python ./decode.py
rm /tmp/rtl.dat
