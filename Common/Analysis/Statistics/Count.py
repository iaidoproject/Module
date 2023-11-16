from tqdm import tqdm
import logging
import json
def plug_in(data):
    logger = logging.getLogger(__name__)
    try :
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        DL = []

        if PROGRESS == 'true' :
            DATA_list = tqdm(range(len(data.computer_id)),
                                total=len(data.computer_id),
                                desc='Count')
        else :
            DATA_list = range(len(data.computer_id))

        for c in DATA_list:
        # for c in range(len(data.computer_id)):
            if len(data['running_service'][c]) > 1:
                running_service_count = len(data['running_service'][c])
            else:
                if data['running_service']== 'unconfirmed' :
                    running_service_count = 'unconfirmed'
                else:
                    running_service_count = 1

            if len(data['session_ip'][c][0]) > 1:
                session_ip_count = len(data['session_ip'][c][0])

            else:
                session_ip_count = 1

            DL.append(
                [data.computer_id[c], str(running_service_count), str(session_ip_count)])
        logger.info('Count.py - 성공')
        return DL

    except Exception as e:
        logger.warning('Count.py - Error 발생')
        logger.warning('Error : {}'.format(e))
