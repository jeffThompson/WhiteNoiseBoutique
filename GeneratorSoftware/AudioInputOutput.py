
import wave								# for all things audio
from struct import pack, unpack			# numbers from raw samples
from Utilities import *					# formatting audio data
from subprocess import check_call		# for secure delete


def read_from_audio_file(input_filename, noise_len):
	"""Reads noise values from audio file."""
	w = wave.open(input_filename, 'r')
	num_samples = w.getnframes()

	# file too short? quit
	if num_samples < noise_len:
		print '- audio file is too short!'
		print '\n QUITTING...'
		exit()

	# read samples
	print '- reading samples from file...'
	noise = []
	for i in range(0, noise_len):
		sample = w.readframes(1)
		sample = int(struct.unpack('<h', sample)[0])
		sample = (sample + 32768) * 65535			# convert 16-bit signed to expected range
		noise.append(sample)

	# securely delete file
	print '- securely deleting input file...'
	check_call([ 'srm', input_filename ])

	# done!
	return noise



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

