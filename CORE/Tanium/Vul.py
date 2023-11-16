import urllib3
import json
import logging
from Common.Input.API.Tanium.Sesstion import plug_in as CIATSPI
from Common.Input.API.Tanium.Sensor.Common import plug_in as CIATSCPI
from Common.Transform.Dataframe.Vul.All import plug_in as CTDAAPI
from Common.Transform.Preprocessing.Vul import plug_in as VUL_TDFPI
from Common.Output.DB.Postgresql.Tanium.Vul.VulOrg import plug_in as CODBPTAOPI
from Common.Input.DB.Postgresql.Vul_List_material.material import vul_list_pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def minutely_plug_in(use): 
    logger = logging.getLogger(__name__)
    if use == 'first':
        VDF = VUL_TDFPI(vul_list_pd(), 'question')
        VQIDB = CODBPTAOPI(VDF, 'question', 'insert')
        if VQIDB == 200 :
            logger.info('VUL Question is  Succesed!!')

    SK = CIATSPI()['dataList'][0]  
    
    VDIPDL = CIATSCPI(SK, 'VUL')['dataList']
    logger.info('recived SessionKey is  Succesed!!')
    
    VUDDFT = CTDAAPI(VDIPDL, 'API', 'VUL')
    logger.info('recived VUL Data is  Succesed!!')
    
    VULDF = VUL_TDFPI(VUDDFT, 'VUL')
    logger.info('Trans DataFrame is Successed!!')
    CODBPTAOPI(VULDF, 'VUL', 'insert')
    logger.info('DB Data is Insert')








