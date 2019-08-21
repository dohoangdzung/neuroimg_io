import sys
import time
import json
import ast

from pipeline import Pipeline
from export import export

args = sys.argv
if len(args) < 1:
    print("Input file is required!")
else:
    in_file = args[1]
    export_file = "export/" + args[0] + ".json"
    stats = ast.literal_eval(open(export_file, "r").read())

    start = time.time()

    pipeline = Pipeline(in_file)
    result = pipeline.copy(in_file, 1)
    stats[in_file] = result[Pipeline.STATS]
    Pipeline.clean_output_folder()

    end = time.time()
    print("\nTOTAL RUNTIME: {0:.4f}".format(end - start))

    export(export_file, json.dumps(stats))
