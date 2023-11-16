from tqdm import tqdm
import logging
import json

def plug_in(data) :
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        DL = []

        if PROGRESS == 'true' :
            DATA_list = tqdm( range(len(data.computer_id)),
                                total=len(data.computer_id),
                                desc='Usage')
        else :
            DATA_list = range(len(data.computer_id))

        for c in DATA_list:
        # for c in range(len(data.computer_id)):
            if data.disk_used_space[c][0].isdigit() and data.disk_total_space[c][0].isdigit() :
                driveUsage = round(int(data.disk_used_space[c][0]) / int(data.disk_total_space[c][0]) * 100, 1)
            else :
                driveUsage = 'unconfirmed'

            if data.ram_use_size[c].isdigit() and data.ram_total_size[c].isdigit() :
                ramUsage = round(int(data.ram_use_size[c]) / int(data.ram_total_size[c]) * 100, 1)
            else :
                ramUsage = 'unconfirmed'

            if type(data.cup_consumption[c]) == float :
                cpuUsage = round(data.cup_consumption[c],1)
            else :
                cpuUsage = 'unconfirmed'
            DL.append([data.computer_id[c], str(driveUsage), str(ramUsage), str(cpuUsage)])
        logger.info('Usage.py - 성공')
        return DL
    except Exception as e:
        logger.warning('Usage.py - Error 발생')
        logger.warning('Error : {}'.format(str(e)))



    #'computer_id', 'last_reboot', 'disk_total_space', 'disk_used_space',
    #'os_platform', 'is_virtual', 'chassis_type',
    #'ipv_address', 'today_listen_port_count', 'yesterday_listen_port_count',
    #'today_established_port_count', 'yesterday_established_port_count',
    #'ram_use_size', 'ram_total_size', 'installed_applications_name',
    #'running_processes', 'cup_consumption'