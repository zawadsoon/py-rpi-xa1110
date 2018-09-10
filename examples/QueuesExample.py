import sys
import time
import queue
import threading

sys.path.append('../')

import pyxa1110

framesQueue = queue.Queue()
runEvent = threading.Event()
runEvent.set()

def fetchData ():
    with pyxa1110.GPS() as gps:
        while runEvent.is_set():
            gps.receiveData()
            framesQueue.put(gps.ascii())

def flushQueue ():
    while runEvent.is_set():
        time.sleep(0.5)
        try:
            item = framesQueue.get(False)
            if item is not None:
                print(item)
        except queue.Empty:
            pass


threads = []

#Thread that retreive data from GPS Device
t1 = threading.Thread(target = fetchData)
t1.start()
threads.append(t1)

#Thread that proceed data if available 
t2 = threading.Thread(target = flushQueue)
t2.start()
threads.append(t2)

try:
    while 1:
        time.sleep(.1)
except KeyboardInterrupt:
    print("\nClosing app...")
    runEvent.clear()
    framesQueue.task_done()
    for t in threads:
        t.join()
    print("App closed")

