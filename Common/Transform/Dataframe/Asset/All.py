import pandas as pd
from tqdm import tqdm
import json
import logging

def plug_in(data, inputPlugin) :
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        PROGRESS = SETTING['PROJECT']['PROGRESSBAR'].lower()
        DFL = []
        DFC = [
            'computer_id', 'computer_name', 'last_reboot', 'disk_total_space', 'disk_used_space', 'os_platform',
            'operating_system', 'is_virtual', 'chassis_type', 'ipv_address', 'listen_port_count',
            'established_port_count', 'ram_use_size', 'ram_total_size', 'installed_applications_name',
            'installed_applications_version', 'installed_applications_silent_uninstall_string',
            'installed_applications_uninstallable', 'running_processes', 'running_service', 'cup_consumption',
            'cup_details_system_type', 'cup_details_cup', 'cup_details_cup_speed',
            'cup_details_total_physical_processors', 'cup_details_total_cores',
            'cup_details_total_logical_processors',
            'disk_free_space', 'high_cup_processes', 'high_memory_processes', 'high_uptime', 'ip_address',
            'tanium_client_nat_ip_address', 'last_logged_in_user', 'listen_ports_process', 'listen_ports_name',
            'listen_ports_local_port', 'last_system_crash', 'mac_address', 'memory_consumption', 'open_port',
            'open_share_details_name', 'open_share_details_path', 'open_share_details_status',
            'open_share_details_type', 'open_share_details_permissions', 'primary_owner_name', 'uptime',
            'usb_write_protected', 'user_accounts', 'ad_query_last_logged_in_user_date',
            'ad_query_last_logged_in_user_name', 'ad_query_last_logged_in_user_time',
            'tanium_client_subnet','manufacturer', 'sessionIp', 'nvidiaSmi', 'online'
        ]
        if PROGRESS == 'true' :
            DATA_list = tqdm(enumerate(data),
                            total=len(data),
                            desc='CM_TRF_DF_AS_ALL_{}'.format(inputPlugin))
        else :
            DATA_list = enumerate(data)

        for index, d in DATA_list :
            if inputPlugin == 'API':
                CI = d[0][0]['text']
                CN = d[1][0]['text']
                LR = d[2][0]['text']
                DTS = []
                for DTSD in d[3]:
                    DTS.append(DTSD['text'])
                DUS = []
                for DUSD in d[4]:
                    DUS.append(DUSD['text'])
                OP = d[5][0]['text']
                OS = d[6][0]['text']
                IV = d[7][0]['text']
                CT = d[8][0]['text']
                IP = d[9][0]['text']
                LPC = d[10][0]['text']
                EPC = d[11][0]['text']
                RUS = d[12][0]['text']
                RTS = d[13][0]['text']
                IA = []
                for IAD in d[14]:
                    IA.append(IAD['text'])
                IAV = []
                for IAVD in d[15]:
                    IAV.append(IAVD['text'])
                IASUS = []
                for IASUSD in d[16]:
                    IASUS.append(IASUSD['text'])
                IAU = []
                for IAUD in d[17]:
                    IAU.append(IAUD['text'])
                RP = []
                for RPD in d[18]:
                    RP.append(RPD['text'])
                RS = []
                for RSD in d[19]:
                    RS.append(RSD['text'])
                CPUC = d[20][0]['text']
                CPUDST = d[21][0]['text']
                CPUDCPU = d[22][0]['text']
                CPUDCPUS = d[23][0]['text']
                CPUDTPP = d[24][0]['text']
                CPUDTC = d[25][0]['text']
                CPUDTLP = d[26][0]['text']
                DFS = []
                for DFSD in d[27]:
                    DFS.append(DFSD['text'])
                HCPUP = []
                for HCPUPD in d[28]:
                    HCPUP.append(HCPUPD['text'])
                HMP = []
                for HMPD in d[29]:
                    HMP.append(HMPD['text'])
                HU = []
                for HUD in d[30]:
                    HU.append(HUD['text'])
                IPA = []
                for IPAD in d[31]:
                    IPA.append(IPAD['text'])
                TCNATIPA = d[32][0]['text']
                LLIU = d[33][0]['text']
                LPP = []
                for LPPD in d[34]:
                    LPP.append(LPPD['text'])
                LPN = []
                for LPND in d[35]:
                    LPN.append(LPND['text'])
                LPLP = []
                for LPLPD in d[36]:
                    LPLP.append(LPLPD['text'])
                LSC = d[37][0]['text']
                MACA = []
                for MACAD in d[38]:
                    MACA.append(MACAD['text'])
                MC = d[39][0]['text']
                openPort = []
                for op in d[40]:
                    openPort.append(op['text'])
                OSDN = []
                for OSDND in d[41]:
                    OSDN.append(OSDND['text'])
                OSDPath = []
                for OSDPathD in d[42]:
                    OSDPath.append(OSDPathD['text'])
                OSDS = []
                for OSDSD in d[43]:
                    OSDS.append(OSDSD['text'])
                OSDT = []
                for OSDTD in d[44]:
                    OSDT.append(OSDTD['text'])
                OSDP = []
                for OSDPD in d[45]:
                    OSDP.append(OSDPD['text'])
                PON = d[46][0]['text']
                Uptime = d[47][0]['text']
                USBWP = d[48][0]['text']
                UA = []
                for UAD in d[49]:
                    UA.append(UAD['text'])
                ADQLLIUD = d[50][0]['text']
                ADQLLIUN = d[51][0]['text']
                ADQLLIUT = d[52][0]['text']
                TCS = d[53][0]['text']
                manufacturer = d[54][0]['text']
                SI =[]
                for SID in d[55] :
                    SI.append(SID['text'])
                nvidiaSmi = []
                for NS in d[56] :
                    nvidiaSmi.append(NS['text'])
                OL = d[57][0]['text']


            if inputPlugin == 'DB':
                CI = d[0]
                CN = d[1]
                LR = d[2]
                DTS = d[3]
                DUS = d[4]
                OP = d[5]
                OS = d[6]
                IV = d[7]
                CT = d[8]
                IP = d[9]
                LPC = d[10]
                EPC = d[11]
                RUS = d[12]
                RTS = d[13]
                IA = d[14]
                IAV = d[15]
                IASUS = d[16]
                IAU = d[17]
                RP = d[18]
                RS = d[19]
                CPUC = d[20]
                CPUDST = d[21]
                CPUDCPU = d[22]
                CPUDCPUS = d[23]
                CPUDTPP = d[24]
                CPUDTC = d[25]
                CPUDTLP = d[26]
                DFS = d[27]
                HCPUP = d[28]
                HMP = d[29]
                HU = d[30]
                IPA = d[31] # 확인
                TCNATIPA = d[32]
                LLIU = d[33]
                LPP = d[34]
                LPN = d[35]
                LPLP = d[36]
                LSC = d[37]
                MACA = d[38]
                MC = d[39]
                openPort = d[40]
                OSDN = d[41]
                OSDPath = d[42]
                OSDS = d[43]
                OSDT = d[44]
                OSDP = d[45]
                PON = d[46]
                Uptime = d[47]
                USBWP = d[48]
                UA = d[49]
                ADQLLIUD = d[50]
                ADQLLIUN = d[51]
                ADQLLIUT = d[52]
                TCS = d[53]
                manufacturer = d[54]
                SI = d[55]
                nvidiaSmi = d[56]
                OL = d[57]

            DFL.append(
                [CI, CN, LR, DTS, DUS, OP, OS, IV, CT, IP, LPC, EPC, RUS, RTS, IA, IAV, IASUS, IAU, RP, RS, CPUC,
                    CPUDST, CPUDCPU, CPUDCPUS, CPUDTPP, CPUDTC, CPUDTLP, DFS, HCPUP, HMP, HU, IPA, TCNATIPA, LLIU,
                    LPP, LPN, LPLP, LSC, MACA, MC, openPort, OSDN, OSDPath, OSDS, OSDT, OSDP, PON, Uptime, USBWP,
                    UA, ADQLLIUD, ADQLLIUN, ADQLLIUT, TCS, manufacturer, SI, nvidiaSmi, OL])
        
        DF = pd.DataFrame(DFL, columns=DFC)
        logger.info('Asset/All.py -  ' + inputPlugin + ' 성공')
        return DF
        
    except Exception as e:
        logger.warning('Asset/All.py - Error 발생')
        logger.warning('Error : ' + str(e))