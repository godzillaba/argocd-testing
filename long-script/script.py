import time
import os
import sys

print('hello1')
print(os.environ.get('ENV1', '???'))
print(os.environ.get('SECRET', '???'))
print(sys.argv)
print(flush=True)

time.sleep(1000000)