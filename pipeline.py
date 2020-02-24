import dask.bag as db
import numpy as np
import time
import gc
import psutil
import os
import glob
import command


class Pipeline:
    INPUT = "input"
    OUTPUT = "output"
    STATS = "stats"
    SIZE = "size"
    MEMORY = "memory"
    READING_TIME = "reading_time"
    WRITING_TIME = "writing_time"
    CPU_TIME = "cpu_time"
    TOTAL_TIME = "total_time"

    def __init__(self, input_file, fincore=False, steps=None):
        self.input_file = input_file
        self.steps = steps
        self.fincore = fincore
        self.start_time = time.time()
        self.bag = db.from_sequence([input_file]) \
            .map(self.task1) \
            .map(self.task2) \
            .map(self.task3)

    def increment(self, input_file, suffix):
        print("\n========================================================================================")
        print("PIPELINE TASK{0} STARTING...\n".format(suffix))
        process = psutil.Process(os.getpid())

        input_filepath = input_file.split('/')
        input_filename = input_filepath[len(input_filepath) - 1]

        filename_parts = input_filename.split('.')
        subject = filename_parts[0].split('_')[0]

        # TODO FINCORE
        print("\n------------------------------------------------------------")
        print("fincore before task{0} read:".format(suffix))
        for i in range(0, suffix):
            if i == 0:
                target_filename = self.input_file
            else:
                target_filename = "output/{0}_{1}.nii.gz".format(subject, i)
            print("\nStats of file: {0}".format(target_filename))
            command.fincore(target_filename)
        start_reading = time.time()
        byte_arr = np.fromfile(input_file, dtype=np.int8)

        finish_reading = time.time()
        reading_time = finish_reading - start_reading

        # TODO FINCORE
        print("\n------------------------------------------------------------")
        print("fincore after task{0} read:".format(suffix))
        for i in range(0, suffix):
            if i == 0:
                target_filename = self.input_file
            else:
                target_filename = "output/{0}_{1}.nii.gz".format(subject, i)
            print("\nStats of file: {0}".format(target_filename))
            command.fincore(target_filename)

        start_cpu = time.time()
        byte_arr = byte_arr + 1
        end_cpu = time.time()

        output_file = "output/{0}_{1}.nii.gz".format(subject, suffix)

        # TODO FINCORE
        print("\n------------------------------------------------------------")
        print("fincore result before task{0} write:".format(suffix))
        for i in range(0, suffix):
            if i == 0:
                target_filename = self.input_file
            else:
                target_filename = "output/{0}_{1}.nii.gz".format(subject, i)
            print("\nStats of file: {0}".format(target_filename))
            command.fincore(target_filename)

        start_writing = time.time()
        byte_arr.tofile(output_file)

        finish_writing = time.time()

        # TODO FINCORE
        print("\n------------------------------------------------------------")
        print("fincore result after task{0} write:".format(suffix))
        for i in range(0, suffix):
            if i == 0:
                target_filename = self.input_file
            else:
                target_filename = "output/{0}_{1}.nii.gz".format(subject, i)
            print("\nStats of file: {0}".format(target_filename))
            command.fincore(target_filename)
        command.fincore("output/{0}_{1}.nii.gz".format(subject, i + 1))

        statinfo = os.stat(input_file)
        print("\nRESULT:")
        print("Start reading:{0:.2f}".format(start_reading - self.start_time))
        print("End reading:{0:.2f}".format(finish_reading - self.start_time))
        print("Start writing:{0:.2f}".format(start_writing - self.start_time))
        print("End writing:{0:.2f}".format(finish_writing - self.start_time))
        print("Input: " + input_file)
        print("Output: " + output_file)
        print("File size: {0} bytes".format(statinfo.st_size))
        print("Reading time: {0:.2f} sec".format(reading_time))

        cpu_time = end_cpu - start_cpu
        print("CPU time: {0:.2f} sec".format(cpu_time))

        writing_time = finish_writing - start_writing
        print("Writing time: {0:.2f} sec".format(writing_time))

        duration = finish_writing - start_reading
        print("Duration: {0:.2f} sec".format(duration))

        print("Memory usage:")
        print(process.memory_info())
        gc.collect()

        result = process.memory_info()

        return {
            Pipeline.INPUT: input_file,
            Pipeline.OUTPUT: output_file,
            Pipeline.STATS: {
                Pipeline.SIZE: statinfo.st_size,
                Pipeline.MEMORY: result[0],
                Pipeline.TOTAL_TIME: duration,
                Pipeline.READING_TIME: reading_time,
                Pipeline.WRITING_TIME: writing_time,
                Pipeline.CPU_TIME: cpu_time
            }
        }

    def task1(self, input_file):
        return self.increment(input_file, 1)

    def task2(self, task1_res):
        input_file = task1_res[Pipeline.OUTPUT]
        result = self.increment(input_file, 2)
        return {
            Pipeline.INPUT: input_file,
            Pipeline.OUTPUT: result[Pipeline.OUTPUT],
            'task1_res': task1_res,
            'task2_res': result
        }

    def task3(self, task2_res):
        input_file = task2_res[Pipeline.OUTPUT]
        result = self.increment(input_file, 3)
        return {
            Pipeline.INPUT: input_file,
            Pipeline.OUTPUT: result[Pipeline.OUTPUT],
            'task1_res': task2_res['task1_res'],
            'task2_res': task2_res['task2_res'],
            'task3_res': result
        }

    def execute(self):
        self.start_time = time.time()
        result = self.bag.compute()[0]
        end = time.time()
        result[Pipeline.TOTAL_TIME] = end - self.start_time
        return result

    def get_bag(self):
        return self.bag

    @staticmethod
    def clean_output_folder():
        output_files = glob.glob('output/*')
        for f in output_files:
            os.remove(f)
