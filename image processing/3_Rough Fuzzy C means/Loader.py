import sys
import time
import threading


resetStyle = "\033[0m"
class Loader:
    _stack = []
    _lock =  threading.Lock()
    def __init__(self, message: str = 'Loading', font:list|None = None):
        self.message  = message
        self.running  = False
        self._thread  = None
        if(font == None):
            self.fontStyle = "\033[1;36m"
        else:
            self.fontStyle = "\033["+";".join(font) + "m"

    def _is_top(self):
        with Loader._lock:
            return Loader._stack  and Loader._stack[-1] is self
        
    def _spin(self):
        frames = ['/', '-', '\\', '|']
        idx = 0
        while self.running:
            if self._is_top():
                sys.stdout.write(f'\r{self.fontStyle}{self.message}...{resetStyle}{frames[idx % 4]}')
                sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

    def start(self):
        self.running = True
        with Loader._lock:
            Loader._stack.append(self)
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, end_message: str = 'Done'):
        self.running = False
        with Loader._lock:
            if self in Loader._stack:
                Loader._stack.remove(self)
        if self._thread:
            self._thread.join()
        sys.stdout.write(f'\r{self.fontStyle}{self.message}... {resetStyle}{end_message}\n')
        sys.stdout.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()