#! python

import csv
import logging
import sys

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
CHUNKSIZE = 500

def chunk(sam_param_table, chunksize=CHUNKSIZE):
    with open(sam_param_table) as f:
        x = csv.reader(f)
        cols = next(x)
        head1 = next(x)
        head2 = next(x)
        filenum = 0
        lastfile = False
        while not lastfile:
            lines = [cols, head1, head2]
            for _ in range(chunksize):
                try:
                    lines.append(next(x))
                except StopIteration:
                    lastfile = True
                    break
            savename = sam_param_table[:-4] + '_{:d}.csv'.format(filenum)
            with open(savename,'w') as g:
                y = csv.writer(g)
                y.writerows(lines)
            LOGGER.debug(savename)
            filenum += 1


if __name__ == '__main__':
    if len(sys.argv) > 2:
        chunksize = int(sys.argv[2])
        chunk(sys.argv[1], chunksize)
    elif len(sys.argv) > 1:
        chunk(sys.argv[1])
    else:
        LOGGER.warning('missing file name')
