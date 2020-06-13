## source : https://gist.github.com/zed/0ac760859e614cd03652

#!/usr/bin/env python
import mmap


def mapcount(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines
