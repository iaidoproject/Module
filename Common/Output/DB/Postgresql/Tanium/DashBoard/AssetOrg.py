from datetime import datetime, timedelta
import psycopg2
import json
from tqdm import tqdm
import logging

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
        MAT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['MA']
        DAT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['DA']
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        #COLLECTIONTYPE = SETTING['CORE']['Tanium']['COLLECTIONTYPE']
        if cycle == 'minutely' :
            TNM = MAT
            insertDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        elif cycle == 'daily' :
            TNM = DAT
            yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
            insertDate = yesterday + " 23:59:59"

        insertConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        insertCur = insertConn.cursor()
        if cycle == 'minutely':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    computer_id, computer_name, last_reboot, disk_total_space, disk_used_space, os_platform, 
                    operating_system, is_virtual, chassis_type, ipv_address, listen_port_count, 
                    established_port_count, ram_use_size, ram_total_size, installed_applications_name, 
                    installed_applications_version, installed_applications_silent_uninstall_string, 
                    installed_applications_uninstallable, running_processes, running_service, cup_consumption, 
                    cup_details_system_type, cup_details_cup, cup_details_cup_speed, 
                    cup_details_total_physical_processors, cup_details_total_cores, 
                    cup_details_total_logical_processors, disk_free_space, high_cup_processes, 
                    high_memory_processes, high_uptime, ip_address, tanium_client_nat_ip_address, 
                    last_logged_in_user, listen_ports_process, listen_ports_name, listen_ports_local_port, 
                    last_system_crash, mac_address, memory_consumption, open_port, open_share_details_name, 
                    open_share_details_path, open_share_details_status, open_share_details_type, 
                    open_share_details_permissions, primary_owner_name, uptime, usb_write_protected, user_accounts, 
                    ad_query_last_logged_in_user_date, ad_query_last_logged_in_user_name, 
                    ad_query_last_logged_in_user_time, tanium_client_subnet, manufacturer, session_ip,
                    nvidia_smi, online, asset_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s,'""" + insertDate + """'
                )
                ON CONFLICT (computer_id)
                DO UPDATE SET
                    computer_name = excluded.computer_name, 
                    last_reboot = excluded.last_reboot, 
                    disk_total_space = excluded.disk_total_space, 
                    disk_used_space = excluded.disk_used_space, 
                    os_platform = excluded.os_platform,
                    operating_system = excluded.operating_system, 
                    is_virtual = excluded.is_virtual, 
                    chassis_type = excluded.chassis_type, 
                    ipv_address = excluded.ipv_address, 
                    listen_port_count = excluded.listen_port_count, 
                    established_port_count = excluded.established_port_count, 
                    ram_use_size = excluded.ram_use_size, 
                    ram_total_size = excluded.ram_total_size, 
                    installed_applications_name = excluded.installed_applications_name, 
                    installed_applications_version = excluded.installed_applications_version,
                    installed_applications_silent_uninstall_string = excluded.installed_applications_silent_uninstall_string, 
                    installed_applications_uninstallable = excluded.installed_applications_uninstallable, 
                    running_processes = excluded.running_processes, 
                    running_service = excluded.running_service, 
                    cup_consumption = excluded.cup_consumption, 
                    cup_details_system_type = excluded.cup_details_system_type, 
                    cup_details_cup = excluded.cup_details_cup, 
                    cup_details_cup_speed = excluded.cup_details_cup_speed, 
                    cup_details_total_physical_processors = excluded.cup_details_total_physical_processors, 
                    cup_details_total_cores = excluded.cup_details_total_cores, 
                    cup_details_total_logical_processors = excluded.cup_details_total_logical_processors, 
                    disk_free_space = excluded.disk_free_space, 
                    high_cup_processes = excluded.high_cup_processes, 
                    high_memory_processes = excluded.high_memory_processes, 
                    high_uptime = excluded.high_uptime, 
                    ip_address = excluded.ip_address, 
                    tanium_client_nat_ip_address = excluded.tanium_client_nat_ip_address, 
                    last_logged_in_user = excluded.last_logged_in_user, 
                    listen_ports_process = excluded.listen_ports_process, 
                    listen_ports_name = excluded.listen_ports_name, 
                    listen_ports_local_port = excluded.listen_ports_local_port, 
                    last_system_crash = excluded.last_system_crash, 
                    mac_address = excluded.mac_address, 
                    memory_consumption = excluded.memory_consumption, 
                    open_port = excluded.open_port, 
                    open_share_details_name = excluded.open_share_details_name, 
                    open_share_details_path = excluded.open_share_details_path, 
                    open_share_details_status = excluded.open_share_details_status, 
                    open_share_details_type = excluded.open_share_details_type, 
                    open_share_details_permissions = excluded.open_share_details_permissions, 
                    primary_owner_name = excluded.primary_owner_name, 
                    uptime = excluded.uptime, 
                    usb_write_protected = excluded.usb_write_protected, 
                    user_accounts = excluded.user_accounts, 
                    ad_query_last_logged_in_user_date = excluded.ad_query_last_logged_in_user_date, 
                    ad_query_last_logged_in_user_name = excluded.ad_query_last_logged_in_user_name, 
                    ad_query_last_logged_in_user_time = excluded.ad_query_last_logged_in_user_time, 
                    tanium_client_subnet = excluded.tanium_client_subnet, 
                    manufacturer = excluded.manufacturer, 
                    session_ip = excluded.session_ip,
                    nvidia_smi = excluded.nvidia_smi, 
                    online = excluded.online,
                    asset_collection_date = '""" + insertDate + """'                                                                
            """
            #print(insertDate)
        elif cycle == 'daily':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    computer_id, computer_name, last_reboot, disk_total_space, disk_used_space, os_platform, 
                    operating_system, is_virtual, chassis_type, ipv_address, listen_port_count, 
                    established_port_count, ram_use_size, ram_total_size, installed_applications_name, 
                    installed_applications_version, installed_applications_silent_uninstall_string, 
                    installed_applications_uninstallable, running_processes, running_service, cup_consumption, 
                    cup_details_system_type, cup_details_cup, cup_details_cup_speed, 
                    cup_details_total_physical_processors, cup_details_total_cores, 
                    cup_details_total_logical_processors, disk_free_space, high_cup_processes, 
                    high_memory_processes, high_uptime, ip_address, tanium_client_nat_ip_address, 
                    last_logged_in_user, listen_ports_process, listen_ports_name, listen_ports_local_port, 
                    last_system_crash, mac_address, memory_consumption, open_port, open_share_details_name, 
                    open_share_details_path, open_share_details_status, open_share_details_type, 
                    open_share_details_permissions, primary_owner_name, uptime, usb_write_protected, user_accounts, 
                    ad_query_last_logged_in_user_date, ad_query_last_logged_in_user_name, 
                    ad_query_last_logged_in_user_time, tanium_client_subnet, manufacturer, session_ip,
                    nvidia_smi, online, asset_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, '""" + insertDate + """')"""
        datalen = len(data.computer_id)
        
        if PROGRESS == 'true' :
            DATA_list = tqdm(range(datalen),
                            total=datalen,
                            desc='OP_DB_AOG_{}'.format(cycle))
        else :
            DATA_list = range(datalen)
            
        for i in DATA_list:
            CI = data.computer_id[i]
            CN = data.computer_name[i]
            LR = data.last_reboot[i]
            DTS = data.disk_total_space[i]
            DUS = data.disk_used_space[i]
            OP = data.os_platform[i]
            OS = data.operating_system[i]
            IV = data.is_virtual[i]
            CT = data.chassis_type[i]
            IP = data.ipv_address[i]
            LPC = data.listen_port_count[i]
            EPC = data.established_port_count[i]
            RUS = data.ram_use_size[i]
            RTS = data.ram_total_size[i]
            IA = data.installed_applications_name[i]
            IAV = data.installed_applications_version[i]
            IASUS = data.installed_applications_silent_uninstall_string[i]
            IAU = data.installed_applications_uninstallable[i]
            RP = data.running_processes[i]
            RS = data.running_service[i]
            CPUC = data.cup_consumption[i]
            CPUDST = data.cup_details_system_type[i]
            CPUDCPU = data.cup_details_cup[i]
            CPUDCPUS = data.cup_details_cup_speed[i]
            CPUDTPP = data.cup_details_total_physical_processors[i]
            CPUDTC = data.cup_details_total_cores[i]
            CPUDTLP = data.cup_details_total_logical_processors[i]
            DFS = data.disk_free_space[i]
            HCPUP = data.high_cup_processes[i]
            HMP = data.high_memory_processes[i]
            HU = data.high_uptime[i]
            IPA = data.ip_address[i]
            TCNATIPA = data.tanium_client_nat_ip_address[i]
            LLIU = data.last_logged_in_user[i]
            LPP = data.listen_ports_process[i]
            LPN = data.listen_ports_name[i]
            LPLP = data.listen_ports_local_port[i]
            LSC = data.last_system_crash[i]
            MACA = data.mac_address[i]
            MC = data.memory_consumption[i]
            openPort = data.open_port[i]
            OSDN = data.open_share_details_name[i]
            OSDPath = data.open_share_details_path[i]
            OSDS = data.open_share_details_status[i]
            OSDT = data.open_share_details_type[i]
            OSDP = data.open_share_details_permissions[i]
            PON = data.primary_owner_name[i]
            Uptime = data.uptime[i]
            USBWP = data.usb_write_protected[i]
            UA = data.user_accounts[i]
            ADQLLIUD = data.ad_query_last_logged_in_user_date[i]
            ADQLLIUN = data.ad_query_last_logged_in_user_name[i]
            ADQLLIUT = data.ad_query_last_logged_in_user_time[i]
            TCS = data.tanium_client_subnet[i]
            manufacturer = data.manufacturer[i]
            SI = data.sessionIp[i]
            NS = data.nvidiaSmi[i]
            OL = data.online[i]
            dataList = CI, CN, LR, DTS, DUS, OP, OS, IV, CT, IP, LPC, EPC, RUS, RTS, IA, IAV, IASUS, IAU, RP, RS, CPUC, \
                       CPUDST, CPUDCPU, CPUDCPUS, CPUDTPP, CPUDTC, CPUDTLP, DFS, HCPUP, HMP, HU, IPA, TCNATIPA, LLIU, \
                       LPP, LPN, LPLP, LSC, MACA, MC, openPort, OSDN, OSDPath, OSDS, OSDT, OSDP, PON, Uptime, USBWP, \
                       UA, ADQLLIUD, ADQLLIUN, ADQLLIUT, TCS, manufacturer, SI, NS, OL
            insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
        logger.info('Asset Table INSERT connection - ' + cycle + ' 성공')
    except ConnectionError as e:
        logger.warning('Asset Table INSERT connection 실패')
        logger.warning('Error : ' + str(e))
