# -*- coding: UTF-8 -*-
import struct, base64

def HeartbeatRequest(bytes):
    vn = struct.unpack("<H", bytes)[0]
    return locals()

signal_trans = ('0-Resume', '1-Hang up')
def HangUpRequest(bytes):
    vn, signal = struct.unpack("<HB", bytes)
    signal = signal_trans[signal]
    return locals()

def LocalRouteRequest(bytes):
    vn, token, _len = struct.unpack("<HHB", bytes[:5])
    route_numbers = struct.unpack("<" + "H" * _len, bytes[5:])[0]
    return locals()

def SimpleRequest(bytes):
    sn, vn = struct.unpack("<8sH", bytes)
    return locals()

def TaskRequest(bytes):
    vn, task_id, point, op_code, value1, value2, value3, value4 = struct.unpack("<HBHHHHHH", bytes)
    return locals()

def RouteRequest(bytes):
    vn, _len = struct.unpack("<HB", bytes[:3])
    route_numbers = struct.unpack("<%dH" % _len, bytes[3:])
    return locals()

block_type_trans = ("0-None-Blocking", "1-Blocking", "2-Area Blocking", "3-Variable Blocking")
def BlockRequest(bytes):
    vn, block_type, block_value = struct.unpack("<HBH", bytes)
    block_type = block_type_trans[block_type]
    return locals()

def WriteBitRequest(bytes):
    vn, bit, value = struct.unpack("<HBB", bytes)
    return locals()

def WriteValueRequest(bytes):
    vn, start_index, _len = struct.unpack("<HBB", bytes[:4])
    values = struct.unpack("<%dH" % _len, bytes[4:])[0]
    return locals()

def ReadValueRequest(bytes):
    vn, start_index, _len = struct.unpack("<HBB", bytes[:4])
    return locals()

def HandshakeRequest(bytes):
    sn, vn = struct.unpack("<8sH", bytes[:10])
    version = str(bytes[10:])
    return locals()
request_class_dict = {
    0x90: SimpleRequest,
    0x10: SimpleRequest,
    0x11: SimpleRequest,
    0x12: SimpleRequest,
    0x01: HandshakeRequest,
    0x50: HeartbeatRequest,
    0x51: HangUpRequest,
    0x21: LocalRouteRequest,
    0x52: TaskRequest,
    0x53: RouteRequest,
    0x54: BlockRequest,
    0x5A: WriteBitRequest,
    0x5B: WriteValueRequest,
    0x5C: ReadValueRequest
}

def on_request(_class, bytes):
    '''request'''
    _session = struct.unpack("<H", bytes[:2])[0]
    handler = request_class_dict.get(_class, None)
    if handler:
        return handler.__name__, handler(bytes[2:])

def SystemLastwillReport(bytes):
    return locals()

def CarrierLastwillReport(bytes):
    sn, vn = struct.unpack("<8sH", bytes)
    return locals()

def ErrorTokenReport(bytes):
    vn, token, session = struct.unpack("<HHH", bytes)
    return locals()

def CarrierStartupReport(bytes):
    vn, token, reserved = struct.unpack("<HHB", bytes)
    return locals()

def CarrierShutdownReport(bytes):
    vn, token, reason = struct.unpack("<HHB", bytes)
    return locals()

def SystemStatusReport(bytes):
    status = struct.unpack("<B", bytes)[0]
    return locals()

navi_status_trans = ('0-Unknown', '1-Lost', '2-Normal')
ctrl_mode_trans = ('0-Manual', '1-Half-Auto', '2-Full-Auto')
auto_mode_trans = ('0-Unknown', '1-Offline', '2-Half-Offline', '3-Online')
def NormalStatusReport(bytes):
    vn, token, location_x, location_y, attitude, navi_status, ctrl_mode, auto_mode, battery, error, logic_bits = struct.unpack("<HHdddBBBHLL", bytes[:-20])
    logic_values = struct.unpack("<10H", bytes[-20:])
    navi_status = navi_status_trans[navi_status]
    ctrl_mode = ctrl_mode_trans[ctrl_mode]
    auto_mode = auto_mode_trans[auto_mode]
    return locals()

route_status_trans = ("0-Unknown", "1-Way Point", "2-Way Line")
task_status_trans = ("0-Unknown", "1-Mailing", "2-Operating", "3-Done")
def TaskStatusReport(bytes):
    vn, token, route_status, route_value1, route_value2, task_id, task_status, task_value, route_len = struct.unpack(
        "<HHBHHBBHB", bytes[:14])
    route_numbers = struct.unpack("<%dH" % route_len, bytes[14:])

    route_status = route_status_trans[route_status]
    task_status = task_status_trans[task_status]
    return locals()

report_class_dict = {
    0xF1: SystemLastwillReport,
    0xF2: CarrierLastwillReport,
    0xFA: ErrorTokenReport,
    0xB1: CarrierStartupReport,
    0xB2: CarrierShutdownReport,
    0xC0: SystemStatusReport,
    0xC1: NormalStatusReport,
    0xC2: TaskStatusReport
}

def on_report(_class, bytes):
    '''report'''
    handler = report_class_dict.get(_class, None)
    if handler:
        return handler.__name__, handler(bytes)

def DatetimeResponse(bytes):
    sn, vn, datetime = struct.unpack("<8sHd", bytes)
    return locals()

def visualize_guid(guid):
    s = base64.b16encode(guid).decode()
    return "%s-%s-%s-%s-%s" % (s[:8], s[8:12], s[12:16], s[16:20], s[20:])


