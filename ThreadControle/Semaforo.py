import threading
import time


class Semaforo:
    def __init__(self):
        self.mutex = threading.Semaphore(4)

    def acquire(self):
        time.sleep(0.5)
        self.mutex.acquire()

    def release(self):
        self.mutex.release()
