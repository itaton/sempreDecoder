timeout 60 rtl_fm -M am -f 434.0M -s 30k -g 25 > /tmp/rtl.dat
python ./decode.py
rm /tmp/rtl.dat