def FileInfoResponse(bytes):
    sn, vn, route_guid, route_revision, carrier_guid, carrier_revision = struct.unpack("<8sH16sL16sL", bytes)
    route_guid = visualize_guid(route_guid)
    carrier_guid = visualize_guid(carrier_guid)
    return locals()

def RouteFileResponse(bytes):
    sn, vn, _len = struct.unpack("<8sHH", bytes[:12])
    value = struct.unpack("<%ds" % _len, bytes[12:])[0]
    return locals()
CarrierFileResponse = RouteFileResponse

handshake_result_trans = ('0-Success', '1-Already registered', '2-Already Binded', '3-Illegal serial No.', '4-Unused Vehicle')
def HandshakeResponse(bytes):
    result, sn, vn, token = struct.unpack("<B8sHH", bytes[:13])
    version = bytes[13:]
    result = handshake_result_trans[result]
    return locals()

def HeartbeatResponse(bytes):
    vn, token = struct.unpack("<HH", bytes)
    return locals()

def HangUpResponse(bytes):
    vn, token, signal = struct.unpack("<HHB", bytes)
    signal = signal_trans[signal]
    return locals()

def TaskResponse(bytes):
    vn, token, task_id, point, code, value1, value2, value3, value4 = struct.unpack("<HHBHHHHHH", bytes)
    return locals()

def RouteResponse(bytes):
    vn, token, route_len = struct.unpack("<HHB", bytes[:5])
    route_numbers = struct.unpack("<%dH" % route_len, bytes[5:])
    return locals()

def BlockResponse(bytes):
    vn, token, block_type, block_value = struct.unpack("<HHBH", bytes)
    block_type = block_type_trans[block_type]
    return locals()

route_resp_result_trans = ('0-Success', '1-Pattern Error', '2-Way Point No. error')
def LocalRouteResponse(bytes):
    vn, route_len, result = struct.unpack("<HBB", bytes)
    result = route_resp_result_trans[result]
    return locals()

def WriteBitResponse(bytes):
    vn, token, value = struct.unpack("<HHL", bytes)
    return locals()

def WriteValueResponse(bytes):
    vn, token, start_index, value_count = struct.unpack("<HHBB", bytes[:6])
    values = struct.unpack("<%dH" % value_count, bytes[6:])[0]
    return locals()

ReadValueResponse = WriteValueResponse

def SoftwareVersionResponse(bytes):
    sn, vn, app_count, sw_type, version_code = struct.unpack("<8sHHH16s", bytes)
    return locals()

def SoftwareUpdateDownloadResponse(bytes):
    sn, vn, sw_type, version_code, file_type, ftp_len = struct.unpack("<8sHH16sHH", bytes[:32])
    ftp_address = bytes[32:]
    return locals()

response_class_dict = {
    0x90: DatetimeResponse,
    0x10: FileInfoResponse,
    0x11: RouteFileResponse,
    0x12: CarrierFileResponse,
    0x21: LocalRouteResponse,
    0x01: HandshakeResponse,
    0x50: HeartbeatResponse,
    0x51: HangUpResponse,
    0x52: TaskResponse,
    0x53: RouteResponse,
    0x54: BlockResponse,
    0x5A: WriteBitResponse,
    0x5B: WriteValueResponse,
    0x5C: ReadValueResponse,
    0x5D: SoftwareVersionResponse,
    0x5E: SoftwareUpdateDownloadResponse
}

def on_response(_class, bytes):
    '''response'''
    _session = struct.unpack("<H", bytes[:2])[0]
    handler = response_class_dict.get(_class, None)
    if handler:
        return handler.__name__, handler(bytes[2:])

type_dict = {
    0x01: on_request,
    0x02: on_response,
    0x03: on_report
}

def parse_header(bytes):
    # parse header
    _type, _class = struct.unpack("<BB", bytes[:2])
    return type_dict[_type].__doc__, _class, bytes[2:]

def parse_content(_type, _class, content):
    for key in type_dict:
        func = type_dict.get(key, None)
        if func.__doc__ == _type:
            return func(_class, content)
    else:
        #debug response
        return on_debug_response(_class, content)

module_state_trans = ('0-Unknown', '1-At Point', '2-At Line', '3-Exception')
can_state_trans = ('0-illegal !!!', '1-ConnectionLost', '2-Connected', '3-BootUp', '4-CanopenStop', '5-Operational', '6-PreOperational')

MotionModuleEx = ('Controller', 'Driver', 'SLAM', 'Location', 'Idle_NotAtPoint')

def MotionInfoResponse(bytes):
    State, HistoryState, _Exception, Index, SWVersion, CtrlMdlCanState, DrvMdlCanState = struct.unpack("<BBHH16sLL", bytes)
    State = module_state_trans[State]
    CtrlMdlCanState = can_state_trans[CtrlMdlCanState]
    DrvMdlCanState = can_state_trans[DrvMdlCanState]
    mask = 1
    exlst = []
    for i,desc in enumerate(MotionModuleEx):
        if _Exception & (mask << i):
            exlst.append(desc)
    _Exception = ' & '.join(exlst) if exlst else "No Exception"
    del mask, exlst, i, desc

    del SWVersion
    return locals()

debug_response_class_dict = [
    MotionInfoResponse, # 0
]
def on_debug_response(_class, content):
    if _class < len(debug_response_class_dict):
        handler= debug_response_class_dict[_class]
        return handler.__name__, handler(content)

if __name__ == "__main__":
    import base64
    content = "03DC0000F5760000E0FB0700E83409000CFC070003000500000005000000"
    bytes = base64.b16decode(content)
    ret = MotionInfoResponse(bytes)

    print( ret )
