
import wave
from struct import pack
from Utilities import *


def write_wav(samples, output_filename):
	"""
	Write a mono wav file from a list of sample values.

	Based on this example:
	http://blog.philippklaus.de/2014/07/generating-sound-with-python/
	"""

	num_channels = 	1				# 1 = mono, 2 = stereo
	sample_width = 	2				# size of sample in bytes (16-bit audio = 2)
	frame_rate = 	44100			# aka sample rate
	num_frames = 	len(samples)	# duration of file in samples
	buffer_size = 	2048

	# create file
	print '- creating wav file...'
	w = wave.open(output_filename, 'w')
	w.setparams((num_channels, sample_width, frame_rate, num_frames, 'NONE', 'not compressed'))

	# convert from byte to integer in range -32767 to 32767 in proper format
	print '- formatting samples...'
	output_samples = b''
	for sample in samples:
		sample = int(scale(sample, 0,256, -32767, 32767))
		output_samples += pack('h', sample)

	# and save to file
	print '- writing samples to file...'
	w.writeframes(output_samples)
	w.close()

