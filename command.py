import subprocess


def fincore(filename):
    if subprocess.Popen("type fincore", shell=True).wait():
        raise Exception("fincore isn't installed")
    return subprocess.Popen("fincore -justsummarize " + filename, shell=True).wait()


def atop(filename):
    return subprocess.Popen("atop -w {0} 1  1".format(filename), shell=True).wait()
