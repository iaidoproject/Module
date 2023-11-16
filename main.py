from datetime import datetime, timedelta
from CORE.Tanium.Dashboard import minutely_plug_in as CTMPI
from CORE.Tanium.Dashboard import daily_plug_in as CTDPI
from CORE.Tanium.Vul import minutely_plug_in as CTVMPI
from Common.ETC.thread import count as count
from Common.Output.DB.Postgresql.AutoCreateTable.Query import QueryPlugIn as QPI
from Common.Output.DB.Postgresql.AutoCreateTable.AutoCreateOrg import plug_in as CODPTV
import urllib3
import threading
import logging
import time
import json
from Common.ETC.logger import date_handler
from apscheduler.schedulers.background import BlockingScheduler
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

run_main = True
MinuitTime = 0
result_list = []
def minutely() :
    if CMU == 'true':
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print('\rminutely', end ="")
        print(now)
        CTMPI()
        if TVU == 'true' :
            CTVMPI('used')
        logger.info('Minutely CMU Module Succesed!!')
    else:
        logger.info('Tanium Minutely cycle 사용여부  : ' + CMU)

def daily():
    if CDU == 'true' :
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print('\rdaily', end ="")
        print(now)
        CTDPI()
        logger.info('Minutely CDU Module Succesed!!')
    else:
        logger.info('Tanium Daily cycle 사용여부  : ' + CDU)
        
def vul() :
    if TVU == 'true' :
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print('\rVUL', end ="")
        print(now)
        CTVMPI('')
        logger.info('Minutely VUL Module Succesed!!')
    else:
        logger.info('Tanium VUL cycle 사용여부  : ' + TVU)

def main():
    if CUSTOMER == "X-FACTOR" :
        if TU == 'true':
            if AUTOCREATEUSE == 'true' : #테이블 자동생성
                for i in AUTOCREATE.values() :
                    if i['USE'] == 'TRUE' :
                        query = QPI(i['NAME'], DROP, i['DROP'].lower())
                        CODPTV(query, i['NAME'], 'create')
                logger.info('AutoCreate Success!!!')
            try :
                if CMU == 'true' :
                    CTMPI()
                    logger.info('Tanium Minutely Module 성공')
                    print('Tanium Minutely Module 성공')
                else:
                    logger.info('Tanium Minutely cycle 사용여부  : ' + CMU)
                
                if TVU == 'true' :
                    CTVMPI('first')
                    logger.info('Tanium VUL Module 성공')
                    print('Tanium VUL Module 성공')
                else:
                    logger.info('Tanium VUL cycle 사용여부  : ' + CDU)
                
                if PTD == "true" :
                    if CDU == 'true' :
                        CTDPI()
                        logger.info('Tanium Daily Module 성공')
                        print('Tanium Daily Module 성공')
                    else:
                        logger.info('Tanium Daily cycle 사용여부  : ' + CDU)
            except Exception as e :
                if AUTOCREATEUSE == 'false' :
                    if '이름의 릴레이션(relation)이 없습니다' in str(e) :
                        print('{} 테이블이 없습니다'.format(str(e).strip('오류:').split('이름의 릴레이션')[0]))
                        print('테이블을 생성하시거나 AUTOCREATE를 True로 변경해주세요')
                        quit()
                    elif 'does not exist' in str(e) :
                        print('{} 테이블이 없습니다'.format(str(e).strip('relation ').split('does not exist')[0]))
                        print('테이블을 생성하시거나 AUTOCREATE를 True로 변경해주세요')
                        quit()
                    else :
                        print(str(e))
            
            print("스케쥴링을 시작하겠습니다.")
            
            for i in reversed(range(3)) :
                print("...........{}".format(i + 1), end="\r")
                time.sleep(1) 
                
            thread.start()
            sched = BlockingScheduler(timezone='Asia/Seoul')
            sched.add_job(minutely, 'interval', seconds=CMT)  # seconds='3'
            sched.add_job(daily, 'cron', hour=CDTH, minute=CDTM)
            sched.add_job(vul, 'interval', seconds=CMT)  # seconds='3'
            logger.info('Start the Scheduling~')
            sched.start()
        else:
            logger.info('Tanium 사용여부 : '+TU)

if __name__ == "__main__":
    with open("setting.json", encoding="UTF-8") as f:
        SETTING = json.loads(f.read())
    CUSTOMER = SETTING['PROJECT']['CUSTOMER']
    
    AUTOCREATE = SETTING['PROJECT']['AUTOCREATE']['TABLE']
    AUTOCREATEUSE = SETTING['PROJECT']['AUTOCREATE']['USE'].lower()
    PTD = SETTING['PROJECT']['TEST']['DAILY'].lower()
    TU = SETTING['CORE']['Tanium']['COREUSE'].lower()
    CMU = SETTING['CORE']['Tanium']['CYCLE']['MINUTELY']['USE'].lower()
    CMT = SETTING['CORE']['Tanium']['CYCLE']['MINUTELY']['TIME']
    CDU = SETTING['CORE']['Tanium']['CYCLE']['DAILY']['USE'].lower()
    CDTH = SETTING['CORE']['Tanium']['CYCLE']['DAILY']['TIME']['hour']
    CDTM = SETTING['CORE']['Tanium']['CYCLE']['DAILY']['TIME']['minute']
    TVU = SETTING['CORE']['Tanium']['PROJECT']['VUL']['USE'].lower()
    DROP = SETTING['PROJECT']['AUTOCREATE']['DROP'].lower()
    
    # today = datetime.today().strftime("%Y%m%d")
    # logFile = LOGFD + LOGFNM + today + LOGFF
    # logFormat = '%(levelname)s, %(asctime)s, %(message)s'
    # logDateFormat = '%Y%m%d%H%M%S'
    # # logging.basicConfig(filename=logFile, format=logFormat, datefmt=logDateFormat, level=logging.DEBUG)
    # # file_handler = RotatingFileHandler(filename='log/log.log', maxBytes=1024*1024*100, backupCount=10)

    # # Create a file handler that rotates log files by date
    # # date_handler = TimedRotatingFileHandler(filename='log/log.log', when='midnight', interval=1, backupCount=10, encoding='utf-8')
    # # date_handler.suffix = '%Y%m%d.log'
    # # Create a console handler

    # # Create a logging format
    # formatter = logging.Formatter('%(levelname)s, %(asctime)s, %(message)s')
    # # file_handler.setFormatter(formatter)
    # # date_handler.setFormatter(formatter)
    # # console_handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(date_handler())
    logger.info('Module Started')
    
    thread = threading.Thread(target=count)
    thread.daemon = True
    main()
    logger.info('Module Finished')


