import time
import os

total = 0

def print_me(message):
    global total
    
    for i in range(30):
        print message, total
        total += 1
        time.sleep(1)


name = 'process 1'
if os.fork() == 0:
    name = 'process 2'
    
print_me('hello from %s' % name)

if name == 'process 1':
    os.wait()
