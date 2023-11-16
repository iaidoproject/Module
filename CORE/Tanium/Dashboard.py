

import urllib3
import json



from Common.Input.API.Tanium.Sesstion import plug_in as CIATSPI
from Common.Input.API.Tanium.Sensor.Common import plug_in as CIATSCPI
from Common.Input.DB.Postgresql.Tanium.AssetOrg import plug_in as CIDBPTAOPI
from Common.Input.DB.Postgresql.Tanium.StatisticsList import plug_in as CIDBPTSLPI
from Common.Input.DB.Postgresql.Tanium.Statistics import plug_in as CIDBPTSPI
from Common.Transform.Dataframe.Asset.All import plug_in as CTDAAPI
from Common.Transform.Dataframe.Asset.Part import plug_in as CTDAPPI
from Common.Transform.Dataframe.Statistics.All import plug_in as CTDSAPI
from Common.Transform.Dataframe.Statistics.Part import plug_in as CTDSPPI
from Common.Transform.Preprocessing.Dashboard import plug_in as CTPPI
from Common.Transform.Merge import plug_in as CTMPI
from Common.Analysis.Statistics.Usage import plug_in as CASUPI
from Common.Analysis.Statistics.GroupByCount import plug_in as CASGBCPI
from Common.Analysis.Statistics.Compare import plug_in as CASCPI
from Common.Analysis.Statistics.Normal import plug_in as CASNPI
from Common.Analysis.Statistics.Count import plug_in as CASCOPI
from Common.Output.DB.Postgresql.Tanium.DashBoard.AssetOrg import plug_in as CODBPTAOPI
from Common.Output.DB.Postgresql.Tanium.DashBoard.StatisticsList import plug_in as CODBPTSLPI
from Common.Output.DB.Postgresql.Tanium.DashBoard.Statistics import plug_in as CODBPTAPI

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def minutely_plug_in():                                                                     # 변수 명 Full Name : Full Name에서 대문자로 명시한 것들을 뽑아서 사용 (괄호 안의 내용은 설명)
    with open("setting.json", encoding="UTF-8") as f:
        SETTING = json.loads(f.read())
    SOMIPAPIU = SETTING['CORE']['Tanium']['SOURCE']['MINUTELY']['INPUT']['API'].lower()            # (Source Data MINUTELY Input plug in API 사용 여부 설정)
    SOMTPIU = SETTING['CORE']['Tanium']['SOURCE']['MINUTELY']['Transform'].lower()            # (Source Data MINUTELY Transform(preprocessing) plug in 사용 여부 설정)
    SOMOPIDBPU = SETTING['CORE']['Tanium']['SOURCE']['MINUTELY']['OUTPUT']['DB']['PS'].lower()      # (Source Data MINUTELY Output plug in postgresql DB 사용 여부 설정)
    STCU = SETTING['CORE']['Tanium']['STATISTICS']['COLLECTIONUSE'].lower()                      # (통계 Data 수집 여부 설정)
    STMIPIDBPU = SETTING['CORE']['Tanium']['STATISTICS']['MINUTELY']['INPUT']['DB']['PS'].lower()   # (통계 Data MINUTELY Input plug in postgresql DB 사용 여부 설정)
    STMTPIU = SETTING['CORE']['Tanium']['STATISTICS']['MINUTELY']['Transform'].lower()              # (통계 Data MINUTELY Transform(preprocessing) plug in 사용 여부 설정)
    STMOPODBPU = SETTING['CORE']['Tanium']['STATISTICS']['MINUTELY']['OUTPUT']['DB']['PS'].lower()  # (통계 Data MINUTELY Output plug in postgresql DB 사용 여부 설정)
    
    # SOURCE
    if SOMIPAPIU == 'true':     # (Source Data MINUTELY Input plug in API 사용 여부 확인 - 사용함.)
        SK = CIATSPI()['dataList'][0]  # Sesstion Key (Tanium Sesstion Key 호출)
        SDIPDL = CIATSCPI(SK, 'DSB')['dataList']                             # Source Data InPut Data List (Tanium API Sensor Data 호출)
    # input plug in 이 API 외의 것들 구현 예정
    SODDFT = CTDAAPI(SDIPDL, 'API')                                                         # Source Data Data Frame Transform (호출한 데이터를 Data Frame 형태로 변형)
    if SOMTPIU == 'true' :                                                                  # (Source Data MINUTELY Transform(preprocessing) plug in 사용 여부 확인 - 사용함.)
        SOPPT = CTPPI(SODDFT, 'minutely_asset_all')
        SOODL = CTDAAPI(SOPPT, 'DB')
    else :                                                                                  # (Source Data MINUTELY Transform(preprocessing) plug in 사용 여부 확인 - 사용안함.)
        SOODL = SODDFT

    if SOMOPIDBPU == 'true' :                                                               # (Source Data MINUTELY Output plug in postgresql DB 사용 여부 확인 - 사용함.)
        CODBPTAOPI(SOODL, 'minutely')                                                       # (minutely_asset Table에 수집)
    # output plug in 이 postgresql DB 외의 것들 구현 예정

    
    # STATISTICS
    if STCU == 'true' :                                                                     # (통계 Data 수집 여부 확인 - 사용함.)
        # statistics List
        if STMIPIDBPU == 'true' :                                                           # (통계 Data MINUTELY Input plug in postgresql DB 사용 여부 확인 - 사용함.)
            MDSDDIPDL = CIDBPTAOPI('minutely_daily_asset')                                  # Minutely Daily Source Data InPut Data List (Module로 DB에 수집한 데이터 호출 : minutely_asset, daily_asset Table)
        # input plug in 이 postgresql DB 외의 것들 구현 예정
        MDSDDFTF = CTDAPPI(MDSDDIPDL, 'DB', 'minutely_daily_asset')                         # Minutely Daily Source Data Data Frame Transform First (호출한 데이터를 Data Frame 형태로 변형)
        if STMTPIU == 'true':                                                               # (통계 Data MINUTELY Transform(preprocessing) plug in 사용 여부 확인 - 사용함.)
            MDSDDPPT = CTPPI(MDSDDFTF, 'minutely_daily_asset')                              # Minutely Daily Source Data PreProcession Transform (데이터 전처리)
            MDSDDFTS = CTDAPPI(MDSDDPPT, 'DB', 'minutely_daily_asset')                      # Minutely Daily Source Data Data Frame Transform Second (전처리한 데이터를 Data Frame 형태로 변형)
        else:                                                                               # (통계 Data MINUTELY Transform(preprocessing) plug in 사용 여부 확인 - 사용안함.)
            MDSDDFTS = MDSDDFTF


        US = CASUPI(MDSDDFTS)                                                               # Usage Statistics (사용량 통계)
        USDFT = CTDSPPI(US, 'DB', 'minutely_statistics_list', 'usage')                      # Usage Statistics DataFrame Transform (사용량 통계를 Data Frame 형태로 변형)
        CS = CASCPI(MDSDDFTS, 'compare')                                                           # Compare Statistics (비교 통계)
        CSDFT = CTDSPPI(CS, 'DB', 'minutely_statistics_list', 'compare')                    # Compare Statistics DataFrame Transform (비교 통계를 Data Frame 형태로 변형)



        NS = CASNPI(MDSDDFTS)                                                               # Normal Statistics (일반 값)
        NSDFT = CTDSPPI(NS, 'DB', 'minutely_statistics_list', 'normal')                     # Normal Statistics DataFrame Transform ( 일반 값을 Data Frame 형태로 변형)
        COS=CASCOPI(MDSDDFTS)                                                               # Count Statistics (일반 값)
        COSDFT = CTDSPPI(COS, 'DB', 'minutely_statistics_list', 'count')                    # Count Statistics DataFrame Transform ( 카운트 값을 Data Frame 형태로 변형)
        


        UCSM = CTMPI(USDFT, CSDFT)                                                          # Usage and Compare Statistics Merge (DataFrame 형태의 사용량 통계 & 비교 통계 병합)
        UCNSM = CTMPI(UCSM, NSDFT)                                                          # UCSM and Normal Statistics Merge (DataFrame 형태의 상위 통계 & 일반 통계 병합)
        UCNCOSM = CTMPI(UCNSM, COSDFT)                                                      # UCNSM and Count Statistics Merge (DataFrame 형태의 상위 통계 & 카운트 통계 병합)

        if STMOPODBPU == 'true' :                                                           # (통계 Data MINUTELY Output plug in postgresql DB 사용 여부 확인 - 사용함.)
            CODBPTSLPI(UCNCOSM, 'minutely')                                                 # (minutely_statistics_list Table에 수집)
        # output plug in 이 postgresql DB 외의 것들 구현 예정

        # statistics
        if STMIPIDBPU == 'true':                                                            # (통계 Data MINUTELY Input plug in postgresql DB 사용 여부 확인 - 사용함.)
            IPMALSDL = CIDBPTSLPI('minutely')                                               # InPut Minutely Asset List Statistics Data List (Module로 DB에 수집한 데이터 호출 : minutely_statistics_list Table)
            IPMSLOALSDL= CIDBPTSLPI('minutely_statistics_list_online')
        # input plug in 이 postgresql DB 외의 것들 구현 예정

        IPMALSDDFT = CTDSAPI(IPMALSDL, 'DB', 'minutely_statistics_list')                    # Data Frame Transform (호출한 데이터를 Data Frame 형태로 변형)
        MDSDDFTFON = CTDSPPI(IPMSLOALSDL, 'DB', 'minutely_statistics_list_online', 'normal')  # list테이블의 asset_list_statistics_collection_date를 Data Frame 변형
        OSGBS = CASGBCPI(IPMALSDDFT, 'os', 'OP')                                            # OS Group By Statistics (OS 통계)
        OSVGBS = CASGBCPI(IPMALSDDFT, 'operating_system', 'OS')                            # OS Version Group By Statistics (OS 버전 포함 통계)
        IVGBS = CASGBCPI(IPMALSDDFT, 'virtual', 'IV')                                       # Is Virtual Group By Statistics (가상, 물리 자산 통계)
        CTGBS = CASGBCPI(IPMALSDDFT, 'asset', 'CT')                                         # Chassis Type Group By Statistics (자산 형태 통계)
        LPCGBS = CASGBCPI(IPMALSDDFT, 'listen_port_count_change', 'LPC')                    # Listen Port Count Group By Statistics (listen port count 변경 여부 통계)
        EPCGBS = CASGBCPI(IPMALSDDFT, 'established_port_count_change', 'EPC')               # Listen Port Count Group By Statistics (established port count 변경 여부 통계)
        AC = CASCPI(IPMALSDDFT, 'alarm')                                                    #
        ADT = CTDSPPI(AC, 'DB', 'minutely_statistics_list', 'alarm')                        #
        DUSGBS = CASGBCPI(ADT, 'drive_usage_size_exceeded', 'DUS')                          #
        RUSGBS = CASGBCPI(ADT, 'ram_usage_size_exceeded', 'RUS')                            #
        CPUGBS = CASGBCPI(ADT, 'cpu_usage_size_exceeded', 'CPU')                            #
        LRBGBS = CASGBCPI(ADT, 'last_reboot_exceeded', 'LRB')                               #
        GRUGBS = CASGBCPI(ADT, 'group_ram_usage_exceeded', 'tanium_client_subnet')                      #
        GCUGBS = CASGBCPI(ADT, 'group_cpu_usage_exceeded', 'tanium_client_subnet')                      #
        GLPCGBS = CASGBCPI(ADT, 'group_listen_port_count_change', 'tanium_client_subnet')               #
        GEPCGBS = CASGBCPI(ADT, 'group_established_port_count_change', 'tanium_client_subnet')          #
        GRSCGBS = CASGBCPI(ADT, 'group_running_service_count_exceeded', 'tanium_client_subnet')         #
        GRPLRGBS = CASGBCPI(ADT, 'group_last_reboot', 'tanium_client_subnet')                           #
        GDUSGBS = CASGBCPI(ADT, 'group_drive_usage_size_exceeded', 'tanium_client_subnet')              #
        GSCGBS = CASGBCPI(ADT, 'group_server_count', 'tanium_client_subnet')                            # group_server Group By Statistics (Session_ip 통계)
        MFGBS = CASGBCPI(IPMALSDDFT, 'manufacturer', 'MF')                                  # Manufacturer Group By Statistics (Session_ip 통계)
        GPUCGBS = CASGBCPI(IPMALSDDFT, 'nvidia_smi', 'NS')                                  # Nvidia_smi Group By Statistics (Nvidia_smi 통계)
        CSO = CASCPI(MDSDDFTFON, 'online')  # Compare Statistic Online - online data를 비교 통계
        CSODFT = CTDSPPI(CSO, 'DB', 'minutely_statistics_list_online', 'count')
        GLOTGBS = CASGBCPI(CSODFT, 'group_last_online_time_exceeded', 'tanium_client_subnet')# 대역별 최근 30분 이내 오프라인 여부
        ONGBS = CASGBCPI(CSODFT, 'last_online_time_exceeded', 'LOTE')  # Last Online Group By Statistics (최근 30분 이내 오프라인 여부 통계)


        MAIPDL = CIDBPTAOPI('minutely_asset_part')                                          # Minutely Asset InPut Data List (Module로 DB에 수집한 데이터 호출 : minutely_asset Table)
        MADFTF = CTDAPPI(MAIPDL, 'DB', 'minutely_asset')                                    # Minutely Asset Data Frame Transform First (호출한 데이터를 Data Frame 형태로 변형)
        MAPPT = CTPPI(MADFTF, 'minutely_asset')                                             # Minutely Asset PreProcession Transform (데이터 전처리)
        MADFTS = CTDAPPI(MAPPT, 'DB', 'minutely_asset')                                     # Minutely Asset Data Frame Transform Second (전처리한 데이터를 Data Frame 형태로 변형)
        IAGBS = CASGBCPI(MADFTS, 'installed_applications', 'IANM')                          # Installed Applications Group By Statistics (Installed Application 통계)
        RSGBS = CASGBCPI(MADFTS, 'running_service', 'RSNM')                                 # Running Service Group By Statistics (Running Service 통계)
        SIPGBS = CASGBCPI(MADFTS, 'session_ip', 'SIP')                                      # Session_Ip Group By Statistics (Session_ip 통계)
        ONAGBC = CASGBCPI(IPMALSDDFT, 'online_asset','')                                    # 서버전체수량 Statistic Table 적재

        MSTD = OSGBS + OSVGBS + IVGBS + CTGBS + LPCGBS + EPCGBS + IAGBS + RSGBS + LRBGBS + DUSGBS + RUSGBS + CPUGBS + GRUGBS + GCUGBS + GLPCGBS + GEPCGBS + GRSCGBS + GRPLRGBS + GDUSGBS + GLOTGBS + GSCGBS + ONGBS + MFGBS + GPUCGBS + SIPGBS + ONAGBC # Minutely Statistics Total Data (minutely_statistics Table에 넣을 모든 통계데이터)
        SDDFT = CTDSAPI(MSTD, 'DB', 'minutely_statistics')                                  # Statistics Data Data Frame Transform (Statistics 데이터를 Data Frame 형태로 변형)

        if STMOPODBPU == 'true':                                                            # (통계 Data MINUTELY Output plug in postgresql DB 사용 여부 확인 - 사용함.)
            CODBPTAPI(SDDFT, 'minutely')


