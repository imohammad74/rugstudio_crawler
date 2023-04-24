import concurrent.futures
import time
from multiprocessing import cpu_count


class Worker:

    @staticmethod
    def cpu_cores():
        cpu_cores = int(cpu_count())
        return cpu_cores

    def main(self, fn, **kwargs):
        max_worker = kwargs['max_worker'] if 'max_worker' in kwargs else self.cpu_cores()
        data = kwargs['data'] if 'data' in kwargs else None
        t1 = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
            if data is not None:
                executor.map(fn, data)
            else:
                executor.map(fn)
        t2 = time.perf_counter()
        print(f'MultiThreaded Code Took:{(t2 - t1):.5f} seconds')

    def __init__(self, fn, **kwargs):
        self.main(fn=fn, **kwargs)
