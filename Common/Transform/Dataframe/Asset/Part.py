import pandas as pd
from tqdm import tqdm
import logging
import json

def plug_in(data, inputPlugin, dataType) :
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()

        if inputPlugin == 'DB':
            if dataType == 'minutely_asset' :
                DFC = ['computer_id', 'installed_applications_name', 'manufacturer', 'running_service', 'session_ip']
            elif dataType == 'minutely_daily_asset' :
                DFC = ['computer_id', 'computer_name', 'last_reboot', 'disk_total_space', 'disk_used_space',
                       'os_platform', 'operating_system', 'is_virtual', 'chassis_type',
                       'ipv_address', 'today_listen_port_count', 'yesterday_listen_port_count',
                       'today_established_port_count', 'yesterday_established_port_count',
                       'ram_use_size', 'ram_total_size', 'installed_applications_name',
                       'running_service', 'cup_consumption', 'online', 'tanium_client_subnet', 'manufacturer',
                       'session_ip', 'nvidia_smi', 'cup_details_cup_speed']
            DFL = []

            if PROGRESS == 'true' :
                DATA_list = tqdm(enumerate(data),
                                total=len(data),
                                desc='CM_TRF_DF_AS_Part_{}_{}'.format(inputPlugin, dataType))
            else :
                DATA_list = enumerate(data)

            for index, d in DATA_list:
            # for d in data:
                if dataType == 'minutely_asset':
                    CID = d[0]
                    IAN= d[1]
                    manufacturer = d[2]
                    RS= d[3]
                    SIP = d[4]
                    DFL.append([CID, IAN, manufacturer, RS, SIP])
                elif dataType == 'minutely_daily_asset' :
                    CID = d[0]
                    CNM = d[1]
                    LR = d[2]
                    DTS = d[3]
                    DUS = d[4]
                    OSP = d[5]
                    OS = d[6]
                    IV = d[7]
                    CT = d[8]
                    IP = d[9]
                    TLPC = d[10]
                    YLPC = d[11]
                    TEPC = d[12]
                    YEPC = d[13]
                    RUS = d[14]
                    RTS = d[15]
                    IAN = d[16]
                    RS = d[17]
                    CC = d[18]
                    OL = d[19]
                    TCS = d[20]
                    MF = d[21]
                    SIP = d[22]
                    NS = d[23]
                    CDS = d[24]
                    DFL.append([CID, CNM, LR, DTS, DUS, OSP, OS, IV, CT, IP, TLPC, YLPC, TEPC, YEPC, RUS, RTS, IAN, RS, CC, OL, TCS, MF, SIP, NS, CDS])

        DF = pd.DataFrame(DFL, columns=DFC)
        logger.info('Asset/Part.py -  ' + inputPlugin+'/'+dataType+ ' 성공')
        return DF
    except Exception as e:
        logger.warning('Asset/Part.py - Error 발생')
        logger.warning('Error : ' + str(e))