import time
import threading

total = 0

def print_me(message):
    global total
    
    for i in range(30):
        print message, total
        total += 1
        time.sleep(1)


# create two threads
t1 = threading.Thread(target=print_me, args=('hello from thread 1',))
t2 = threading.Thread(target=print_me, args=('hello from thread 2',))

# run 'em
t1.start()
t2.start()

# wait for 'em to finish.
t1.join()
t2.join()
