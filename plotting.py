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
repetition = len(single)


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
    single_write_avg = []
    for fn in input_file_names:
        file_size = input_files[fn]
        single_read_avg.append(file_size * repetition / sum(single_read_arrs[fn]))
        single_write_avg.append(file_size * repetition / sum(single_write_arrs[fn]))

    single_read_arrs.values()

    fig, (read, write) = plt.subplots(1, 2, dpi=80)
    plt.tight_layout()

    read.plot(file_sizes_in_mb, single_read_avg, 'r.')
    read.set_title("read")
    read.set_xlabel('size (MB)')
    read.set_ylabel('speed (MBps)')

    write.plot(file_sizes_in_mb, single_write_avg, 'b.')
    write.set_title("write")
    write.set_xlabel('size (MB)')
    write.set_ylabel('speed (MBps)')

    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))


def plot_single_spectrum():
    single_read_arrs = parse_single_records(single, Pipeline.READING_TIME)
    single_write_arrs = parse_single_records(single, Pipeline.WRITING_TIME)

    fig, axes = plt.subplots(len(input_files), 2, dpi=80)
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


def create_pipeline_table(results, title):
    headers = ["", "Read (s)", "Write (s)", "Total (s)"]
    fig, axes = plt.subplots(input_size, 1)
    fig.suptitle(title)

    # filename
    #     task
    #         read
    #         write
    stats = {}
    for fn in input_file_names:
        stats[fn] = {}
        stats[fn]['task1'] = {}
        stats[fn]['task1'][Pipeline.READING_TIME] = []
        stats[fn]['task1'][Pipeline.WRITING_TIME] = []
        stats[fn]['task1'][Pipeline.TOTAL_TIME] = []

        stats[fn]['task2'] = {}
        stats[fn]['task2'][Pipeline.READING_TIME] = []
        stats[fn]['task2'][Pipeline.WRITING_TIME] = []
        stats[fn]['task2'][Pipeline.TOTAL_TIME] = []

        stats[fn]['task3'] = {}
        stats[fn]['task3'][Pipeline.READING_TIME] = []
        stats[fn]['task3'][Pipeline.WRITING_TIME] = []
        stats[fn]['task3'][Pipeline.TOTAL_TIME] = []

    for i in range(0, repetition):
        rec = results[i]
        for fn in input_file_names:
            file_stats = rec[fn]

            stats[fn]['task1'][Pipeline.READING_TIME].append(
                file_stats['task1_res'][Pipeline.STATS][Pipeline.READING_TIME])
            stats[fn]['task1'][Pipeline.WRITING_TIME].append(
                file_stats['task1_res'][Pipeline.STATS][Pipeline.WRITING_TIME])
            stats[fn]['task1'][Pipeline.TOTAL_TIME].append(file_stats['task1_res'][Pipeline.STATS][Pipeline.TOTAL_TIME])

            stats[fn]['task2'][Pipeline.READING_TIME].append(
                file_stats['task2_res'][Pipeline.STATS][Pipeline.READING_TIME])
            stats[fn]['task2'][Pipeline.WRITING_TIME].append(
                file_stats['task2_res'][Pipeline.STATS][Pipeline.WRITING_TIME])
            stats[fn]['task2'][Pipeline.TOTAL_TIME].append(file_stats['task2_res'][Pipeline.STATS][Pipeline.TOTAL_TIME])

            stats[fn]['task3'][Pipeline.READING_TIME].append(
                file_stats['task3_res'][Pipeline.STATS][Pipeline.READING_TIME])
            stats[fn]['task3'][Pipeline.WRITING_TIME].append(
                file_stats['task3_res'][Pipeline.STATS][Pipeline.WRITING_TIME])
            stats[fn]['task3'][Pipeline.TOTAL_TIME].append(file_stats['task3_res'][Pipeline.STATS][Pipeline.TOTAL_TIME])

    for i in range(0, len(input_file_names)):
        fn = input_file_names[i]

        task1 = [sum(stats[fn]['task1'][Pipeline.READING_TIME]) / repetition,
                 sum(stats[fn]['task1'][Pipeline.WRITING_TIME]) / repetition,
                 sum(stats[fn]['task1'][Pipeline.TOTAL_TIME]) / repetition]

        task2 = [sum(stats[fn]['task2'][Pipeline.READING_TIME]) / repetition,
                 sum(stats[fn]['task2'][Pipeline.WRITING_TIME]) / repetition,
                 sum(stats[fn]['task2'][Pipeline.TOTAL_TIME]) / repetition]

        task3 = [sum(stats[fn]['task3'][Pipeline.READING_TIME]) / repetition,
                 sum(stats[fn]['task3'][Pipeline.WRITING_TIME]) / repetition,
                 sum(stats[fn]['task3'][Pipeline.TOTAL_TIME]) / repetition]

        task1 = ["%.2f" % x for x in task1]
        task2 = ["%.2f" % x for x in task2]
        task3 = ["%.2f" % x for x in task3]

        task1.insert(0, "task1")
        task2.insert(0, "task2")
        task3.insert(0, "task3")

        table_data = [headers, task1, task2, task3]

        axes[i].table(cellText=table_data, loc='center')
        axes[i].set_title("File size: {0:.0f} MB".format(input_files[fn]))
        axes[i].axis('off')


plot_single_avg()
plot_single_spectrum()
create_pipeline_table(bag, "Pipeline tasks")

plt.show()
