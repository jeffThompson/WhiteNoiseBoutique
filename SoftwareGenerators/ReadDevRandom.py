
'''
READ /DEV/RANDOM
Jeff Thompson | 2015 | www.jeffreythompson.org

'''

import os, struct

i = struct.unpack('<L', os.urandom(4))[0]
print i