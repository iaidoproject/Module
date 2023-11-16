from datetime import datetime, timedelta
import psycopg2
import json
from tqdm import tqdm
import logging

def plug_in(data, cycle, type) :
    logger = logging.getLogger(__name__)
    with open("setting.json", encoding="UTF-8") as f:
        SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PWD']
        VQ = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['VQ']
        VJ = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['VJ']
        VUL_STS = SETTING['CORE']['Tanium']['ONOFFTYPE']
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
    if type == 'insert' :
        try :
            logger.info('Start the process : {} '.format(cycle))
            if cycle == 'question' :
                TNM = VQ
                insertDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            elif cycle == 'VUL' :
                TNM = VJ
                insertDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            insertConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
            insertCur = insertConn.cursor()
            
            if cycle == 'question':
                IQ = """ INSERT INTO 
                    """ + TNM + """ (
                        vulnerability_classification,
                        vulnerability_code,
                        vulnerability_item,
                        vulnerability_explanation,
                        vulnerability_standard_good,
                        vulnerability_standard_weak,
                        vulnerability_create_date
                        ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                        );"""
            elif cycle == 'VUL' :
                if VUL_STS == 'None' :
                    IQ = """ INSERT INTO 
                    """ + TNM + """ (computer_id,
                                        vulnerability_code,
                                        vulnerability_judge_result,
                                        vulnerability_judge_update_time,
                                        vulnerability_judge_reason,
                                        computer_name,
                                        chassis_type,
                                        tanium_client_nat_ip_address,
                                        last_reboot,
                                        operating_system,
                                        classification_cid,
                                        online) 
                        VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                ) 
                        ON CONFLICT (classification_cid)
                        DO UPDATE SET 
                                computer_id = excluded.computer_id ,
                                vulnerability_code = excluded.vulnerability_code,
                                vulnerability_judge_result = excluded.vulnerability_judge_result,
                                vulnerability_judge_update_time = excluded.vulnerability_judge_update_time,
                                vulnerability_judge_reason = excluded.vulnerability_judge_reason,
                                computer_name = excluded.computer_name,
                                chassis_type = excluded.chassis_type,
                                tanium_client_nat_ip_address = excluded.tanium_client_nat_ip_address,
                                last_reboot = excluded.last_reboot,
                                operating_system = excluded.operating_system,
                                classification_cid = excluded.classification_cid,
                                online = excluded.online;"""
                    datalen = len(data.computer_id)
                elif VUL_STS == "online" :
                    insertCur.execute('TRUNCATE TABLE ' + TNM + ';')
                    insertCur.execute('ALTER SEQUENCE seq_vulnerability_judge_num RESTART WITH 1;')
                    
                    IQ = """ INSERT INTO 
                    """ + TNM + """ (computer_id,
                                        vulnerability_code,
                                        vulnerability_judge_result,
                                        vulnerability_judge_update_time,
                                        vulnerability_judge_reason,
                                        computer_name,
                                        chassis_type,
                                        tanium_client_nat_ip_address,
                                        last_reboot,
                                        operating_system,
                                        classification_cid,
                                        online) 
                        VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                );"""
                elif VUL_STS == "Offline" :
                    return None
            if cycle == 'question' :
                datalen = len(data.vulnerability_code)
            else :
                datalen = len(data.computer_id)

            if PROGRESS == 'true' :
                DATA_list = tqdm(range(datalen),
                                total=datalen,
                                desc='OP_DB_VOG_{}'.format(cycle))
            else :
                DATA_list = range(datalen)
            try :
                for i in DATA_list:
                    if cycle == 'question' :
                        VCL = data.vulnerability_classification[i]
                        VC = data.vulnerability_code[i]
                        VI = data.vulnerability_item[i]
                        VE = data.vulnerability_explanation[i]
                        VSG = data.vulnerability_standard_good[i]
                        VSW = data.vulnerability_standard_weak[i]
                        VCD = data.vulnerability_create_date[i]
                        dataList = VCL, VC, VI, VE, VSG, VSW, VCD
                    elif cycle == 'VUL' :
                        CI = data.computer_id[i]
                        VC = data.vulnerability_code[i]
                        VJR = data.vulnerability_judge_result[i]
                        VJUT = data.vulnerability_judge_update_time[i]
                        VJRS = data.vulnerability_judge_reason[i]
                        VJCN = data.computer_name[i]
                        VJCT = data.chassis_type[i]
                        VJIP = data.tanium_client_nat_ip_address[i]
                        VJLR = data.last_reboot[i]
                        VJOS = data.operating_system[i]
                        CCD = data.classification_cid[i]
                        ONLINE = data.online[i]
                        dataList = CI, VC, VJR, VJUT, VJRS, VJCN, VJCT, VJIP, VJLR, VJOS, CCD, ONLINE
                    insertCur.execute(IQ, (dataList))
            except Exception as e:
                if '고유 제약 조건을 위반함' in str(e) or 'duplicate key value violates unique constraint' in str(e):
                    logger.warning('Error : {} '.format(str(e)))
                    print('이미 Question이 들어가져있습니다.')
                    return 400
                elif '이름의 릴레이션(relation)이 없습니다'.format(str(e)) in str(e):
                    print('{} 테이블이 없습니다'.format(str(e).strip('오류:').split('이름의 릴레이션')[0]))
                    print('취약점 테이블을 생성하시거나 Autocreate를 true로 변경해주세요')
                    logger.warning('Error : {} '.format(str(e)))
                    quit()
                else :
                    print(e)
                    logger.warning('Error : {} '.format(str(e)))
                    return 404
            insertConn.commit()
            insertConn.close()
            logger.info('Insert {} Process is finish '.format(cycle))
            
            return 200
        except ConnectionError as e:
            print(e)
            logger.warning('ConnectionError : {} '.format(str(e)))
        except Exception as e :
            if '이름의 릴레이션(relation)이 없습니다'.format(str(e)) in str(e):
                print('{} 테이블이 없습니다'.format(str(e).strip('오류:').split('이름의 릴레이션')[0]))
                print('취약점 테이블을 생성하시거나 Autocreate를 true로 변경해주세요')
                logger.warning('Error : {} '.format(str(e)))
                quit()