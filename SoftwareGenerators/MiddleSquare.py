
'''
MIDDLE SQUARE
Jeff Thompson | 2015 | www.jeffreythompson.org

'''

seed = 13243546576879800897867564534231

n = seed
index = 0
already_seen = set()
while n not in already_seen:
	already_seen.add(n)
	n = str(n * n).zfill(8)[2:6]
	print str(index) + ': ' + str(n)
	n = int(n)
	index += 1

print '\n[ reached never-ending loop, quit ]\n\n'