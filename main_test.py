from datetime import datetime
from CORE.Tanium.Dashboard import minutely_plug_in as CTMPI
from CORE.Tanium.Dashboard import daily_plug_in as CTDPI
from CORE.Tanium.Vul import minutely_plug_in as CTVMPI
import urllib3
import logging
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main() :
    if TU == 'true' :
        if CMU == 'true' :
            CTMPI()
            logging.info('Tanium Minutely Module 성공')
        else:
            logging.info('Tanium Minutely cycle 사용여부  : ' + CMU)

        if CDU == 'true' :
            CTDPI()
            logging.info('Tanium Daily Module 성공')
        else:
            logging.info('Tanium Daily cycle 사용여부  : ' + CDU)
            
        if TVU == 'true' :
            install = True
            while install :
                answer = input('취약점 모듈을 처음 사용하십니까? (Y/N)')
                if answer.lower() == 'y' :
                    CTVMPI('first')
                    install = False
                elif answer.lower() == 'n' :
                    CTVMPI('used')
                    install = False

    else:
        logging.info('Tanium 사용여부 : '+TU)

if __name__ == "__main__":

    with open("setting.json", encoding="UTF-8") as f:
        SETTING = json.loads(f.read())
    LOGFD = SETTING['PROJECT']['LOG']['directory']
    LOGFNM = SETTING['PROJECT']['LOG']['fileName']
    LOGFF = SETTING['PROJECT']['LOG']['fileFormat']
    TU = SETTING['CORE']['Tanium']['COREUSE'].lower()
    CMU = SETTING['CORE']['Tanium']['CYCLE']['MINUTELY']['USE'].lower()
    CMT = SETTING['CORE']['Tanium']['CYCLE']['MINUTELY']['TIME']
    CDU = SETTING['CORE']['Tanium']['CYCLE']['DAILY']['USE'].lower()
    TVU = SETTING['CORE']['Tanium']['PROJECT']['VUL']['USE'].lower()

    today = datetime.today().strftime("%Y%m%d")
    logFile = LOGFD + LOGFNM + today + LOGFF
    logFormat = '%(levelname)s, %(asctime)s, %(message)s'
    logDateFormat = '%Y%m%d%H%M%S'
    logging.basicConfig(filename=logFile, format=logFormat, datefmt=logDateFormat, level=logging.DEBUG)
    logging.info('Module Started')
    main()
    logging.info('Module Finished')