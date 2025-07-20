import os
import sys
import time
from functools import wraps

from Infrastructure.Utils.Logs.Logger import Logger


class PerformanceTracker:
    @staticmethod
    def _is_debugging():
        if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
            return True

        ide_vars = [
            'PYCHARM_HOSTED',
            'PYDEVD_LOAD_VALUES_ASYNC',
            'VSCODE_PID'
        ]

        return any(var in os.environ for var in ide_vars)

    @staticmethod
    def timeit(threshold: float = 0.5):
        def decorator(func):
            # If not debugging, return original function (no timing overhead)
            if not PerformanceTracker._is_debugging():
                return func

            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                if duration >= threshold:
                    Logger.debug(f"{func.__name__} took {duration:.4f}s")
                return result

            return wrapper

        return decorator