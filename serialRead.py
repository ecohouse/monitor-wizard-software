import serial
import time
import datetime
import RPi.GPIO as RPIO
from subprocess import call

#once the Pi detects an edge, it reads from the Pi TODO: instead: send a signal, inside the recv() function of the
#Arduino there will be code waiting for this signal from the serial line, only when it is received will the
#data be sent using pySerial.
#this should be immune from noise: since the response is only inside the recv() function in the Arduino loop
#if there is a spurious signal, then there will be nothing sent

increment = 0.392
lowerTempLimit = -40.0
packetLen = 49
ser = serial.Serial('/dev/ttyACM2', 9600,)

def decodeTemp(t):
	return float(t) * increment + lowerTempLimit

def decodeHumidity(h):
	return float(h) *  increment

def readFromSerial(channel):
	#print ('callback')
	recv = ser.read(4)
	print recv
	if (recv == "SEND"):
		arr = fillArray()
		writeFile(arr)
		ser.flushInput()
	else:
		ser.flushInput()
	#print('finished')

def fillArray():
	a = [0]*packetLen
	
	for x in range(0, packetLen):
		s = ser.read()
		try:
			a[x] = ord(s)
		except TypeError:
			continue
	return a

def writeFile(a):
	#in future try and deduce which node the data is coming from
	with  open('dataFile.txt', 'a') as f:
	
	#note: this timestamp is in fact the start of the NEXT packet of data
		time_stamp = time.time()
		date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M')
		f.write(str(date_stamp) + "\t")
	
		for x in range(0, len(a)):
			if (x % 2 == 0):
				temp = "{0:.1f}".format(decodeTemp(a[x])) 
				f.write(temp + "\t")
			else:
				humidity = "{0:.1f}".format(decodeHumidity(a[x])) 
				f.write(humidity + "\t")
		f.write("\n")
		f.close()

def main():
	RPIO.setmode(RPIO.BCM)
	RPIO.setup(4, RPIO.IN, pull_up_down = RPIO.PUD_DOWN )
	RPIO.add_event_detect(4, RPIO.RISING, callback = readFromSerial)
	
	while True:
		try:
			time.sleep(180) 
			dataFile =  "../../Dropbox-uploader/dropbox_uploader.sh upload dataFile.txt MonitorWizardResults.txt"
			call ([dataFile], shell = True)  				
		except  KeyboardInterrupt:
			RPIO.cleanup()

if __name__ == "__main__":
	main()
		
	#while True:
		#sleep until 1AM each day and then upload the textfile
		#t = datetime.datetime.today()
		#future = datetime.datetime(t.year, t.month, t.day, 1.0)
		
		#if t.hour >= 1:
		#	#TODO: upload the data
		#	 
		#	call (dataFile, shell = True)
		#	future += datetime.timedelta(days = 1)
		#GPIO.cleanup()	
		#
		#time.sleep((future-t).second)


			
	
	





