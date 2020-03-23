"""
Long running Python application.

Every `n` seconds, it logs the current time to the console. The behaviour, such
as message format and `n` itself can be configured by setting environment
variables.

- `TIME_TELLER__STEP`: Number of seconds between each message. Should be
  between `1` and `60`. Otherwise it will be rounded up or down.
- `TIME_TELLER__LOG_TEMPLATE`: The template of the log message. Gets treated as
  a python time format string. See the
  [docs](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
  for more details.
"""
import datetime
import logging
import os
import sys
import time

level = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
logger.addHandler(ch)


TEMPLATE = os.getenv('TIME_TELLER__LOG_TEMPLATE', '%Y-%m-%dT%H:%M:%S')
TIMESTEP = min(
    max(
        int(os.getenv('TIME_TELLER__STEP', 15)),
        1
    ),
    60
)


def next_step(instant: datetime, step: int):
    """
    Round to the next round multiple of step seconds in the minute.

    0 <= step <= 60

    >>> inst = datetime.datetime(2020, 2, 20, 9, 30, 33)
    >>> next_step(inst, 15)
    datetime.datetime(2020, 2, 20, 9, 30, 45)
    >>> inst = datetime.datetime(2020, 2, 20, 9, 30, 30)
    >>> next_step(inst, 15)
    datetime.datetime(2020, 2, 20, 9, 30, 45)
    >>> inst = datetime.datetime(2020, 2, 20, 9, 30, 55)
    >>> next_step(inst, 15)
    datetime.datetime(2020, 2, 20, 9, 31)
    >>> next_step(inst, 60)
    datetime.datetime(2020, 2, 20, 9, 31)
    """
    return instant.replace(
        minute=instant.minute + step * (1 + instant.second // step) // 60,
        second=(step * (1 + instant.second // step)) % 60,
        microsecond=0
    )


def main():
    while True:
        next_instant = next_step(datetime.datetime.now(), TIMESTEP)
        while (now := datetime.datetime.now()) < next_instant:    # noqa
            logger.debug(to_elapse := (next_instant - now).total_seconds())    # noqa
            time.sleep(to_elapse)
        else:
            logger.info(now.strftime(TEMPLATE))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
