import csv
import logging

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


def chunk(sam_param_table):
    with open(sam_param_table) as f:
        x = csv.reader(f)
        cols = next(x)
        head1 = next(x)
        head2 = next(x)
        filenum = 0
        lastfile = False
        while not lastfile:
            lines = [cols, head1, head2]
            for _ in range(400):
                try:
                    lines.append(next(x))
                except StopIteration as exc:
                    lastfile = True
                    LOGGER.error(exc)
                    break
            with open(sam_param_table[-4:] + '_{:d}.csv'.format(filenum),'w') as g:
                y = csv.writer(g)
                y.writerows(lines)
            LOGGER.debug(filenum)
            filenum += 1
