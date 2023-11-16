from tqdm import tqdm
import logging
from ast import literal_eval
def plug_in(data, inputPlugin, project) :
    logger = logging.getLogger(__name__)
    DFC = ['SW1', 'SW2', 'SW2_2', 'SW2-3', 'SW2_4', 'SW3', 'SW4', 'SW4_2']
    
    chekc_swv = [20, 42, 9, 24]
    dict = {}
    dict_list = []
    list_dict = {}
    count = 0
    SWV_list = []
    dataList = []
    try :
        for i in range(len(data)) :
            dict = {}
            dict_list = []
            list_dict = {}
            count = 0
            SWV_list = []
            for index, cdata in enumerate(chekc_swv) :
                for j in range(cdata) :
                    SWV_list.append('SW' + str(index+1) + '-' + str(j + 1).zfill(2))
            for k in range(len(DFC)) :
                count = count + 1
                for j in data[i]['data'][k] :
                    if j['text'] == 'TSE-Error: No Sensor Definition for this Platform':
                        logger.info('ComputerID :  {} has {}'.format(data[i]['cid'], j['text']))
                        continue
                    if j['text'] == 'TSE-Error: Python is disabled':
                        logger.info('ComputerID :  {} has {}'.format(data[i]['cid'], j['text']))
                        continue
                    elif j['text'] == '[current result unavailable]' :
                        logger.info('ComputerID :  {} has {}'.format(data[i]['cid'], j['text']))
                        continue
                    elif j['text'] == 'TSE-Error: Python is not available on this system.':
                        logger.info('ComputerID :  {} has {}'.format(data[i]['cid'], j['text']))
                        continue
                    else :
                        if j['text'] == 'TSE-Error: Failed to send to sensor child process: broken pipe' :
                            dict['SWV'] = DFC[k]
                            dict['value'] = j['text']
                            j['text'] = dict
                        else :
                            if not j['text'].startswith('{') and not j['text'].endswith('}'):
                                j['text'] = '{' + j['text'] + '}'
                            dict = literal_eval(j['text'])
                            SWV_list.remove(dict['SWV'])
                        dict_list.append(dict)
                if len(DFC) == count : 
                    if not len(SWV_list) == 0 :
                        for index in SWV_list :
                            sub_dict = {}
                            sub_dict['SWV'] = index
                            sub_dict['status'] = 'None'
                            sub_dict['value'] = 'None'
                            dict_list.append(sub_dict)
                if len(dict_list) != 0 :
                    list_dict['list'] = dict_list
                    list_dict['cid'] = data[i]['data'][8][0]['text'] #computer_id
                    list_dict['cpn'] = data[i]['data'][9][0]['text'] #computer_name
                    list_dict['os'] = data[i]['data'][10][0]['text'] #Operating System
                    list_dict['ip'] = data[i]['data'][11][0]['text'] #Tanium Client NAT IP Address
                    list_dict['ct'] = data[i]['data'][12][0]['text'] #Chassis Type
                    list_dict['lr'] = data[i]['data'][13][0]['text'] #Last Reboot
                    list_dict['online'] = data[i]['data'][14][0]['text']
            if len(list_dict) != 0 :
                dataList.append(list_dict)
        for i in range(len(dataList)) :
            dataList[i]['list'] = sorted(dataList[i]['list'], key= lambda x: x['SWV'])
        DFL = dataList
        logger.info('Tanium ' + project + ' Data API Call Success')
        
        return DFL
    
    except Exception as e:
        logger.warning('Asset/All.py - Error 발생')
        logger.warning('Error : ' + e)