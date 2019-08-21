import dask.bag as db
# import nibabel as nb
import time
import gc
import psutil
import os
import glob


# def load_volume(volume):
#     if isinstance(volume, str):
#         # importing nifti files
#         image = nb.load(volume)
#     # if volume is already a nibabel object
#     elif isinstance(volume, nb.spatialimages.SpatialImage):
#         image = volume
#     else:
#         raise ValueError('Input volume must be a either a path to a file in a '
#                          'format that Nibabel can load, or a nibabel'
#                          'SpatialImage.')
#     return image
#
#
# def save_volume(filename, volume, dtype='float32', overwrite_file=True):
#     if dtype is not None:
#         volume.set_data_dtype(dtype)
#     if os.path.isfile(filename) and overwrite_file is False:
#         print("\nThis file exists and overwrite_file was set to False, "
#               "file not saved.")
#     else:
#         try:
#             volume.to_filename(filename)
#             print("\nSaving {0}".format(filename))
#         except AttributeError:
#             print('\nInput volume must be a Nibabel SpatialImage.')
#
#
# def export_DAX(dask_graph):
#     graph = dask_graph.dependencies
#
#     f = open('pipelines.DAX', 'w')
#
#     task_ids = graph.keys()
#     for task_id in task_ids:
#         f.write('<job id="{0}" namespace="pipeline" name="{0}">\n'.format(task_id))
#         f.write('</job>\n\n'.format(task_id))
#
#     for task_id in task_ids:
#         dependencies = graph[task_id]
#         if len(dependencies) > 0:
#             for parent in dependencies:
#                 f.write('<child ref="{0}">\n'.format(task_id))
#                 f.write('\t<parent ref="{0}"/>\n'.format(parent))
#                 f.write('</child>\n'.format(task_id))
#
#     f.close()


class Pipeline:
    INPUT = "input"
    OUTPUT = "output"
    STATS = "stats"
    SIZE = "size"
    MEMORY = "memory"
    READING_TIME = "reading_time"
    WRITING_TIME = "writing_time"
    TOTAL_TIME = "total_time"

    def __init__(self, input_file, steps=None):
        self.input_file = input_file
        self.steps = steps
        self.bag = db.from_sequence([input_file]) \
            .map(self.task1) \
            .map(self.task2) \
            .map(self.task3)

    def copy(self, input_file, suffix):
        process = psutil.Process(os.getpid())

        input_filepath = input_file.split('/')
        input_filename = input_filepath[len(input_filepath) - 1]

        filename_parts = input_filename.split('.')
        subject = filename_parts[0].split('_')[0]

        start_reading = time.time()

        inp = open(input_file, 'rb')
        file_obj = inp.read()

        finish_reading = time.time()
        reading_time = finish_reading - start_reading

        statinfo = os.stat(input_file)
        print("File size: {0} bytes".format(statinfo.st_size))

        output_file = "output/{0}_{1}.nii.gz".format(subject, suffix)
        temp_file = "output/{0}_{1}_temp.nii.gz".format(subject, suffix)

        out = open(output_file, 'wb')
        out_temp = open(temp_file, 'wb')

        time.sleep(30)

        start_writing = time.time()

        out.write(file_obj)
        out_temp.write(file_obj)

        finish_writing = time.time()

        inp.close()
        out.close()
        out_temp.close()

        writing_time = finish_writing - start_writing

        duration = finish_writing - start_reading

        print("Duration: {0:.2f} sec".format(duration))
        print("Reading time: {0:.2f} sec".format(reading_time))
        print("Writing time: {0:.2f} sec".format(writing_time))
        print("Memory usage:")
        print(process.memory_info())
        print("=====================================\n")
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
                Pipeline.WRITING_TIME: writing_time
            }
        }

    def task1(self, input_file):
        return self.copy(input_file, 1)

    def task2(self, task1_res):
        input_file = task1_res[Pipeline.OUTPUT]
        result = self.copy(input_file, 2)
        return {
            Pipeline.INPUT: input_file,
            Pipeline.OUTPUT: result[Pipeline.OUTPUT],
            'task1_res': task1_res,
            'task2_res': result
        }

    def task3(self, task2_res):
        input_file = task2_res[Pipeline.OUTPUT]
        result = self.copy(input_file, 3)
        return {
            Pipeline.INPUT: input_file,
            Pipeline.OUTPUT: result[Pipeline.OUTPUT],
            'task1_res': task2_res['task1_res'],
            'task2_res': task2_res['task2_res'],
            'task3_res': result
        }

    def execute(self):
        start = time.time()
        result = self.bag.compute()[0]
        end = time.time()
        result[Pipeline.TOTAL_TIME] = end - start
        return result

    def get_bag(self):
        return self.bag

    @staticmethod
    def clean_output_folder():
        output_files = glob.glob('output/*')
        for f in output_files:
            os.remove(f)
