
import hashlib, struct


def convert_to_byte_range(noise, max_value):
	for i, val in enumerate(noise):
		noise[i] = scale(val, 0, max_value, 0,256)
	return noise


def write_byte_file(noise, output_file):
	"""Write file as bytes for ent test."""
	byte_arr = bytearray(noise)
	out = open(output_file, 'wb')
	out.write(byte_arr)


def write_dieharder_file(noise, output_file, max_value):
	"""Write noise (passed as list) to file with appropriate header for dieharder."""
	header = {
		'version': 	'0.6',
		'count': 	str(len(noise)),
		'format': 	'decimal',
		'maximum': 	str(max_value),
		'minimum': 	'0'
	}
	with open(output_file, 'w') as out:
		out.write('[header]\n')

		for key in header.keys():
			out.write(key + '=' + header[key] + '\n')

		out.write('\n[data]\n')
		for val in noise:
			out.write(str(val) + '\n')


def hash_file_sha512(filename, salt):
	"""Return SHA512 hash from file's contents."""
	sha512 = hashlib.sha512()

	if salt != None:
		sha512.update(salt)

	with open(filename, 'rb') as f:
		for chunk in iter(lambda: f.read(128*sha512.block_size), b''):
			sha512.update(chunk)
	return sha512.hexdigest()


def hash_file_md5(filename, salt):
	"""Return MD5 hash from file's contents."""
	md5 = hashlib.md5()

	if salt != None:
		md5.update(salt)

	with open(filename, 'rb') as f:
		for chunk in iter(lambda: f.read(128*md5.block_size), b''):
			md5.update(chunk)
	return md5.hexdigest()


def check_against_hashes(sha512, all_hashes_file):
	"""Check if hash is already stored in list of hashes."""
	with open(all_hashes_file) as all_hashes:
		for hash in all_hashes:
			if sha512 == hash.strip():
				return True
		return False


def scale(input_value, in_low, in_high, out_low, out_high):
	"""Scale number from one range to another; same as 'map' command in Java."""
	return (((input_value - in_low) * (out_high - out_low)) / (in_high - in_low)) + out_low

