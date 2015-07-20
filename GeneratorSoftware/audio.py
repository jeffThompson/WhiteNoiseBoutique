
import pyaudio, struct, math
from Utilities import *


rec_seconds = 		10
channels = 			1
sample_rate = 		44100
chunk_size = 		1024
bit_depth = 		pyaudio.paInt16


print 'recording audio...'
p = pyaudio.PyAudio()
stream = p.open(format=bit_depth, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
frames = []
for i in range(0, int(sample_rate / chunk_size * rec_seconds)):
	block = stream.read(chunk_size)
	# count = len(block)/2
	# shorts = struct.unpack('%dh' % count, block)
	# for short in shorts:
		# frames.append(short)
	frames.append(block)

print '- done recording'
print '- closing stream'
stream.stop_stream()
stream.close()
print '- shutting down audio connection'
p.terminate()


# remove any blank audio at start by chopping off first 2 sec
# frames = frames[ rate * 2000 : ]

# http://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic?rq=1
# http://people.csail.mit.edu/hubert/pyaudio/
for block in frames:
	# frames[i] = scale(frame, -32767,32767, 0,4294967295)
	sum_squares = 0.0
	count = len(block)/2
	shorts = struct.unpack('%dh' % count, block)
	for sample in shorts:
		n = sample * (1/32767.0)	# normalize
		sum_squares += n*n
	rms = math.sqrt(sum_squares / len(block)/2)
	print rms


# print frames
# print min(frames)
# print max(frames)







