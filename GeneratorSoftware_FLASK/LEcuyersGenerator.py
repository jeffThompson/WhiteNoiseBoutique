
def lecuyers_generator(idum):
	"""Returns random value using the L'Ecuyer's generator
	with Bays-Durham shuffle; returns values 0-1.

	A PRNG with a very long period*, which combines two
	pseudo-random sequences with different periods to create
	a new sequence. Or, as quoted in an implementation of
	this algorithm: "For present computers, period exhaustion
	is a practical impossibility." This method also reduces
	the serial correlation.

	* The actual period is at least 2*10^18

	The Bays-Durham shuffle mixes up the sequence to remove
	low-order serial correlation further.

	This implementation via a statistical analysis of the
	LavaRand generator (which uses... lava lamps).
	"""

	# constants
	IM1 = 	2147483563
	IM2 = 	2147483399
	AM = 	1.0/IM1
	IMM1 = 	IM1-1
	IA1 = 	40014
	IA2 = 	40692
	IQ1 = 	53668
	IQ2 = 	52774
	IR1 = 	12211
	IR2 = 	3791
	NTAB = 	32
	NDIV = 	(1 + IMM1/NTAB)
	EPS = 	1.2e-7
	RNMX = 	1.0 - EPS

	idum2 =	123456789
	iy = 	0
	iv = 	[NTAB]

	# initialize, prevents idum == 0
	if idum <= 0:
		if -(idum) < 1:
			idum = 1
		else:
			idum = -(idum)
		idum2 = idum

		# load shuffle table
		for j in reversed(xrange(NTAB+7)):
			k = idum / IQ1
			idum = IA1 * (idum-k * IQ1) - k * IR1
			if idum < 0:
				idum += IM1
			if j < NTAB:
				iv[j] = idum
		iy = iv[0]

	# generate
	k = idum / IQ1
	idum = IA1 * (idum-k * IQ1) - k * IR1
	if idum < 0:
		idum += IM1
	k = idum2 / IQ2
	idum2 = IA2 * (idum2-k * IQ2) - k * IR2
	if idum2 < 0:
		idum2 += IM2
	j = iy / NDIV

	# shuffle and combine
	iy = iv[j] - idum2
	iv[j] = idum
	if iy < 1:
		iy += IMM1

	temp = AM * iy
	if temp > RNMX:
		return RNMX
	return temp



seed = 1
for i in range(10):
	print seed
	seed = lecuyers_generator(seed)


























