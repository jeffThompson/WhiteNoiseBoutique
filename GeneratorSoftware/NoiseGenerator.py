
'''
NOISE GENERATOR
Jeff Thompson | 2015 | www.jeffreythompson.org

Interface for generating boutique white noise.

TODO
- email table with link to file as wav, txt, etc?
- web interface with Flask

PROCESS
(not many of these items can be skipped if specified)
1.  generate noise using either:
		1a. built-in RNG, or
		1b. input from hardware RNG
2.  save to file
3. 	create random salt or use user-specified
4.  hash file with salt
5.  make sure doesn't already exist and store hash
6.  ent tests
7.  dieharder tests
8.  write to audio file
9.  upload to server
10.  email link
11. securely delete file

Generously supported by a commission from Brighton Digital Festival.

'''

from Generators import *		# file with noise generating functions
from Tests import *				# file with RNG testing (ent, dieharder)
from AudioOutput import *
from UploadAndEmail import *
from Utilities import *			# file with misc functions (hashing, etc)
import uuid 					# for creating salt


# user-specified options
generator = 			'congruential'					# which to use?
email_address = 		'mail@jeffreythompson.org'		# needed to send download link
pre_chosen_salt = 		None 							# user-specified salt
salt_it = 				True							# randomly salt the noise?
email_salt = 			True
store_hash = 			True							# store the resulting hash?
upload_to_server = 		True							# upload noise for download?
delete_noise_file = 	True							# securely delete noise file when done?
noise_len = 			10 * 44100						# duration in sec * sample rate
seed = 					None							# seed value (or None) - doesn't work with all gens

# dieharder_tests = []
dieharder_tests = 		[ 1, 2, 101, 202, 203 ]

# files created and used
noise_byte_file = 		'bytes.dat'
noise_dieharder_file = 	'dieharder.dat'
all_hashes_file = 		'AllHashes.csv'		# file to store previous hashes

max_value = 			4294967295			# max value for 32-bit integer


# - - - - - - - - - - - - - - - - - - - -

print '\n' + 'WHITE NOISE GENERATOR'
print ('- ' * 8) + '\n'

print 'generating ' + str(noise_len/44100) + ' seconds of noise...'

# read from hardware RNG
if 'hardware:' in generator:
	generator = generator.replace('hardware:', '')
	print '- using hardware generator: ' + generator

# or, create noise using algo RNG and write to file
# by default, use dev/random since it is very secure
else:
	print '- using software generator: ' + generator
	if generator == 'threefish':
		noise = threefish(seed, noise_len)
	elif generator == 'aes_ofb':
		noise = aes_ofb(seed, noise_len)
	elif generator == 'congruential':
		noise = congruential(seed, noise_len)
	elif generator == 'dieharder:':
		generator = generator[10:]
		noise = dieharder_generator(seed, noise_len, generator)
	else:
		noise = dev_random(seed, noise_len)
	noise = convert_to_byte_range(noise, max_value)

# add generator to stats
stats = [ [ 'generator', generator, 'pseudo RNG' ] ]


print '- writing to file...'
write_byte_file(noise, noise_byte_file)
write_dieharder_file(noise, noise_dieharder_file, max_value)


# create salt as a "password" to the data
# or use user-specified salt if it exists
if pre_chosen_salt == None:
	salt = uuid.uuid4().hex
else:
	salt = pre_chosen_salt


# hash file as SHA512 for storage in list
# also create MD5 hash with salt created above for audio
# filename (since most OSs can't take filenames)
# longer than 128-256 characters
print '\n' + 'hashing file...'
if salt_it:
	sha512 = hash_file_sha512(noise_byte_file, salt)
else:
	sha512 = hash_file_sha512(noise_byte_file, None)

md5 = hash_file_md5(noise_byte_file, salt)


# check against previous hashes and store
if store_hash:
	print '- checking against previous hashes...'
	if check_against_hashes(sha512, all_hashes_file) == True:
		print '- already stored - redo generation!'
		exit(1)
	else:
		print '- not stored, adding to list...'
		with open(all_hashes_file, 'a') as out:
			out.write(sha512 + '\n')


# run tests on noise file
print '\n' + 'running ENT tests...'
stats.extend( ent_test(noise_byte_file) )


print '\n' + 'running DIEHARDER tests (may take a while)...'
for test in dieharder_tests:
	stats.extend( run_dieharder(noise_dieharder_file, test) )


# write wav file!
print '\n' + 'writing audio file...'
audio_filename = 'AudioFiles/' + md5 + '.wav'
write_wav(noise, audio_filename)


# upload to server
if upload_to_server:
	print '\n' + 'uploading audio file to server...'
	upload(audio_filename, 'noise/' + md5 + '.wav')


# email
print '\n' + 'sending email...'
if email_salt:
	send_email(email_address, 'http://www.whitenoiseboutique.com/noise/' + md5 + '.wav', stats, salt)
else:
	send_email(email_address, 'http://www.whitenoiseboutique.com/noise/' + md5 + '.wav', stats, None)


# delete noise file (we only keep the hash)
if delete_noise_file:
	print '\n' + 'securely deleting noise files...'
	check_call(['srm', noise_byte_file])
	check_call(['srm', noise_dieharder_file])


# all done!
print '\n' + 'DONE!' + '\n\n'

