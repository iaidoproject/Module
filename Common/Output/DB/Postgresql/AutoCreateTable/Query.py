def QueryPlugIn(name, all_drop_use, drop_use):
    if all_drop_use == 'true' :
        if drop_use =='true' :
            dropT = """DROP TABLE {} ;""".format(name)
            
            dropS = """DROP SEQUENCE seq_{}_num;""".format(name)
    
    createS = """CREATE SEQUENCE seq_{}_num START 1""".format(name)
    
    if name == 'minutely_asset' :
        createT = """CREATE TABLE minutely_asset (
                    minutely_asset_num integer NOT NULL DEFAULT nextval('seq_minutely_asset_num'::regclass),
                    computer_id text NOT NULL,
                    computer_name text NOT NULL,
                    last_reboot text NOT NULL,
                    disk_total_space text NOT NULL,
                    disk_used_space text NOT NULL,
                    os_platform text NOT NULL,
                    operating_system text NOT NULL,
                    is_virtual text NOT NULL,
                    chassis_type text NOT NULL,
                    ipv_address text NOT NULL,
                    listen_port_count text NOT NULL,
                    established_port_count text NOT NULL,
                    ram_use_size text NOT NULL,
                    ram_total_size text NOT NULL,
                    installed_applications_name text NOT NULL,
                    installed_applications_version text NOT NULL,
                    installed_applications_silent_uninstall_string text NOT NULL,
                    installed_applications_uninstallable text NOT NULL,
                    running_processes text NOT NULL,
                    running_service text NOT NULL,
                    cup_consumption text NOT NULL,
                    cup_details_system_type text NOT NULL,
                    cup_details_cup text NOT NULL,
                    cup_details_cup_speed text NOT NULL,
                    cup_details_total_physical_processors text NOT NULL,
                    cup_details_total_cores text NOT NULL,
                    cup_details_total_logical_processors text NOT NULL,
                    disk_free_space text NOT NULL,
                    high_cup_processes text NOT NULL,
                    high_memory_processes text NOT NULL,
                    high_uptime text NOT NULL,
                    ip_address text NOT NULL,
                    tanium_client_nat_ip_address text NOT NULL,
                    last_logged_in_user text NOT NULL,
                    listen_ports_process text NOT NULL,
                    listen_ports_name text NOT NULL,
                    listen_ports_local_port text NOT NULL,
                    last_system_crash text NOT NULL,
                    mac_address text NOT NULL,
                    memory_consumption text NOT NULL,
                    open_port text NOT NULL,
                    open_share_details_name text NOT NULL,
                    open_share_details_path text NOT NULL,
                    open_share_details_status text NOT NULL,
                    open_share_details_type text NOT NULL,
                    open_share_details_permissions text NOT NULL,
                    primary_owner_name text NOT NULL,
                    uptime text NOT NULL,
                    usb_write_protected text NOT NULL,
                    user_accounts text NOT NULL,
                    ad_query_last_logged_in_user_date text NOT NULL,
                    ad_query_last_logged_in_user_name text NOT NULL,
                    ad_query_last_logged_in_user_time text NOT NULL,
                    tanium_client_subnet text NOT NULL,
                    manufacturer text NOT NULL,
                    session_ip text NOT NULL,
                    nvidia_smi text NOT NULL,
                    online text NOT NULL,
                    asset_collection_date timestamp NOT NULL,
                    CONSTRAINT minutely_assest_pk PRIMARY KEY (minutely_asset_num),
                    CONSTRAINT minutely_assest_un UNIQUE (computer_id)
                    );"""
                    
    elif name == 'daily_asset' :
        createT = """CREATE TABLE daily_asset (
                    daily_asset_num integer NOT NULL DEFAULT nextval('seq_daily_asset_num'::regclass),
                    computer_id text NOT NULL,
                    computer_name text NOT NULL,
                    last_reboot text NOT NULL,
                    disk_total_space text NOT NULL,
                    disk_used_space text NOT NULL,
                    os_platform text NOT NULL,
                    operating_system text NOT NULL,
                    is_virtual text NOT NULL,
                    chassis_type text NOT NULL,
                    ipv_address text NOT NULL,
                    listen_port_count text NOT NULL,
                    established_port_count text NOT NULL,
                    ram_use_size text NOT NULL,
                    ram_total_size text NOT NULL,
                    installed_applications_name text NOT NULL,
                    installed_applications_version text NOT NULL,
                    installed_applications_silent_uninstall_string text NOT NULL,
                    installed_applications_uninstallable text NOT NULL,
                    running_processes text NOT NULL,
                    running_service text NOT NULL,
                    cup_consumption text NOT NULL,
                    cup_details_system_type text NOT NULL,
                    cup_details_cup text NOT NULL,
                    cup_details_cup_speed text NOT NULL,
                    cup_details_total_physical_processors text NOT NULL,
                    cup_details_total_cores text NOT NULL,
                    cup_details_total_logical_processors text NOT NULL,
                    disk_free_space text NOT NULL,
                    high_cup_processes text NOT NULL,
                    high_memory_processes text NOT NULL,
                    high_uptime text NOT NULL,
                    ip_address text NOT NULL,
                    tanium_client_nat_ip_address text NOT NULL,
                    last_logged_in_user text NOT NULL,
                    listen_ports_process text NOT NULL,
                    listen_ports_name text NOT NULL,
                    listen_ports_local_port text NOT NULL,
                    last_system_crash text NOT NULL,
                    mac_address text NOT NULL,
                    memory_consumption text NOT NULL,
                    open_port text NOT NULL,
                    open_share_details_name text NOT NULL,
                    open_share_details_path text NOT NULL,
                    open_share_details_status text NOT NULL,
                    open_share_details_type text NOT NULL,
                    open_share_details_permissions text NOT NULL,
                    primary_owner_name text NOT NULL,
                    uptime text NOT NULL,
                    usb_write_protected text NOT NULL,
                    user_accounts text NOT NULL,
                    ad_query_last_logged_in_user_date text NOT NULL,
                    ad_query_last_logged_in_user_name text NOT NULL,
                    ad_query_last_logged_in_user_time text NOT NULL,
                    tanium_client_subnet text NOT NULL,
                    manufacturer text NOT NULL,
                    session_ip text NOT NULL,
                    nvidia_smi text NOT NULL,
                    online text NOT NULL,
                    asset_collection_date timestamp NOT NULL,
                    CONSTRAINT daily_assest_pk PRIMARY KEY (daily_asset_num)
                    );"""
    elif name == 'minutely_statistics_list' :
        createT = """CREATE TABLE minutely_statistics_list (
                    minutely_statistics_list_num integer NOT NULL DEFAULT nextval('seq_minutely_statistics_list_num'::regclass),
                    computer_id text NOT NULL,
                    computer_name text NOT NULL,
                    ipv_address text NOT NULL,
                    chassis_type text NOT NULL,
                    os_platform text NOT NULL,
                    is_virtual text NOT NULL,
                    last_reboot text NOT NULL,
                    driveUsage text NOT NULL,
                    ramUsage text NOT NULL,
                    cpuUsage text NOT NULL,
                    listenPortCountChange text NOT NULL,
                    establishedPortCountChange text NOT NULL,
                    running_service_Count text NOT NULL,
                    online text NOT NULL,
                    operating_system text NOT NULL,
                    tanium_client_subnet text NOT NULL,
                    manufacturer text NOT NULL,
                    session_ip_count text NOT NULL,
                    nvidia_smi text NOT NULL,
                    ram_use_size text NOT NULL,
                    ram_total_size text NOT NULL,
                    cup_details_cup_speed text NOT NULL,
                    disk_used_space text NOT NULL,
                    disk_total_space text NOT NULL,
                    asset_list_statistics_collection_date timestamp NOT NULL,
                    CONSTRAINT minutely_statistics_list_pk PRIMARY KEY (minutely_statistics_list_num),
                    CONSTRAINT minutely_statistics_list_un UNIQUE (computer_id)
                    );"""
    elif name == 'daily_statistics_list' :
        createT = """CREATE TABLE daily_statistics_list (
                    daily_statistics_list_num integer NOT NULL DEFAULT nextval('seq_daily_statistics_list_num'::regclass),
                    computer_id text NOT NULL,
                    computer_name text NOT NULL,
                    ipv_address text NOT NULL,
                    chassis_type text NOT NULL,
                    os_platform text NOT NULL,
                    is_virtual text NOT NULL,
                    last_reboot text NOT NULL,
                    driveUsage text NOT NULL,
                    ramUsage text NOT NULL,
                    cpuUsage text NOT NULL,
                    listenPortCountChange text NOT NULL,
                    establishedPortCountChange text NOT NULL,
                    running_service_Count text NOT NULL,
                    online text NOT NULL,
                    operating_system text NOT NULL,
                    tanium_client_subnet text NOT NULL,
                    manufacturer text NOT NULL,
                    session_ip_count text NOT NULL,
                    nvidia_smi text NOT NULL,
                    ram_use_size text NOT NULL,
                    ram_total_size text NOT NULL,
                    cup_details_cup_speed text NOT NULL,
                    disk_used_space text NOT NULL,
                    disk_total_space text NOT NULL,
                    asset_list_statistics_collection_date timestamp NOT NULL,
                    CONSTRAINT daily_statistics_list_pk PRIMARY KEY (daily_statistics_list_num)
                    );"""
    elif name == 'minutely_statistics' :
        createT = """CREATE TABLE minutely_statistics (
                    minutely_statistics_num integer NOT NULL DEFAULT nextval('seq_minutely_statistics_num'::regclass),
                    minutely_statistics_unique varchar(200) NOT NULL,
                    classification varchar(100) NOT NULL,
                    item text NOT NULL,
                    item_count varchar(100) NOT NULL,
                    statistics_collection_date timestamp NOT NULL,
                    CONSTRAINT minutely_statistics_pk PRIMARY KEY (minutely_statistics_num),
                    CONSTRAINT minutely_statistics_un UNIQUE (minutely_statistics_unique)
                    );"""
    elif name == 'daily_statistics' :
        createT = """CREATE TABLE daily_statistics (
                    daily_statistics_num integer NOT NULL DEFAULT nextval('seq_daily_statistics_num'::regclass),
                    classification varchar(100) NOT NULL,
                    item text NOT NULL,
                    item_count varchar(100) NOT NULL,
                    statistics_collection_date timestamp NOT NULL,
                    CONSTRAINT daily_statistics_pk PRIMARY KEY (daily_statistics_num)
                    );
                    """
    elif name == 'vulnerability_list' :
        createT = """CREATE TABLE vulnerability_list (
                    vulnerability_num int4 NOT NULL DEFAULT nextval('seq_vulnerability_list_num'::regclass),
                    vulnerability_classification varchar(50) NOT NULL,
                    vulnerability_code varchar(50) NOT NULL,
                    vulnerability_item varchar(300) NOT NULL,
                    vulnerability_explanation text NOT NULL,
                    vulnerability_standard_good text NOT NULL,
                    vulnerability_standard_weak text NOT NULL,
                    vulnerability_create_date timestamp NOT NULL,
                    CONSTRAINT vulnerability_list_pk PRIMARY KEY (vulnerability_num),
                    CONSTRAINT vulnerability_list_un UNIQUE (vulnerability_code)
                    );"""
    elif name == 'vulnerability_judge' :
        createT = """CREATE TABLE public.vulnerability_judge (
                vulnerability_judge_num int4 NOT NULL DEFAULT nextval('seq_vulnerability_judge_num'::regclass),
                computer_id varchar(50) NOT NULL,
                vulnerability_code varchar(50) NOT NULL,
                vulnerability_judge_result varchar(10) NOT NULL,
                vulnerability_judge_update_time timestamp NOT NULL,
                vulnerability_judge_reason text NOT NULL,
                computer_name varchar NOT NULL,
                chassis_type varchar NOT NULL,
                tanium_client_nat_ip_address varchar NOT NULL,
                last_reboot varchar NOT NULL,
                operating_system varchar NOT NULL,
                classification_cid varchar NOT NULL,
                online varchar NOT NULL,
                CONSTRAINT vulnerability_judge_pk PRIMARY KEY (vulnerability_judge_num),
                CONSTRAINT vulnerability_judge_un UNIQUE (classification_cid)
                );"""
    if all_drop_use == 'true' :
        if drop_use == 'true' :
            QUERYLIST = [dropT, dropS, createS, createT]
        elif drop_use == 'false' :
            QUERYLIST = [createS, createT]
    elif all_drop_use == 'false' :
        QUERYLIST = [createS, createT]
        
    return QUERYLIST