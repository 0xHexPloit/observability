import pandas as pd
import psutil

from multiprocessing import Process, Queue
from datetime import datetime


class CPUUsage:
    def __init__(self):
        self._process = None
        self._queue = Queue()

    def _monitor_cpu_usage(self, queue):
        """
        Monitor CPU usage and store results in the queue
        """
        try:
            seconds = 0
            while True:
                timestamp = datetime.now()
                cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
                
                # Create a dictionary with timestamp and CPU data
                data = {
                    'seconds': seconds,
                    'cpu_data': cpu_percentages
                }
                queue.put(data)
                seconds += 1

        except Exception as e:
            queue.put(None)  # Signal that monitoring has stopped
            raise e

    def start_monitoring(self) -> None:
        """
        Start the CPU monitoring process
        """
        if self._process is not None and self._process.is_alive():
            raise RuntimeError("Monitoring is already running")
            
        self._process = Process(target=self._monitor_cpu_usage, args=(self._queue,))
        self._process.start()

    def stop_monitoring(self) -> pd.DataFrame:
        """
        Stop monitoring and return collected data as DataFrame
        """
        if self._process is None or not self._process.is_alive():
            raise RuntimeError("No monitoring process is running")

        # Terminate the process
        self._process.terminate()
        self._process.join()
        
        # Collect all data from queue
        data = []
        while not self._queue.empty():
            item = self._queue.get()
            if item is not None:
                data.append(item)

        # Create DataFrame
        if not data:
            return pd.DataFrame()

        # Expand the CPU data into columns
        rows = []
        for item in data:
            seconds = item['seconds']
            cpu_data = item['cpu_data']
            row = {'seconds': seconds}
            for i, cpu_percent in enumerate(cpu_data):
                row[f'CPU_{i}'] = cpu_percent
            rows.append(row)

        df = pd.DataFrame(rows)
        df.set_index('seconds', inplace=True)
        
        return df