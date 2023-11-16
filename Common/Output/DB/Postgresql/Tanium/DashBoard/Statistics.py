from datetime import datetime, timedelta
import psycopg2
import json
import logging
from tqdm import tqdm

def plug_in(data, cycle):
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PWD']
        MST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['MS']
        DST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['DS']
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        if cycle == 'minutely':
            TNM = MST
            insertDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        elif cycle == 'daily':
            TNM = DST
            yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
            insertDate = yesterday + " 23:59:59"

        insertConn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        insertCur = insertConn.cursor()
        if cycle == 'minutely':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    minutely_statistics_unique, classification, item, item_count, statistics_collection_date
                ) VALUES (
                    %s, %s, %s, %s, '""" + insertDate + """'
                )
                ON CONFLICT (minutely_statistics_unique)
                DO UPDATE SET
                    classification = excluded.classification, 
                    item = excluded.item, 
                    item_count = excluded.item_count,
                    statistics_collection_date = '""" + insertDate + """'                                                                
            """
        elif cycle == 'daily':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    classification, item, item_count, statistics_collection_date
                ) VALUES (
                    %s, %s, %s, '""" + insertDate + """')"""
        datalen = len(data.classification)
        
        if PROGRESS == 'true' :
            DATA_list = tqdm(range(datalen),
                            total=datalen,
                            desc='OP_DB_ST_{}'.format(cycle))
        else :
            DATA_list = range(datalen)
        for i in DATA_list:
            classification = data.classification[i]
            item = data.item[i]
            IC = str(data.item_count[i])
            if cycle == 'minutely':
                MSU = data.minutely_statistics_unique[i]
                dataList = MSU, classification, item, IC
            elif cycle == 'daily':
                dataList = classification, item, IC
            insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
        logger.info('Statistics Table INSERT connection - ' + cycle + '성공')
    except ConnectionError as e:
        logger.warning('Statistics Table INSERT connection 실패')
        logger.warning('Error : ' + str(e))
