import sys
import time
import json
import ast
import os

from pipeline import Pipeline
from export import export

args = sys.argv
if len(args) < 1:
    print("Input file is required!")
else:
    in_file = args[1]
    iteration = int(args[2])
    export_file = "export/" + args[0] + ".json"
    if os.path.exists(export_file):
        stats = ast.literal_eval(open(export_file, "r").read())
    else:
        stats = []

    start = time.time()

    pipeline = Pipeline(in_file)
    result = pipeline.modify(in_file, 1)

    if iteration >= len(stats):
        new_iter_stat = {}
        if len(stats) == 0:
            stats = []
        stats.append(new_iter_stat)

    stats[iteration][in_file] = result[Pipeline.STATS]

    Pipeline.clean_output_folder()
    end = time.time()
    print("TOTAL RUNTIME: {0:.4f}".format(end - start))
    print("=====================================\n")

    export(export_file, json.dumps(stats))
