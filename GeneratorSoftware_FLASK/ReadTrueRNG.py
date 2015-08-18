
import serial, sys, glob


def list_ports():
	ports = []
	if sys.platform.startswith('win'):
		ports = [ 'COM' + str(i+1) for i in range(256) ]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	return ports

ports = list_ports()
yield ports


ser = serial.Serial(port=ports[2], baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

for i in range(10):
	yield ser.read(8)

ser.close()

