

PROTOS = {
    503001 : {'path' : 'route/route', 'name' : 'RegisterA2R_R'},
    503002 : {'path' : 'route/route', 'name' : 'RegisterR2A_S'},
    503003 : {'path' : 'route/route', 'name' : 'RegisterDebugA2R_R'},
    0 : {'path' : 'common/error', 'name' : 'ErrorRes'},
    504001 : { 'path' : 'global/config', 'name' : 'GetServerListA2C_R'},
    504002 : { 'path' : 'global/config', 'name' : 'GetServerListC2A_S'},
    900001 : { 'path' : 'monitor/monica', 'name' : 'GateRouteServerConnInfoReq'},
    900002 : { 'path' : 'monitor/monica', 'name' : 'GateRouteServerConnInfoRes'},
    900003 :{ 'path' : 'monitor/monica', 'name' : 'RegisterServerReq'},
    900004 :{ 'path' : 'monitor/monica', 'name' : 'RegisterServerRes'},
    900005 :{ 'path' : 'monitor/monica', 'name' : 'ResiterServerNotify'},
    900013 :{ 'path' : 'monitor/monica', 'name' : 'GetGameServerInfoReq'},
    900014 :{ 'path' : 'monitor/monica', 'name' : 'GetGameServerInfoRes'},
    900015 :{ 'path' : 'monitor/monica', 'name' : 'GetMonitorServerInfoReq'},
    900016 :{ 'path' : 'monitor/monica', 'name' : 'GetMonitorServerInfoRes'},
    900017 :{ 'path' : 'monitor/monica', 'name' : 'ServerErrorLogNotify'},
    900018 :{ 'path' : 'monitor/monica', 'name' : 'GetServerErrorLogReq'},
    900019 :{ 'path' : 'monitor/monica', 'name' : 'GetServerErrorLogRes'},
    500003 :{ 'path' : 'gate/gate', 'name' : 'RegisterDebugA2G_R'},
    500002 :{ 'path' : 'gate/gate', 'name' : 'RegisterG2A_S'},

    #消息结构    
    "ServerInfo" : { 'path' : 'monitor/monica', 'name' : 'ServerInfo'},
    "Server_Type" : { 'path' : 'common/type', 'name' : 'Server_Type'},
}