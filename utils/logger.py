__all__ = ['ExpLogger']

from datetime import datetime
from enum import Enum, auto
import os
import time
from pathlib import Path
import gc

import psutil
from multiprocessing import Process, Value
from threading import Thread

# stop_thread = [False]
class Flag(Enum):
    stop = auto()
    stopped = auto()
    run = auto()
    running = auto()
    terminate = auto()

flag = Value('i', Flag.stopped.value)

def measure_memory(process: psutil.Process, log_file_memory:Path, frequency:float):
    """
    Measure the memory usage of the main process every second.
    """
    global flag
    try:
        with open(log_file_memory, 'a') as f:
            # print(flag, flush=True)
            while flag.value != Flag.terminate.value:
                # print(flag, flag.value, flush=True)
                if flag.value == Flag.run.value:
                    flag.value = Flag.running.value
                if flag.value == Flag.running.value:
                    current_time = time.time()
                    memory = process.memory_full_info().uss
                    f.write(f"{current_time},{memory},log\n")
                    f.flush()
                    # print(f"{current_time},{memory}", flush=True)
                    dt = frequency - (time.time() - current_time) - 0.01
                    if dt > 0:
                        time.sleep(dt)
                if flag.value == Flag.stop.value:
                    flag.value = Flag.stopped.value
                
                if flag.value == Flag.stopped.value:
                    time.sleep(0.1)
                
    except Exception as e:
        print(e, flush=True)
        pass

class ExpLogger:
    """
    [Experiment Logger]
    
    Logs the execution time and memory usage of the experiment.
    Execution time:
        'start_measure_time()' method records the start time of the experiment.
        'end_measure_time()' method records the end time of the experiment, calculates the execution time, and logs it.
    
    Memory usage:
        'start_measure_memory()' method creates a process and records the memory usage of the main process.
        'end_measure_memory()' method ends the process.
    
    """
    def __init__(self, log_dir:str, exp_name:str, tag:str, default_overwrite=None, log_start_time=True, log_accuracy:bool=True, log_memory:bool=True, log_time:bool=True):
        log_start_time = datetime.now(tz="Asia/Seoul").strftime("%Y-%m-%d_%H:%M:%S") if log_start_time else ""
        
        self.log_dir = Path(log_dir) / exp_name / f"{log_start_time}_{tag}"
        
        self.terminate = False
        
        self.log_file_accuracy = self.log_dir / 'accuracy.csv' if log_accuracy else None
        self.log_file_memory = self.log_dir / 'memory_usage.csv' if log_memory else None
        self.log_file_time = self.log_dir / 'execution_time.csv' if log_time else None
        
        if self.log_dir.exists():
            # check file only has header
            for log_file in [self.log_file_accuracy, self.log_file_memory, self.log_file_time]:
                if log_file is not None:
                    with open(log_file, 'r') as f:
                        if len(f.readlines()) <= 1:
                            default_overwrite = True
                            print(f"Log file '{log_file}' only has header. Overwriting the log.")
                            break
            
            if default_overwrite is None:
                # ask the user if they want to overwrite the existing log
                print(f"Log directory '{self.log_dir}' already exists.")
                print("Do you want to overwrite the existing log? (y/n)")
                answer = input()
                if answer.lower() != 'y':
                    self.terminate = True
                    return
                else:
                    import shutil
                    shutil.rmtree(self.log_dir)
            elif default_overwrite:
                import shutil
                shutil.rmtree(self.log_dir)
            else:
                self.terminate = True
                return
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        
        # for log_file in [self.log_file_accuracy, self.log_memory, self.log_time]:
        #     if log_file is not None:
        #         with open(log_file, 'w') as f:
        #             f.write("")
        
        self.memory_process = None
        self.main_process = psutil.Process()
        
        if self.log_file_accuracy is not None:
            with open(self.log_file_accuracy, 'w') as f:
                f.write("name,accuracy\n")
        
        if self.log_file_time is not None:
            with open(self.log_file_time, 'w') as f:
                f.write("name,time\n")
        
        if self.log_file_memory is not None:
            with open(self.log_file_memory, 'w') as f:
                f.write("time,memory,name\n")
            self.memory_process = Process(target=measure_memory, args=(self.main_process, self.log_file_memory, .0001))
            self.memory_process.start()
            
        self.start_time = {}
    
    def start_measure_time(self, name:str="main"):
        if self.log_file_time is None:
            return
        
        self.start_time[name] = time.time()
        
    def end_measure_time(self, name:str="main"):
        if self.log_file_time is None:
            return
        
        exec_time = time.time() - self.start_time.pop(name)
        with open(self.log_file_time, 'a') as f:
            f.write(f"{name},{exec_time}\n")  
    
    def set_memory(self):
        if self.log_file_memory is None:
            return
        
        gc.collect()
        self.start_measure_memory(0.0001)
        time.sleep(0.1)
        self.end_measure_memory()
    
    def start_measure_memory(self, frequency=0.5):
        """
        Start a process to log the memory usage
        """
        if self.log_file_memory is None:
            return
        gc.collect()
        
        global flag
        flag.value = Flag.run.value
        
        while flag.value != Flag.running.value:
            time.sleep(0.1)
        
        
    
    def end_measure_memory(self):
        """
        End the thread to log the memory usage
        """
        if self.log_file_memory is None:
            return
        
        # stop_thread[0] = True
        # self.memory_process.terminate()
        global flag
        flag.value = Flag.stop.value
        
        while flag.value != Flag.stopped.value:
            time.sleep(0.1)
    
    def end_measure_memory_and_terminate(self):
        if self.log_file_memory is None:
            return
        
        # stop_thread[0] = True
        # self.memory_process.terminate()
        global flag
        flag.value = Flag.terminate.value
        self.memory_process.join()
        
    def write_accuracy(self, name, accuracy):
        if self.log_file_accuracy is None:
            return
        
        with open(self.log_file_accuracy, 'a') as f:
            f.write(f"{name},{accuracy}\n")
            f.flush()