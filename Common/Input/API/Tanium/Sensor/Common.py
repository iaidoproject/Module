import requests
import json
import logging
from tqdm import tqdm

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
    

APIURL = SETTING['CORE']['Tanium']['INPUT']['API']['URL']
CSP = SETTING['CORE']['Tanium']['INPUT']['API']['PATH']['Sensor']

PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()


def plug_in(sessionKey, projectType) :
    logger = logging.getLogger(__name__)
    try:
        if projectType == 'DSB' :
            CSID = SETTING['CORE']['Tanium']['INPUT']['API']['SensorID']['COMMON']
        elif projectType == 'VUL' :
            CSID = SETTING['CORE']['Tanium']['INPUT']['API']['SensorID']['VUL']
        CSH = {'session': sessionKey}
        CSU = APIURL + CSP + CSID
        CSR = requests.post(CSU, headers=CSH, verify=False)
        CSRC = CSR.status_code
        CSRT = CSR.content.decode('utf-8')
        CSRJ = json.loads(CSRT)
        CSRJD = CSRJ['data']
        
        if projectType == 'DSB' :
            dataList = []
            if PROGRESS == 'true' :
                DATA_list = tqdm(enumerate(CSRJD['result_sets'][0]['rows']), 
                                total=len(CSRJD['result_sets'][0]['rows']),
                                desc='CALL_API : {}'.format(CSP))
            else :
                DATA_list = enumerate(CSRJD['result_sets'][0]['rows'])
                
            for index, d in DATA_list :
                DL = []
                for i in d['data'] :
                    DL.append(i)
                dataList.append(DL)
        elif projectType == 'VUL' :
            dataList = CSRJD['result_sets'][0]['rows']
        RD = {'resCode': CSRC, 'dataList': dataList}
        logger.info('Tanium API Sensor 호출 성공')
        logger.info('Sensor ID : ' + str(CSID))
        
        return RD
    except :
        logger.warning('Tanium API Sensor 호출 Error 발생')
        logger.warning('Sensor ID : '+str(CSID))