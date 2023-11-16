import pandas as pd
import logging

def plug_in(leftDF, rightDF) :
    logger = logging.getLogger(__name__)
    try:
        RD = pd.merge(left=leftDF, right=rightDF, how="outer", on=['computer_id'])
        logger.info('Merge.py - 성공')
        return RD
    except Exception as e:
        logger.warning('Merge.py - Error 발생')
        logger.warning('Error : ' + str(e))