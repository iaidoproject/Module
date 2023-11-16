from pprint import pprint
from tqdm import tqdm
import pandas as pd
import logging
import json

def plug_in(data, inputPlugin, dataType, columnsType) :
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()

        if inputPlugin == 'DB':
            if dataType == 'minutely_statistics_list' :
                if columnsType == 'usage':
                    DFC = ['computer_id',  'driveUsage', 'ramUsage', 'cpuUsage']
                elif columnsType == 'compare' :
                    DFC = ['computer_id', 'listenPortCountChange','establishedPortCountChange', 'online']
                elif columnsType == 'normal':
                    DFC = ['computer_id', 'computer_name', 'ipv_address', 'chassis_type', 'os_platform', 'operating_system', 'is_virtual', 'last_reboot', 'tanium_client_subnet', 'manufacturer',
                            'nvidia_smi', 'ram_use_size', 'ram_total_size', 'cup_details_cup_speed', 'disk_used_space', 'disk_total_space']
                elif columnsType == 'count':
                    DFC = ['computer_id', 'running_service_count', 'session_ip_count']


                elif columnsType == 'alarm' :
                    DFC = ['computer_id','group_ip','tanium_client_subnet', 'ram', 'cpu', 'listenport_count', 'establishedport_count', 'running_service_count', 'last_reboot', 'drive']
            elif dataType == 'minutely_statistics' :
                DFC = ['classification', 'item', 'item_count']
            elif dataType == 'minutely_statistics_list_online' :
                if columnsType == 'normal':
                    DFC = ['computer_id', 'computer_name', 'ipv_address', 'tanium_client_subnet', 'asset_list_statistics_collection_date']
                elif columnsType == 'count':
                    DFC = ['computer_id', 'ipv_address', 'tanium_client_subnet', 'asset_list_statistics_collection_date']
            DFL = []

            if PROGRESS == 'true' :
                DATA_list = tqdm(enumerate(data),
                                total=len(data),
                                desc='CM_TRF_DF_ST_Part_{}_{}_{}'.format(inputPlugin, dataType, columnsType))
            else :
                DATA_list = enumerate(data)

            for index, d in DATA_list:
                if dataType == 'minutely_statistics_list' :
                    CID = d[0]
                    if columnsType == 'usage' :
                        DUS = d[1]
                        RUS = d[2]
                        CPUUS = d[3]
                        DFL.append([CID, DUS, RUS, CPUUS])
                    elif columnsType == 'compare' :
                        LPC = d[1]
                        EPC = d[2]
                        OL = d[3]
                        DFL.append([CID, LPC, EPC, OL])

                    elif columnsType == 'normal':
                        CNM = d[1]
                        IP = d[2]
                        CT = d[3]
                        OSP = d[4]
                        OS = d[5]
                        IV = d[6]
                        LR = d[7]
                        TCS = d[8]
                        MF = d[9]
                        NS = d[10]
                        RSZ = d[11]
                        RTZ = d[12]
                        CDS = d[13]
                        DSZ = d[14][0]
                        DTS = d[15][0]
                        DFL.append([CID, CNM, IP, CT, OSP, OS, IV, LR, TCS, MF, NS, RSZ, RTZ, CDS, DSZ, DTS])

                    elif columnsType == 'count':
                        RSC = d[1]
                        SIP = d[2]
                        DFL.append([CID, RSC, SIP])

                    elif columnsType == 'alarm':
                        IPG = d[1]
                        TCS = d[2]
                        RAM = d[3]
                        CPU = d[4]
                        LPC = d[5]
                        EPC = d[6]
                        RSC = d[7]
                        LRB = d[8]
                        DUS = d[9]
                        DFL.append([CID,IPG, TCS, RAM, CPU, LPC, EPC, RSC, LRB, DUS])
                elif dataType == 'minutely_statistics' :
                    classification = d[0]
                    item = d[1]
                    IC = d[2]
                    DFL.append([classification, item, IC])
                elif dataType == 'minutely_statistics_list_online' :
                    CID = d[0]
                    IP = d[1]
                    TCS = d[2]
                    ALSCD = d[3]
                    if columnsType == 'normal' :
                        CNM = d[4]
                        DFL.append([CID, IP,TCS, ALSCD, CNM])
                    elif columnsType == 'count' :
                        DFL.append([CID, IP, TCS, ALSCD])
        DF = pd.DataFrame(DFL, columns=DFC)
        logger.info('Statistics/Part.py -  ' + dataType+'/'+columnsType+ ' 성공')
        return DF
    except Exception as e:
        logger.warning('Statistics/Part.py - Error 발생'+ dataType)
        logger.warning('Error : ' + str(e))
