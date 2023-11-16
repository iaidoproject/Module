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
            if dataType == 'minutely_statistics_list' :
                DFC = ['computer_id', 'computer_name', 'ipv_address', 'chassis_type', 'os_platform', 'operating_system', 'is_virtual',
                       'last_reboot', 'driveUsage', 'ramUsage', 'cpuUsage', 'listenPortCountChange',
                       'establishedPortCountChange', 'running_service_count', 'online', 'tanium_client_subnet', 'manufacturer', 'session_ip_count', 'nvidia_smi',
                       'ram_use_size', 'ram_total_size', 'cup_details_cup_speed', 'disk_used_space', 'disk_total_space']
            elif dataType == 'minutely_statistics' :
                DFC = ['minutely_statistics_unique', 'classification', 'item', 'item_count']
            DFL = []

            if PROGRESS == 'true' :
                DATA_list = tqdm(enumerate(data),
                                total=len(data),
                                desc='CM_TRF_ST_ALL_{}_{}'.format(inputPlugin, dataType))
            else :
                DATA_list = enumerate(data)

            for index, d in DATA_list:
                if dataType == 'minutely_statistics_list' :
                    CID = d[0]
                    CNM = d[1]
                    IP = d[2]
                    CT = d[3]
                    OSP = d[4]
                    OP = d[5]
                    IV = d[6]
                    LR = d[7]
                    DUS = d[8]
                    RUS = d[9]
                    CPUUS = d[10]
                    LPC = d[11]
                    EPC = d[12]
                    RSC = d[13]
                    OL = d[14]
                    TCS = d[15]
                    MF = d[16]
                    SIP = d[17]
                    NS = d[18]
                    RSZ = d[19]
                    RTZ = d[20]
                    CDS = d[21]
                    DSZ = d[22]
                    DTS = d[23]
                    DFL.append([CID, CNM, IP, CT, OSP, OP, IV, LR, DUS, RUS, CPUUS, LPC, EPC, RSC, OL, TCS, MF, SIP, NS, RSZ, RTZ, CDS, DSZ, DTS])
                elif dataType == 'minutely_statistics':
                    MSU = d[0]
                    classification = d[1]
                    item = d[2]
                    IC = d[3]
                    DFL.append([MSU, classification, item, IC])
        DF = pd.DataFrame(DFL, columns=DFC)
        logger.info('Statistics/All.py -  ' + inputPlugin+'/'+dataType+ ' 성공')
        return DF
    except Exception as e:
        logger.warning('Statistics/ALl.py - Error 발생')
        logger.warning('Error : ' + str(e))


