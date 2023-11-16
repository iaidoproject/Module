import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import logging

import json
def plug_in(data, classification, itemType) :
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        DL = []
        RD = []
        CNM = itemType

        if PROGRESS == 'true' :
            DATA_list = tqdm( range(len(data.computer_id)),
                                total=len(data.computer_id),
                                desc='GroupByCount : {}_{}'.format(classification, itemType))
        else :
            DATA_list = range(len(data.computer_id))


        for c in DATA_list:
        # for c in range(len(data.computer_id)):
            if classification == 'os' :
                DL.append(data.os_platform[c])
            elif classification == 'operating_system' :
                DL.append(data.operating_system[c])
            elif classification == 'virtual' :
                DL.append(data.is_virtual[c])
            elif classification == 'asset' :
                DL.append(data.chassis_type[c])
            elif classification == 'installed_applications' :
                for d in range(len(data.installed_applications_name[c])):
                    DL.append(data.installed_applications_name[c][d])
            elif classification == 'listen_port_count_change' :
                DL.append(data.listenPortCountChange[c])
            elif classification == 'established_port_count_change' :
                DL.append(data.establishedPortCountChange[c])
            elif classification == 'running_service' :
                if data.running_service[c] == 'unconfirmed':
                    DL.append('unconfirmed')
                else :
                    for d in data.running_service[c] :
                        DL.append(d)
            elif classification == 'drive_usage_size_exceeded' :
                DL.append(data.drive[c])
            elif classification == 'ram_usage_size_exceeded' :
                DL.append(data.ram[c])
            elif classification == 'cpu_usage_size_exceeded' :
                DL.append(data.cpu[c])
            elif classification == 'last_reboot_exceeded' :
                DL.append(data.last_reboot[c])
            elif classification == 'group_ram_usage_exceeded' :
                if data.ram[c] == '95Risk' :
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_cpu_usage_exceeded' :
                if data.cpu[c] == '95Risk':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_listen_port_count_change' :
                if data.listenport_count[c] == 'Yes':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_established_port_count_change' :
                if data.establishedport_count[c] == 'Yes':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_running_service_count_exceeded' :
                if data.running_service_count[c] == 'Yes':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_last_reboot' :
                if data.last_reboot[c] == 'Yes':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_drive_usage_size_exceeded' :
                if data.drive[c] == '99Risk':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_server_count' :
                DL.append(data.tanium_client_subnet[c])
            elif classification == 'group_last_online_time_exceeded' :
                if data.asset_list_statistics_collection_date[c] == 'Yes':
                    DL.append(data.tanium_client_subnet[c])
            elif classification == 'manufacturer' :
                if not data.is_virtual[c] == 'Yes' :
                    DL.append(data.manufacturer[c])
            elif classification == 'nvidia_smi' :
                if data.nvidia_smi[c] =='no results' or data.nvidia_smi[c] == 'unconfirmed':
                    DL.append('NO')
                else :
                    DL.append('YES')
            elif classification == 'session_ip' :
                for d in data.session_ip[c]:
                    if data.session_ip[c] == ['no results'] or data.session_ip[c] == ['unconfirmed']:
                        DL.append('NO')
                    else:
                        for x in d:
                            DL.append(x)
            elif classification == 'last_online_time_exceeded' :
                DL.append(data.asset_list_statistics_collection_date[c])

            elif classification == 'online_asset' :
                DL.append(len(data.computer_id))



        DF = pd.DataFrame(DL, columns=[CNM])
        DFG = DF.groupby([CNM]).size().reset_index(name='counts')
        DFGS = DFG.sort_values(by="counts", ascending=False)

        if classification == 'os' :
            statistics_unique = classification + '_' + DFGS.OP
            item = DFGS.OP
        if classification == 'operating_system' :
            statistics_unique = classification + '_' + DFGS.OS
            item = DFGS.OS
        elif classification == 'virtual':
            statistics_unique = classification + '_' + DFG.IV
            item = DFGS.IV
        elif classification == 'asset':
            statistics_unique = classification+'_'+DFGS.CT
            item = DFGS.CT
        elif classification == 'installed_applications':
            statistics_unique = classification+'_'+DFGS.IANM
            item = DFGS.IANM
        elif classification == 'listen_port_count_change':
            statistics_unique = classification+'_'+ DFGS.LPC
            item = DFGS.LPC
        elif classification == 'established_port_count_change':
            statistics_unique = classification + '_' + DFGS.EPC
            item = DFGS.EPC
        elif classification == 'running_service':
            statistics_unique = classification + '_' + DFGS.RSNM
            item = DFGS.RSNM
        elif classification == 'drive_usage_size_exceeded':
            statistics_unique = classification + '_' + DFGS.DUS
            item = DFGS.DUS
        elif classification == 'ram_usage_size_exceeded':
            statistics_unique = classification + '_' + DFGS.RUS
            item = DFGS.RUS
        elif classification == 'cpu_usage_size_exceeded':
            statistics_unique = classification + '_' + DFGS.CPU
            item = DFGS.CPU
        elif classification == 'last_reboot_exceeded':
            statistics_unique = classification + '_' + DFGS.LRB
            item = DFGS.LRB
        elif classification == 'group_ram_usage_exceeded' or classification == 'group_cpu_usage_exceeded' or classification == 'group_listen_port_count_change' or classification == 'group_established_port_count_change' or classification  == 'group_running_service_count_exceeded' or classification == 'group_last_reboot' or classification == 'group_drive_usage_size_exceeded':
            statistics_unique = classification + '_' + DFGS.tanium_client_subnet
            item = DFGS.tanium_client_subnet
        elif classification == 'group_last_online_time_exceeded':
            statistics_unique = classification + '_' + DFGS.tanium_client_subnet
            item = DFGS.tanium_client_subnet
        elif classification == 'group_server_count':
            statistics_unique = classification + '_' + DFGS.tanium_client_subnet
            item = DFGS.tanium_client_subnet
        elif classification == 'manufacturer':
            statistics_unique = classification + '_' + DFGS.MF
            item = DFGS.MF
        elif classification == 'nvidia_smi':
            statistics_unique = classification + '_' + DFGS.NS
            item = DFGS.NS
        elif classification == 'session_ip':
            statistics_unique = classification + '_' + DFGS.SIP
            item = DFGS.SIP
        elif classification == 'last_online_time_exceeded':
            statistics_unique = classification + '_' + DFGS.LOTE
            item = DFGS.LOTE

        elif classification == 'online_asset':
            statistics_unique = ['online_asset']
            item = ['online_asset']

        item_count = DFG.counts

        for DFC in range(len(DFGS)) :
            RD.append([statistics_unique[DFC], classification, item[DFC], item_count[DFC]])

        logger.info('GroupByCount.py -' + classification + ' 성공')
        return RD
    except Exception as e:
        logger.warning('GroupByCount.py - ' + classification + ' Error 발생')
        logger.warning('Error : {}'.format(str(e)))


