import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import ast
from pipeline import Pipeline

single = ast.literal_eval(open("export/single.py.json", "r").read())
bag = ast.literal_eval(open("export/bag.py.json", "r").read())

single_result = single[0]
file_sizes_in_mb = [x[Pipeline.SIZE] / 1000000 for x in dict(single_result).values()]

input_files = {}
input_file_names = list(dict(single_result).keys())
for filename in input_file_names:
    input_files[filename] = single_result[filename][Pipeline.SIZE] / 1000000

input_size = len(input_file_names)


def parse_single_records(results, attr):
    # This is the dictionary that stores the statistics of a single task
    # The structure is
    # {'filename1': {
    #     'attr1': value1,
    #     'attr2': value2
    #     },
    #     'filename1': {
    #         'attr1': value1,
    #         'attr2': value2
    #     }
    # }
    stats = {}
    for fn in input_files:
        stats[fn] = []

    for res in results:
        for fn in input_files:
            stats[fn].append(res[fn][attr])

    return stats


def plot_single_avg():
    single_read_arrs = parse_single_records(single, Pipeline.READING_TIME)
    single_write_arrs = parse_single_records(single, Pipeline.WRITING_TIME)

    single_read_avg = []
    for fn in single_read_arrs.keys():
        single_read_avg.append(sum(single_read_arrs[fn]) / len(single_read_arrs[fn]))

    single_write_avg = []
    for fn in single_write_arrs.keys():
        single_write_avg.append(sum(single_write_arrs[fn]) / len(single_write_arrs[fn]))

    single_read_arrs.values()

    fig, (read, write) = plt.subplots(1, 2)

    read.plot(file_sizes_in_mb, single_read_avg, 'r.')
    read.set_title("read")

    write.plot(file_sizes_in_mb, single_write_avg, 'b.')
    write.set_title("write")

    plt.xlabel('size (MB)')
    plt.ylabel('time (s)')
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))


def plot_single_spectrum():
    single_read_arrs = parse_single_records(single, Pipeline.READING_TIME)
    single_write_arrs = parse_single_records(single, Pipeline.WRITING_TIME)

    fig, axes = plt.subplots(len(input_files), 2)
    plt.tight_layout()

    for i in range(0, input_size):
        fn = input_file_names[i]
        filesize_in_mb = input_files[fn]

        axes[i][0].hist([filesize_in_mb / x for x in single_read_arrs[fn]], bins=20)
        axes[i][0].set_xlabel("MBps")
        axes[i][0].set_title('Read, file size = {0:.0f} MB'.format(filesize_in_mb))

        axes[i][1].hist([filesize_in_mb / x for x in single_write_arrs[fn]], bins=20)
        axes[i][1].set_xlabel("MBps")
        axes[i][1].set_title('Write, file size = {0:.0f} MB'.format(filesize_in_mb))


def create_pipeline_table(obj, title):
    files = list(dict(obj).keys())

    headers = ["", "Read (s)", "Write (s)", "Total (s)"]
    fig, axes = plt.subplots(len(files), 1)
    fig.suptitle(title)

    for i in range(0, len(files)):
        key = files[i]
        file_stats = obj[key]

        task1_stats = file_stats['task1_res'][Pipeline.STATS]
        task2_stats = file_stats['task2_res'][Pipeline.STATS]
        task3_stats = file_stats['task3_res'][Pipeline.STATS]

        task1 = [task1_stats[Pipeline.READING_TIME],
                 task1_stats[Pipeline.WRITING_TIME],
                 task1_stats[Pipeline.TOTAL_TIME]]
        task2 = [task2_stats[Pipeline.READING_TIME],
                 task2_stats[Pipeline.WRITING_TIME],
                 task2_stats[Pipeline.TOTAL_TIME]]
        task3 = [task3_stats[Pipeline.READING_TIME],
                 task3_stats[Pipeline.WRITING_TIME],
                 task3_stats[Pipeline.TOTAL_TIME]]

        task1 = ["%.2f" % x for x in task1]
        task2 = ["%.2f" % x for x in task2]
        task3 = ["%.2f" % x for x in task3]

        task1.insert(0, "task1")
        task2.insert(0, "task2")
        task3.insert(0, "task3")

        table_data = [headers, task1, task2, task3]

        axes[i].table(cellText=table_data, loc='center')
        axes[i].set_title("File size: {0:.0f} MB".format(task1_stats[Pipeline.SIZE] / 1000000))
        axes[i].axis('off')


plot_single_avg()
plot_single_spectrum()
# f2 = create_pipeline_table(bag, "Pipeline tasks")

plt.show()
