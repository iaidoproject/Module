from datetime import datetime, timedelta
import psycopg2
import json
import logging
from tqdm import tqdm

def plug_in(data, cycle) :
    logger = logging.getLogger(__name__)
    try :
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PWD']
        MSLT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['MSL']
        DSLT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['DSL']
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        if cycle == 'minutely' :
            TNM = MSLT
            insertDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        elif cycle == 'daily' :
            TNM = DSLT
            yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
            insertDate = yesterday + " 23:59:59"

        insertConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        insertCur = insertConn.cursor()
        if cycle == 'minutely':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    computer_id, computer_name, ipv_address, chassis_type, os_platform, operating_system, is_virtual, last_reboot,
                    driveUsage, ramUsage, cpuUsage, listenPortCountChange, establishedPortCountChange,
                    running_service_count, online, tanium_client_subnet, manufacturer, session_ip_count, nvidia_smi, ram_use_size, ram_total_size, cup_details_cup_speed,
                    disk_used_space, disk_total_space, asset_list_statistics_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '""" + insertDate + """'
                )
                ON CONFLICT (computer_id)
                DO UPDATE SET
                    computer_name = excluded.computer_name, 
                    ipv_address = excluded.ipv_address, 
                    chassis_type = excluded.chassis_type, 
                    os_platform = excluded.os_platform,
                    operating_system = excluded.operating_system,
                    is_virtual = excluded.is_virtual, 
                    last_reboot = excluded.last_reboot, 
                    driveUsage = excluded.driveUsage,
                    ramUsage = excluded.ramUsage,
                    cpuUsage = excluded.cpuUsage,
                    listenPortCountChange = excluded.listenPortCountChange,
                    establishedPortCountChange = excluded.establishedPortCountChange,
                    running_service_count = excluded.running_service_count,
                    online = excluded.online,
                    tanium_client_subnet = excluded.tanium_client_subnet,
                    manufacturer = excluded.manufacturer, 
                    session_ip_count = excluded.session_ip_count, 
                    nvidia_smi = excluded.nvidia_smi,
                    ram_use_size = excluded.ram_use_size,
                    ram_total_size = excluded.ram_total_size,
                    cup_details_cup_speed = excluded.cup_details_cup_speed,
                    disk_used_space = excluded.disk_used_space,
                    disk_total_space = excluded.disk_total_space,
                    asset_list_statistics_collection_date = '""" + insertDate + """'                                                                
            """
        elif cycle == 'daily':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    computer_id, computer_name, ipv_address, chassis_type, os_platform, operating_system, is_virtual, last_reboot,
                    driveUsage, ramUsage, cpuUsage, listenPortCountChange, establishedPortCountChange,
                    running_service_count, online, tanium_client_subnet, manufacturer, session_ip_count, nvidia_smi, ram_use_size, ram_total_size, cup_details_cup_speed,
                    disk_used_space, disk_total_space, asset_list_statistics_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '""" + insertDate + """'
                )
            """
        datalen = len(data.computer_id)
        
        if PROGRESS == 'true' :
            DATA_list = tqdm(range(datalen),
                            total=datalen,
                            desc='CM_OP_DB_STL_{}'.format(cycle))
        else :
            DATA_list = range(datalen)

        for i in DATA_list:
            CI = data.computer_id[i]
            CN = data.computer_name[i]
            IP = data.ipv_address[i]
            CT = data.chassis_type[i]
            OP = data.os_platform[i]
            OS = data.operating_system[i]
            IV = data.is_virtual[i]
            LR = data.last_reboot[i]
            DUS = data.driveUsage[i]
            RUS = data.ramUsage[i]
            CPUUS = data.cpuUsage[i]
            LPC = data.listenPortCountChange[i]
            EPC = data.establishedPortCountChange[i]
            RSC = data.running_service_count[i]
            OL = data.online[i]
            TCS = data.tanium_client_subnet[i]
            MF = data.manufacturer[i]
            SIC = data.session_ip_count[i]
            NS = data.nvidia_smi[i]
            RSZ = data.ram_use_size[i]
            RTS = data.ram_total_size[i]
            CDS = data.cup_details_cup_speed[i]
            DSZ = data.disk_used_space[i]
            DTS = data.disk_total_space[i]
            dataList = CI, CN, IP, CT, OP, OS, IV, LR, DUS, RUS, CPUUS, LPC, EPC, RSC, OL, TCS, MF, SIC, NS, RSZ, RTS, CDS, DSZ, DTS
            insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
        logger.info('Statistics List Table INSERT connection - ' + cycle + '성공')
    except ConnectionError as e:
        logger.warning('Statistics List Table INSERT connection 실패')
        logger.warning('Error : ' + str(e))
