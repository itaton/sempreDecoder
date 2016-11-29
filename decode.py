import struct
f = open("/tmp/rtl.dat", "rb")
#i = 0 #for debugging only
p = 0 #pause counter
wasHigh = 0 #set when signal was high
r = "" #the sent bit string
threshold = 1500 #needs to be set between high and low, depends on gain of sdr-stick
#samplemax = 0 #for debugging only
resultArray = [] #Stores the 12 packages that are send
try:
    s = f.read(1) #16 bits are one sample
    s += f.read(1)
    while s:
        sample = struct.unpack('<H', s)[0] #samples are in little endian

        #print(sample) #debugging
        #if (sample > samplemax and sample < 5000):
        #    samplemax = sample

        if (sample > threshold):
            #print(sample)
            wasHigh = 1
            if (p != 0):
                if (p >= 27 and p <= 31): #short pause -> 0
                    r = r + "0" 
                if (p >= 56 and p <= 62): #medium pause -> 1
                    r += "1"
                if (p > 100): #long pause -> transmission of one package ended. The package is send 12 times
                    resultArray.append(r)
                    r = ""
                #print(p)

            p = 0

        if (sample < threshold and (wasHigh == 1 or p != 0)):
            wasHigh = 0
            p += 1

        #i += 1
        s = f.read(1)
        s+= f.read(1)
finally:
    resultArray.append(r)

    #Check for transmission/decoding error - this assumes there is max 1 error in the first 3 transmissions
    if (resultArray[0] == resultArray[1]):
        #print(resultArray[0]) #resulting bitstring that was transmitted
        data = resultArray[0]
    else:
        #print(resultArray[2])
        data = resultArray[2]

    humidity = int(data[-8:], 2)
    print("Humidity:", humidity)
    temp = int(data[12:-12], 2)
    if (temp & 0x800 != 0):
        temp = ~temp
        temp = temp & 0xFFF
        temp += 1
        temp = temp/10.0
        print("Temperature:", "-" + str(temp))
    else:
        temp = temp/10.0
        print("Temperature:", temp)
    f.close()
