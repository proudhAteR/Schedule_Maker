import sys
import threading
import time
from contextlib import contextmanager


class Loader:
    def __init__(self, speed=0.05):
        self._speed = speed
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self._spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠏', '⠇']
        self._frames = [f'\r{c}' for c in self._spinner]

    def _spin(self):
        i = 0
        while self._running:
            with self._lock:
                sys.stdout.write(f'\r{self._spinner[i]}')
                sys.stdout.flush()
            i = (i + 1) % len(self._spinner)
            time.sleep(self._speed)
        # Clear spinner
        with self._lock:
            self._clear_spinner()

    def _clear_spinner(self):
        max_len = max(len(f) for f in self._frames)
        sys.stdout.write('\r' + ' ' * max_len + '\r')
        sys.stdout.flush()

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._thread.join()

    @classmethod
    @contextmanager
    def run(cls, speed=0.05):
        loader = cls(speed)
        loader.start()
        try:
            yield loader
        finally:
            loader.stop()
