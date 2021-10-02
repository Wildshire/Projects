from contextlib import contextmanager
import threading
import _thread


@contextmanager
def time_limit(seconds):
    if seconds is None:
        yield
        return
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutError("Timed out!")
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()

