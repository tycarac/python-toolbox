"""Trivial calculator to show sleep times using library urllib3 retry algorithm

Sleep calculation is:
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    sleep_between_retries = {backoff_factor} * (2 ** ({retry_number} - 1))
Simply, the sleep before retries has an initial value of 'backoff' which doubles in value before the next retry

Note:
 - Maximum backoff in urllib calculation is 120s
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.retry.Retry.BACKOFF_MAX
 - Default number of retries is 3 and default backoff factor is 0.0
    https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.retry.Retry.DEFAULT
"""

from io import StringIO
import urllib3

BACKOFF_MAX = 120
DEFAULT_NUMBER_RETRIES = 3


# _____________________________________________________________________________
def calc_sleep(backoff_factor, number_retries):
    return list(map(lambda x: min(backoff_factor * (2 ** (x - 1)), urllib3.Retry.BACKOFF_MAX), range(number_retries)))


# _____________________________________________________________________________
def output(backoff_factor, number_retries):
    with StringIO() as buf:
        buf.write('%5.1f  - ' % backoff_factor)
        for i, s in enumerate(calc_sleep(backoff_factor, number_retries), 1):
            buf.write('%8.1f ' % s)
            if i % DEFAULT_NUMBER_RETRIES == 0:
                buf.write('  |  ')
        print('%s' % buf.getvalue())


# _____________________________________________________________________________
def main():
    number_retries = 6
    for backoff_factor in [0, 0.5, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]:
        output(backoff_factor, number_retries)


# _____________________________________________________________________________
if __name__ == '__main__':
    main()
