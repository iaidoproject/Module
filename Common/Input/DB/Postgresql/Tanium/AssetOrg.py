import psycopg2
from datetime import datetime, timedelta
import json
import logging
from tqdm import tqdm
def plug_in(dataType) :
    logger = logging.getLogger(__name__)
    try :
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['PWD']
        MAT = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['TNM']['MA']
        DAT = SETTING['CORE']['Tanium']['INPUT']['DB']['PS']['TNM']['DA']
        COLLECTIONTYPE = SETTING['CORE']['Tanium']['ONOFFTYPE']
        CMT = SETTING['CORE']['Tanium']['CYCLE']['MINUTELY']['TIME']
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        
        yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
        minutes_ago = (datetime.today() - timedelta(minutes=CMT/60)).strftime("%Y-%m-%d %H:%M:%S")
        DL = []
        selectConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        selectCur = selectConn.cursor()
        if dataType == 'minutely_asset_all':
            if COLLECTIONTYPE == 'online' :
                SQ = """
                    select 
                        computer_id, computer_name, last_reboot, disk_total_space, disk_used_space, os_platform, 
                        operating_system, is_virtual, chassis_type, ipv_address, listen_port_count, 
                        established_port_count, ram_use_size, ram_total_size, installed_applications_name, 
                        installed_applications_version, installed_applications_silent_uninstall_string, 
                        installed_applications_uninstallable, running_processes, running_service, cup_consumption, 
                        cup_details_system_type, cup_details_cup, cup_details_cup_speed, 
                        cup_details_total_physical_processors, cup_details_total_cores, 
                        cup_details_total_logical_processors, 
                        disk_free_space, high_cup_processes, 
                        high_memory_processes, high_uptime, ip_address, tanium_client_nat_ip_address, 
                        last_logged_in_user, listen_ports_process, listen_ports_name, listen_ports_local_port, 
                        last_system_crash, mac_address, memory_consumption, open_port, open_share_details_name, 
                        open_share_details_path, open_share_details_status, open_share_details_type, 
                        open_share_details_permissions, primary_owner_name, uptime, usb_write_protected, user_accounts, 
                        ad_query_last_logged_in_user_date, ad_query_last_logged_in_user_name, 
                        ad_query_last_logged_in_user_time, tanium_client_subnet, manufacturer, session_ip,
                        nvidia_smi, online, asset_collection_date
                    from  
                        """ + MAT + """ 
                    where 
                        to_char(asset_collection_date , 'YYYY-MM-DD HH24:MI:SS') >= '"""+minutes_ago+"""'"""
            else :
                SQ = """
                    select 
                        computer_id, computer_name, last_reboot, disk_total_space, disk_used_space, os_platform, 
                        operating_system, is_virtual, chassis_type, ipv_address, listen_port_count, 
                        established_port_count, ram_use_size, ram_total_size, installed_applications_name, 
                        installed_applications_version, installed_applications_silent_uninstall_string, 
                        installed_applications_uninstallable, running_processes, running_service, cup_consumption, 
                        cup_details_system_type, cup_details_cup, cup_details_cup_speed, 
                        cup_details_total_physical_processors, cup_details_total_cores, 
                        cup_details_total_logical_processors, 
                        disk_free_space, high_cup_processes, 
                        high_memory_processes, high_uptime, ip_address, tanium_client_nat_ip_address, 
                        last_logged_in_user, listen_ports_process, listen_ports_name, listen_ports_local_port, 
                        last_system_crash, mac_address, memory_consumption, open_port, open_share_details_name, 
                        open_share_details_path, open_share_details_status, open_share_details_type, 
                        open_share_details_permissions, primary_owner_name, uptime, usb_write_protected, user_accounts, 
                        ad_query_last_logged_in_user_date, ad_query_last_logged_in_user_name, 
                        ad_query_last_logged_in_user_time, tanium_client_subnet, manufacturer, session_ip,
                        nvidia_smi, online, asset_collection_date
                    from  
                        """ + MAT

        elif dataType == 'minutely_asset_part':
            if COLLECTIONTYPE == 'online':
                SQ = """
                    select 
                        computer_id, 
                        installed_applications_name, 
                        manufacturer,
                        running_service,
                        session_ip
                    from 
                        """ + MAT + """
                    where 
                        to_char(asset_collection_date , 'YYYY-MM-DD HH24:MI:SS') >= '"""+minutes_ago+"""'"""
            else :
                SQ = """
                    select 
                        computer_id, 
                        installed_applications_name, 
                        manufacturer,
                        running_service,
                        session_ip
                    from 
                        """ + MAT
        elif dataType == 'minutely_daily_asset':
            if COLLECTIONTYPE == 'online':
                SQ = """
                    select
                        ma.computer_id as computer_id,
                        ma.computer_name as computer_name,
                        ma.last_reboot as last_reboot,
                        ma.disk_total_space as disk_total_space,
                        ma.disk_used_space as disk_used_space,
                        ma.os_platform as os_platform, 
                        ma.operating_system as operating_system, 
                        ma.is_virtual as is_virtual, 
                        ma.chassis_type as chassis_type,
                        ma.ipv_address as ipv_address,
                        ma.listen_port_count as today_listen_port_count,
                        da.listen_port_count as yesterday_listen_port_count,
                        ma.established_port_count as today_established_port_count,
                        da.established_port_count as yesterday_established_port_count,
                        ma.ram_use_size as ram_use_size,
                        ma.ram_total_size as ram_total_size, 
                        ma.installed_applications_name as installed_applications_name, 
                        ma.running_service as running_service, 
                        ma.cup_consumption as cup_consumption,
                        ma.online as online,
                        ma.tanium_client_subnet,
                        ma.manufacturer,
                        ma.session_ip,
                        ma.nvidia_smi,
                        ma.cup_details_cup_speed
                    from
                        (select 
                            computer_id, 
                            computer_name,
                            last_reboot, 
                            disk_total_space,
                            disk_used_space, 
                            os_platform, 
                            operating_system, 
                            is_virtual, 
                            chassis_type,
                            ipv_address, 
                            listen_port_count, 
                            established_port_count,
                            ram_use_size, 
                            ram_total_size, 
                            installed_applications_name, 
                            running_service, 
                            cup_consumption,
                            online,
                            tanium_client_subnet,
                            manufacturer,
                            session_ip,
                            nvidia_smi,
                            cup_details_cup_speed
                        from 
                            """+MAT+"""
                        where
                            to_char(asset_collection_date , 'YYYY-MM-DD HH24:MI:SS') >= '"""+minutes_ago+"""'
                        ) as ma
                    LEFT JOIN 
                        (select 
                            computer_id,
                            listen_port_count, 
                            established_port_count
                        from 
                            """+DAT+""" 
                        where 
                            to_char(asset_collection_date , 'YYYY-MM-DD') = '""" + yesterday + """') as da
                    ON ma.computer_id = da.computer_id
                """
            else :
                SQ = """
                    select
                        ma.computer_id as computer_id,
                        ma.computer_name as computer_name,
                        ma.last_reboot as last_reboot,
                        ma.disk_total_space as disk_total_space,
                        ma.disk_used_space as disk_used_space,
                        ma.os_platform as os_platform, 
                        ma.operating_system as operating_system, 
                        ma.is_virtual as is_virtual, 
                        ma.chassis_type as chassis_type,
                        ma.ipv_address as ipv_address,
                        ma.listen_port_count as today_listen_port_count,
                        da.listen_port_count as yesterday_listen_port_count,
                        ma.established_port_count as today_established_port_count,
                        da.established_port_count as yesterday_established_port_count,
                        ma.ram_use_size as ram_use_size,
                        ma.ram_total_size as ram_total_size, 
                        ma.installed_applications_name as installed_applications_name, 
                        ma.running_service as running_service, 
                        ma.cup_consumption as cup_consumption,
                        ma.online as online,
                        ma.tanium_client_subnet,
                        ma.manufacturer,
                        ma.session_ip,
                        ma.nvidia_smi,
                        ma.cup_details_cup_speed
                    from
                        (select 
                            computer_id, 
                            computer_name,
                            last_reboot, 
                            disk_total_space,
                            disk_used_space, 
                            os_platform, 
                            operating_system, 
                            is_virtual, 
                            chassis_type,
                            ipv_address, 
                            listen_port_count, 
                            established_port_count,
                            ram_use_size, 
                            ram_total_size, 
                            installed_applications_name, 
                            running_service, 
                            cup_consumption,
                            online,
                            tanium_client_subnet,
                            manufacturer,
                            session_ip,
                            nvidia_smi,
                            cup_details_cup_speed
                        from 
                            """ + MAT + """
                        ) as ma
                    LEFT JOIN 
                        (select 
                            computer_id,
                            listen_port_count, 
                            established_port_count
                        from 
                            """ + DAT + """ 
                        where 
                            to_char(asset_collection_date , 'YYYY-MM-DD') = '""" + yesterday + """') as da
                    ON ma.computer_id = da.computer_id
                """

        selectCur.execute(SQ)
        selectRS = selectCur.fetchall()
        
        if PROGRESS == 'true' :
            DATA_list = tqdm(enumerate(selectRS), 
                            total=len(selectRS),
                            desc='IP_DB_AOG_{}'.format(dataType))
        else :
            DATA_list = enumerate(selectRS)
            
        for index, RS in DATA_list:
        # for RS in selectRS:
            DL.append(RS)
        logger.info('Asset Table Select connection - ' + dataType+ '성공')
        return DL
    except ConnectionError as e:
        logger.warning('Asset Table Select connection 실패')
        logger.warning('Error : ' + str(e))