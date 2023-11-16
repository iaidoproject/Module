from datetime import datetime, timedelta
import psycopg2
import json
from tqdm import tqdm
import logging
import sys

def plug_in(data, cycle, type) :
    logger = logging.getLogger(__name__)
    with open("setting.json", encoding="UTF-8") as f:
        SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PWD']
    if type == 'create' :
        success = True
        process = 0
        status = 0
        createConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        createCur = createConn.cursor()
        processList = ["DROP TABLE {}".format(cycle), "DROP SEQ {}".format(cycle), "CREATE SEQ {}".format(cycle), "CREATE TABLE {}".format(cycle)]
        if len(data) == 2 :
            del processList[0 : 2]
        try :
            logger.info('Auto Create Table Start')
            while success :
                if process == 0 :
                    CTQ = data[process]
                if process == 1 :
                    CTQ = data[process]
                if process == 2 :
                    CTQ = data[process]
                if process == 3:
                    CTQ = data[process]
                try :
                    createCur.execute(CTQ)
                    print("{} 이 성공했습니다.".format(processList[process]))
                    logger.info('{} is Successed!!  ({}//{})'.format(processList[process], process + 1, len(processList)))
                    createConn.commit()
                    process = process + 1
                    if len(data) == 2 and process == 2:
                        success = False
                        logger.info('{} Table Create Successed!!'.format(cycle))
                    if process == 4 :
                        success = False
                        logger.info('{} Table Create Successed!!'.format(cycle))
                except Exception as e :
                    if '테이블 없음' in str(e) or 'table "{}" does not exist'.format(cycle) in str(e):
                        
                        print("==========================")
                        logger.warning('Error : {}'.format(str(e).strip()))
                        print('{} '.format(str(e)))
                        print("==========================")
                        
                        if len(data) == 2 :
                            logger.info('{}의 DROP 기능을 켜주세요'.format(cycle))
                            print('{}의 DROP 기능을 켜주세요'.format(cycle))
                            status = 400
                            break
                        createConn.rollback()
                        process = 2
                        logger.info('RESTART {} '.format(processList[process]))
                        print("{} 테이블 다시 생성".format(cycle))
                        print("==========================")
                    elif '"seq_{}_num" 이름의 릴레이션(relation)이 이미 있습니다'.format(cycle) in str(e) or 'relation "seq_{}_num" already exists'.format(cycle) in str(e):
                        if len(data) == 2:
                            if '기타 다른 개체들이 이 개체에 의존하고 있어, seq_{}_num 시퀀스 삭제할 수 없음 '.format(cycle) :
                                print(str(e).split(':')[1])
                                print("AutoCreate를 끄시거나 Drop기능을 켜주시고 다시 실행해주세요")
                                status = 400
                                break
                        
                        print("==========================")
                        logger.warning('Error : {}'.format(str(e).strip()))
                        print('{} '.format(str(e)))
                        print("==========================")
                        createConn.rollback()
                        process = 1
                        logger.info('RESTART {} '.format(processList[process]))
                        print("{} 시퀀스 다시 생성".format(cycle))
                        print("==========================")
                    else :
                        print(str(e))
                        logger.warning('RESTART is Failed : {}'.format(str(e).strip()))
                        status = 400
                        break
                    
            createConn.close()
            if status == 400 :
                print("모듈 종료")
                quit()
            else :
                print("==================={} 테이블이 만들어졌습니다 ===================".format(cycle))
                logger.info('{} Table Create Successed!!'.format(cycle))
        except Exception as e :
            logger.info('ENTRY ERROR : {} '.format(str(e)))
            print(e)
        
    