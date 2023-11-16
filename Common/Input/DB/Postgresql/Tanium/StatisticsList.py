import psycopg2
import json
from datetime import datetime, timedelta
import logging
from tqdm import tqdm
def plug_in(dataType) :
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['PWD']
        MSLT = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['TNM']['MSL']
        CMT = SETTING['CORE']['Tanium']['CYCLE']['MINUTELY']['TIME']
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        
        minutes_ago = (datetime.today() - timedelta(minutes=CMT/60)).strftime("%Y-%m-%d %H:%M:%S")
        DL = []
        selectConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        selectCur = selectConn.cursor()
        if dataType == 'minutely':
            SQ = """
                select 
                    computer_id,
                    computer_name,
                    ipv_address,
                    chassis_type,
                    os_platform,
                    operating_system,
                    is_virtual,
                    last_reboot,
                    driveUsage,
                    ramUsage,
                    cpuUsage,
                    listenPortCountChange,
                    establishedPortCountChange,
                    running_service_count,
                    online,
                    tanium_client_subnet, 
                    manufacturer, 
                    session_ip_count, 
                    nvidia_smi,
                    ram_use_size,
                    ram_total_size,
                    cup_details_cup_speed,
                    disk_used_space,
                    disk_total_space,
                    asset_list_statistics_collection_date
                from  
                    """ + MSLT + """
                where to_char(asset_list_statistics_collection_date , 'YYYY-MM-DD HH24:MI:SS') >= '"""+minutes_ago+"""'"""
        elif dataType == 'minutely_statistics_list_online':
            SQ = """
                select
                    computer_id,
                    computer_name,
                    ipv_address,
                    tanium_client_subnet,
                    asset_list_statistics_collection_date
                from
                    """ + MSLT
        selectCur.execute(SQ)
        selectRS = selectCur.fetchall()
        
        if PROGRESS == 'true' :
            DATA_list = tqdm(enumerate(selectRS), 
                            total=len(selectRS),
                            desc='IP_DB_STL_{}'.format(dataType))
        else :
            DATA_list = enumerate(selectRS)
            
        for index, RS in DATA_list:
        # for RS in selectRS:
            DL.append(RS)
        logger.info('Statistics List Table Select connection - ' + dataType + ' 성공')
        return DL
    except ConnectionError as e:
        logger.warning('Statistics List Table Select connection 실패')
        logger.warning('Error : ' + e)