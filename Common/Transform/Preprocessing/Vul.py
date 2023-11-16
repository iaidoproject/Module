from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import logging
import json
import logging
from collections import Counter
from pprint import pprint
def plug_in(data, dataType):
    logger = logging.getLogger(__name__)
    try:
        if dataType == 'question':
            a = []
            good_list = []
            weak_list = []
            date_list = []
            QDF = pd.DataFrame(data, columns=['vulnerability_classification',
                                              'vulnerability_code',
                                              'vulnerability_item',
                                              'vulnerability_explanation',
                                              'vulnerability_standard'])
            for i in QDF['vulnerability_standard']:
                a = i.split('취약')
                a[1] = "취약" + a[1]
                good_list.append(a[0])
                weak_list.append(a[1])
                date_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            QDF['vulnerability_standard_good'] = good_list
            QDF['vulnerability_standard_weak'] = weak_list
            # pprint(QDF['vulnerability_standard_good'])
            QDF['vulnerability_create_date'] = date_list
            DF = QDF.drop(['vulnerability_standard'], axis=1)
            return DF
        if dataType == 'VUL':
            try:
                weak_dict = {}
                status_list = []
                value_list = []
                cid_list = []
                cpn_list = []
                ct_list = []
                ip_list = []
                lr_list = []
                os_list = []
                online_list = []
                swv_list = []
                date_list = []
                logger.info('Tanium ' + dataType + ' Data Transform(Dataframe) Plug In Start')
                for i in data:
                    for j in i['list']:
                        if 'cid' in i:
                            cid_list.append(i['cid'])
                        if 'cpn' in i:
                            cpn_list.append(i['cpn'])
                        if 'ct' in i:
                            ct_list.append(i['ct'])
                        if 'ip' in i:
                            ip_list.append(i['ip'])
                        if 'lr' in i:
                            lr_list.append(i['lr'])
                        if 'os' in i:
                            os_list.append(i['os'])
                        if 'online' in i:
                            online_list.append(i['online'])
                        if 'status' in j:
                            status_list.append(j['status'])
                        else:
                            status_list.append('TSE-Error')
                        if 'value' in j:
                            value_list.append(j['value'])
                        else:
                            value_list.append('TSE-Error')
                        if 'SWV' in j:
                            swv_list.append(j['SWV'])
                        else:
                            swv_list.append('TSE-Error')
                        date_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        # class_date_list.append(datetime.now().strftime('%Y-%m-%d'))
                logger.info('Completing list operations for putting into a data frame')
                for i in range(len(value_list)):
                    if type(value_list[i]) == list:
                        for j in range(len(value_list[i])):
                            if type(value_list[i][j]) == dict:
                                value_list[i][j] = str(value_list[i][j])
                    elif type(value_list[i]) == dict:
                        value_list[i] = str(value_list[i])
                dup_cid = dict(Counter(cid_list))
                cid = []
                for x in dup_cid:
                    for y in range(int(dup_cid[x])):
                        cid.append(x + '-' + str(y))
                weak_dict['computer_id'] = cid_list
                weak_dict['vulnerability_code'] = swv_list
                weak_dict['vulnerability_judge_result'] = status_list
                weak_dict['vulnerability_judge_update_time'] = date_list
                weak_dict['vulnerability_judge_reason'] = value_list
                weak_dict['computer_name'] = cpn_list
                weak_dict['chassis_type'] = ct_list
                weak_dict['tanium_client_nat_ip_address'] = ip_list
                # for i in range(len(lr_list)) :
                #     if 'current result unavailable' in lr_list[i] :
                #         lr_list[i] = '0000-00-00 00:00:00.000'
                # pprint(lr_list)
                weak_dict['last_reboot'] = lr_list
                weak_dict['online'] = online_list
                weak_dict['operating_system'] = os_list
                weak_dict['classification_cid'] = cid
                # weak_dict['classification_date'] = class_date_list
                DF = pd.DataFrame(weak_dict)
                DF = DF.astype({'computer_id': 'object'})
                DF = DF.astype({'vulnerability_judge_update_time': 'datetime64'})
                logger.info('Tanium ' + dataType + ' Data Transform(Dataframe) Plug In Finish')
                return DF
            except:
                logger.warning('Error running Tanium ' + dataType + ' Data Transform (Data Frame) plugin')
                return 'error'
    except Exception as e:
        logger.warning('Preprocessing_VUL.py - Error 발생')
        logger.warning('Error : ' + str(e))