def daily_plug_in():                                                                        # 변수 명 Full Name : Full Name에서 대문자로 명시한 것들을 뽑아서 사용 (괄호 안의 내용은 설명)
    CSMDL = CIDBPTAOPI('minutely_asset_all')                                                # Common Sensor Minutely Data List (Module로 DB에 수집한 데이터 호출 : minutely_asset Table )
    MSDDFT = CTDAAPI(CSMDL, 'DB')                                                           # minutely Source Data Data Frame Transform (호출한 데이터를 Data Frame 형태로 변형)
    CODBPTAOPI(MSDDFT, 'daily')                                                             # (daily_asset Table에 수집)

    MSLDIPDL = CIDBPTSLPI('minutely')                                                       # Minutely Statistics List Data InPut Data List (Module로 DB에 수집한 데이터 호출 : minutely_statistics_list Table)
    MSLDDFT = CTDSAPI(MSLDIPDL, 'DB', 'minutely_statistics_list')                           # Minutely Statistics List Data Data Frame Transform (호출한 데이터를 Data Frame 형태로 변형)
    CODBPTSLPI(MSLDDFT, 'daily')                                                            # (daily_statistics_list Table에 수집)

    MSIPDL = CIDBPTSPI('minutely')                                                          # InPut Data List (Module로 DB에 수집한 데이터 호출 : minutely_statistics Table)
    MSDFT = CTDSPPI(MSIPDL, 'DB', 'minutely_statistics', '')                                # Data Frame Transform (호출한 데이터를 Data Frame 형태로 변형)
    CODBPTAPI(MSDFT, 'daily')                                                               # (daily_statistics Table에 수집)








