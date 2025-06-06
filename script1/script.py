import time
import os

print('hello1', flush=True)
print(os.environ.get('ENV1', '???'), flush=True)

time.sleep(120)