# -*- coding: UTF-8 -*-
import struct

def HeartbeatRequest(bytes):
    vn = struct.unpack("<H", bytes)[0]
    return locals()

signal_trans = ('0-恢复', '1-挂起')
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

block_type_trans = ("0-无阻塞", "1-小车阻塞", "2-区块阻塞", "3-变量阻塞")
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
request_class_dict = {
    0x90: SimpleRequest,
    0x10: SimpleRequest,
    0x11: SimpleRequest,
    0x12: SimpleRequest,
    0x01: SimpleRequest,
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
    '''=>'''
    _session = struct.unpack("<H", bytes[2:4])[0]
    handler = request_class_dict.get(_class, None)
    if handler:
        return handler(bytes[4:])

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

def NormalStatusReport(bytes):
    vn, token, location_x, location_y, attitude, navi_status, ctrl_mode, auto_mode, battery, error, logic_bits, logic_values = struct.unpack("<HHdddBBBHLL10H", bytes)
    return locals()

report_class_dict = {
    0xF1: SystemLastwillReport,
    0xF2: CarrierLastwillReport,
    0xFA: ErrorTokenReport,
    0xB1: CarrierStartupReport,
    0xB2: CarrierShutdownReport,
    0xC0: SystemStatusReport,
    0xC1: NormalStatusReport
}

def on_report(_class, bytes):
    handler = report_class_dict.get(_class, None)
    if handler:
        return handler(bytes[2:])

def DatetimeResponse(bytes):
    sn, vn, datetime = struct.unpack("<8sHd", bytes)
    return locals()

def FileInfoResponse(bytes):
    sn, vn, route_guid, route_revision, carrier_guid, carrier_revision = struct.unpack("<8sH16sL16sL", bytes)
    return locals()

def RouteFileResponse(bytes):
    sn, vn, _len = struct.unpack("<8sHH", bytes[:12])
    value = struct.unpack("<%ds" % _len, bytes[12:])[0]
    return locals()
CarrierFileResponse = RouteFileResponse

handshake_result_trans = ('0-成功', '1-该小车系统编号已注册', '2-该小车系统编号已绑定', '3-非法的序列号', '4-该小车未启用')
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

route_resp_result_trans = ('0-成功', '1-模式错误', '2-错误的路径编号')
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
    '''<='''
    _session = struct.unpack("<H", bytes[2:4])[0]
    handler = response_class_dict.get(_class, None)
    if handler:
        return handler(bytes[4:])

type_dict = {
    0x01: on_request,
    0x02: on_response,
    0x03: on_report
}

def parse_payload(bytes):
    # parse header
    _type, _class = struct.unpack("<BB", bytes[:2])
    func = type_dict.get(_type, None)
    if func:
        func(_class, bytes)
