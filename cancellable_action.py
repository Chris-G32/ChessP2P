import threading

class CancellableAction:
    def __init__(self):
        self.cancelled = threading.Event()
    def is_cancelled(self):
        return self.cancelled.is_set()
    def cancel(self):
        self.cancelled.set()
