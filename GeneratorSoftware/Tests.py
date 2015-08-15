
'''
TESTS RUN 							WHERE
frequency (monobits)*				ENT
mean 								ENT
serial correlation*					ENT
entropy*							ENT
chi-squared							ENT
monte carlo pi 						ENT
OPERM5*								Dieharder 1
32x32 binary matrix*				Dieharder 2
STS runs*							Dieharder 101
RGB permutations*					Dieharder 202
RGB lagged sums*					Dieharder 203

CONSIDER
RGB Kolmogorov-Smirnov				Dieharder 204
Craps								Dieharder 16

* = required to pass NIST guidelines, details of which are here:
http://csrc.nist.gov/groups/ST/toolkit/rng/stats_tests.html

'''


from subprocess import check_call, Popen, PIPE
import re, math

label_padding = 25
value_padding = 15


def pad(s, l):
	"""
	Format text as a padded table entry.

	Args:
	s = value to pad (#s converted to string)
	l = length of padding
	"""
	s = str(s)
	if l < len(s):
		return s
	return s + ('&nbsp;' * (l-len(s)))


def ent_test(input_file):
	"""Run ENT test on a series of random numbers, returns a dict of stats.

	TESTS:
	- entropy				100% = complete entropy
	- chi-square 			99-100/0-1 = not at all random, 95-99/1-5% = suspect, 50% = random
	- mean 					0.5 = completely random
	- monte carlo pi 		how close value is to pi at specified precision
	- serial correlation 	totally uncorrelated = 0, 0.5 = non-random, completely predictable = 1

	Values for passing via this Reddit thread:
	https://www.reddit.com/r/crypto/comments/3drlgl/what_values_constitute_passing_for_ent_tests/

	More info via:
	http://www.fourmilab.ch/random/
	"""

	command = [ 'ent', input_file ]
	p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	result, err = p.communicate()

	print result

	entropy = (float(re.findall('Entropy = (.*?) bits', result)[0]) / 8) * 100.0
	total_samples = int(re.findall('distribution for (.*?) samples', result)[0])
	chi_square = float(re.findall('would exceed this value( less than)? (.*?) percent', result)[1])
	mean = float(re.findall('value of data bytes is (.*?) \(', result)[0])
	monte_carlo_pi = float(re.findall('error (.*?) percent', result)[0])
	serial_correlation = abs(float(re.findall('correlation coefficient is (.*?) \(', result)[0]))

	stats = []
	printable_stats = ''

	printable_stats += pad('- entropy (100%)', label_padding) +  pad(str(entropy) + '%', value_padding)
	if entropy > 90:
		printable_stats += 'PASSED\n'
		stats.append(['entropy', entropy, 'PASSED' ])
	else:
		printable_stats += 'FAILED\n'
		stats.append(['entropy', entropy, 'FAILED' ])

	printable_stats += pad('- chi-square (50%)', label_padding) +  pad(str(chi_square) + '%', value_padding)
	if chi_square > 99 or chi_square < 1:
		printable_stats += 'FAIL\n'
		stats.append(['chi-square', chi_square, 'FAILED' ])
	elif chi_square > 95 or chi_square < 5:
		printable_stats += 'SUSPECT\n'
		stats.append(['chi-square', chi_square, 'SUSPECT' ])
	elif chi_square > 90 or chi_square < 10:
		printable_stats += 'ALMOST SUSPECT\n'
		stats.append(['chi-square', chi_square, 'ALMOST SUSPECT' ])
	else:
		printable_stats += 'PASSED\n'
		stats.append(['chi-square', chi_square, 'PASSED' ])

	printable_stats += pad('- arith mean (127.5)', label_padding) +  pad(mean, value_padding)
	if mean > 114.25 and mean < 140.75:
		printable_stats += 'PASSED\n'
		stats.append(['mean', mean, 'PASSED' ])
	else:
		printable_stats += 'FAILED\n'
		stats.append(['mean', mean, 'FAILED' ])

	printable_stats += pad('- monte-carlo pi (0%)', label_padding) +  pad(str(monte_carlo_pi) + '%', value_padding)
	if monte_carlo_pi < 2.0:
		printable_stats += 'PASSED\n'
		stats.append(['monte_carlo_pi', monte_carlo_pi, 'PASSED' ])
	else:
		printable_stats += 'FAILED\n'
		stats.append(['monte_carlo_pi', monte_carlo_pi, 'FAILED' ])

	# test values via:
	# https://www.reddit.com/r/crypto/comments/3drlgl/what_values_constitute_passing_for_ent_tests/ct8xry7
	printable_stats += pad('- serial correl (0)', label_padding) +  pad(serial_correlation, value_padding)
	n = total_samples
	m = -1.0 / (n-1)
	s = math.sqrt((n*n - 3*n)/(n+1)) / (n-1)
	if serial_correlation > m-2*s and serial_correlation < m+2*s:
		printable_stats += 'PASSED\n'
		stats.append(['serial_correlation', serial_correlation, 'PASSED' ])
	else:
		printable_stats += 'FAILED\n'
		stats.append(['serial_correlation', serial_correlation, 'FAILED' ])

	# done, return stats
	return stats, printable_stats


def run_dieharder(noise_file, test):
	"""Run DIEHARDER tests on a series of random numbers, returns a dict of stats.

	More info via:
	http://manpages.ubuntu.com/manpages/vivid/man1/dieharder.1.html
	"""

	stats = []
	printable_stats = ''

	command = [ 'dieharder', '-d', str(test), '-f', noise_file ]
	p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	result, err = p.communicate()

	result = result.split('\n')[8:]
	for r in result:

		# only read valid data (ignore lines with #, for example)
		if not any(x in r for x in ['PASSED', 'WEAK', 'FAILED', '#']):
			continue

		r = r.split('|')
		test = r[0].replace('_', ' ')			# format test name nicely
		test = test.replace('diehard', '')		# remove unecessary info
		test = test.strip()
		value = r[4].strip()
		passing = r[5].strip()

		stats.append( [test, value, passing ] )

		printable_stats += pad('- ' + test, label_padding) + pad(value, value_padding) + passing + '\n'

	# done, return stats
	return stats, printable_stats

