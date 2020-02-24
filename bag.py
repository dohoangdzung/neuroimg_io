import sys
import time
import json
import ast
import os
from pipeline import Pipeline
from export import export


def run(args):
    if len(args) < 2:
        print("Input file is required!")
    else:
        in_file = args[1]

        fincore = False
        iteration = 0
        if len(args) > 2:
            iteration = int(args[2])
            fincore = False

        export_file = "export/" + args[0] + ".json"
        if os.path.exists(export_file):
            stats = ast.literal_eval(open(export_file, "r").read())
        else:
            stats = []

        start = time.time()

        p = Pipeline(in_file, fincore)

        if not fincore:
            # If benchmarking
            if iteration >= len(stats):
                new_iter_stat = {}
                if len(stats) == 0:
                    stats = []
                stats.append(new_iter_stat)

        stats[iteration][in_file] = p.execute()

        Pipeline.clean_output_folder()

        end = time.time()

        print("TOTAL RUNTIME: {0:.4f}".format(end - start))
        print("=====================================\n")

        export(export_file, json.dumps(stats))


run(sys.argv)
