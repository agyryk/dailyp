import datetime
from pytz import timezone


def wrileln(message):
    logger = open('dailyp_queries.log', 'a')
    logger.write('\n')
    logger.write(datetime.datetime.now(timezone('US/Pacific')).strftime("%Y_%m_%d-%H:%M") + ": " + str(message))
    logger.write('\n')
    logger.close()
