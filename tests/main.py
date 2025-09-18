from wztools import logger, measure_time
import time

@measure_time
def test():
    time.sleep(1)
    logger.info('090')

test()
