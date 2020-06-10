import subprocess

import sys

sys.setrecursionlimit(10000)


def if_restart():
    popen = subprocess.Popen('python I:\workstation-5\cn-3\CN\DRGs_CN_Comp.py',stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    out, err = popen.communicate()

    if err.decode() != "":
        if_restart()
    else:
        print(out.decode("utf-8"))


if_restart()

