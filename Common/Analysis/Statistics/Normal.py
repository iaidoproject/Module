
from tqdm import tqdm
import logging
import json

def plug_in(data):
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        DL = []

        if PROGRESS == 'true' :
            DATA_list = tqdm( range(len(data.computer_id)),
                                total=len(data.computer_id),
                                desc='Normal')
        else :
            DATA_list = range(len(data.computer_id))

        for c in DATA_list:
        # for c in range(len(data.computer_id)):
            DL.append([data.computer_id[c], data.computer_name[c], data.ipv_address[c], data.chassis_type[c], data.os_platform[c], data.operating_system[c], data.is_virtual[c], str(data.last_reboot[c]), data.tanium_client_subnet[c], data.manufacturer[c], data.nvidia_smi[c],
                        data.ram_use_size[c], data.ram_total_size[c], data.cup_details_cup_speed[c], data.disk_used_space[c], data.disk_total_space[c]])
        logger.info('Normal.py - 성공')
        return DL
    except Exception as e:
        logger.warning('Normal.py - Error 발생')
        logger.warning('Error : {}'.format(str(e)))
