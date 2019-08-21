import sys
import time
import json
import ast
from pipeline import Pipeline
from export import export

args = sys.argv
if len(args) < 2:
    print("Input file is required!")
else:
    in_file = args[1]
    export_file = "export/" + args[0] + ".json"
    stats = ast.literal_eval(open(export_file, "r").read())

    start = time.time()

    p = Pipeline(in_file)
    stats[in_file] = p.execute()
    Pipeline.clean_output_folder()

    end = time.time()

    print("\nTOTAL RUNTIME: {0:.4f}".format(end - start))

    export(export_file, json.dumps(stats))
