# -*- coding: utf-8 -*-
import re


class Color:
    OKBLUE = '<font color="blue">'
    OKGREEN = '<font color="green">'
    FAIL = '<font color="red">'
    ENDC = '</font>'

    @staticmethod
    def normal(info):
        return Color.OKBLUE + info + Color.ENDC

    @staticmethod
    def high(info):
        return Color.OKGREEN + info + Color.ENDC

    @staticmethod
    def fail(info):
        return Color.FAIL + info + Color.ENDC

class Report:
    def __init__(self, _title, lang):
        self.title = _title
        self.contents = []
        self.max_name_len = 0
        self.lang = lang

    def append(self, value):
        index = len(self.contents)
        name = self.lang[index][0]
        desc = self.lang[index][1].get(value, None)
        if desc == None:
            if len(self.lang[index][1]):
                desc = Color.fail(value+' -- 异常状态')
            else:
                desc = value
        self.contents.append((name, desc))
        self.max_name_len = max(self.max_name_len, len(bytes(name, 'gb2312')))

    def dump(self):
        ret = '\n' + self.title + '\n'
        ret += ('='*len( bytes(self.title, 'gb2312') ) + '\n')
        for name, value in self.contents:
            ret += "  %s%s = %s\n" % (' '*(self.max_name_len - len(bytes(name, 'gb2312'))), name, value)
        return ret
class General:
    script_lang = [
        ("与脚本的通信状态", {
            'ex': Color.fail('通信异常'),
            'ok': Color.normal('通信正常'),
            'un':  Color.fail('状态未知')
        }),
        ("当前相对停车点的编号", {
            '0': Color.high('在目标点上'),
            '1': Color.high('在目标点的前一个点'),
            '-1': Color.high('在目标点的后一个点'),
            '-9999': '其他位置(脚本不关心的值)'
         }),
        ("脚本设置的相对停车位置", {
            '0': '在目标点停车',
            '1': '在目标点前一个点停车'
         }),
         ("脚本应答的任务ID号", {}),
         ("距离目标点的长度(毫米)", {}),
    ]

    canopen_state = {'5' : Color.normal('通信正常')}
    canopen_lang = [
        ("行走控制器", canopen_state),
        ("行走驱动器", canopen_state),
        ("举升控制器", canopen_state),
        ("举升驱动器", canopen_state),
        ("拉线编码器", canopen_state),
    ]

    lift_lang = [
        ("车载网关内部举升状态机", {'ex': Color.fail('举升过程出现异常'),
            'idle': Color.normal('举升功能处于空闲状态'),
            'task': Color.high('当前有举升任务'),
            'unkno': Color.fail('初始化时的未知状态')
         }),
        ("举升异常码", {
            '0': Color.normal('正常'),
            '1': Color.fail('举升控制器故障'),
            '2': Color.fail('举升驱动器故障'),
            '4': Color.fail('拉线编码器故障'),
            '8': Color.fail('任务超时'),
            '22': Color.fail('未知'),
        }),
        ("举升工作状态", {
            '1': Color.high('开始升降叉臂'),
            '2': '叉臂升降完成'
        }),
        ("举升的目标高度(毫米)", {}),
        ("叉臂的当前高度(毫米)", {}),
        ("叉臂的控制模式", {
            '0': '叉臂不控',
            '1': '精准举升',
            '2': '精准下降',
            '3': '模糊举升',
            '4': '模糊下降',
            '5': '不带货举升',
            '6': '不带货下降',
            '7': '短距离举升'
        }),
        ("叉臂错误状态", {
            '1': Color.normal('正常'),
            '2':  Color.fail('估重失败'),
            '3':  Color.fail('举升驱动器故障'),
            '4':  Color.fail('拉线编码器故障')
        }),
        ("叉臂举升时的电机工作电压(伏)", {}),
    ]

    basic_lang = [
        ("车载网关状态机", {
            'init': Color.fail('上电初始化中'),
            'work': Color.normal('正常工作中')
         }),
        ("地图状态", {
            'new': Color.normal('已同步最新地图'),
            'wft':  Color.fail('正在获取Ftp地址'),
            'dow':  Color.fail('正在下载地图'),
            'old':  Color.fail('地图不是最新的'),
        }),
        ("抱闸状态", {
            'b':  Color.fail('抱闸'),
            'o': Color.normal('松开'),
            'u':  Color.fail('未知'),
        }),
        ("手自动信号", {
            'm': Color.fail('手动'),
            'a': Color.normal('自动'),
            'c': Color.high('充电'),
            'u': Color.fail('未知'),
         })
    ]

    slam_lang = [
        ("车载网关与slam的通信状态", {
            'ok': Color.normal('通信正常'),
            'ex': Color.fail('通信失败'),
            'un': Color.fail('未知状态'),
        })
    ]

    task_lang = [
        ("任务ID", {}),
        ("目标点", {}),
        ("操作码", {}),
        ("任务参数1", {}),
        ("任务参数2", {}),
        ("任务参数3", {}),
        ("任务参数4", {}),
        ("目标点", {}),
        ("目标点前一个点", {}),
        ("任务执行状态", {
            'r': Color.high('运行中'),
            'f': Color.normal('任务完成'),
            'o': Color.high('任务操作中(或将要操作)'),
            'n': '当前无任务',
        }),
    ]

    motion_lang = [
        ("行走状态", {
            'ex': Color.fail('出现异常'),
            'li': Color.high('在线上'),
            'pt': Color.normal('在点上'),
            'un': Color.fail('未知'),
        }),
        ("异常码", {
            '0': Color.normal('正常'),
            '1': Color.fail('行走控制器故障'),
            '2': Color.fail('行走驱动器故障'),
            '4': Color.fail('SLAM故障'),
            '8': Color.fail('未定义故障8'),
            '16': Color.fail('未定义故障16'),
        }),
        ("运行状态", {
            '1': Color.high('开始走线'),
            '2': Color.fail('脱轨'),
            '3': Color.normal('正常停车')
        }),
        ("任务参数1(线号)", {}),
        ("任务参数2(百分比)", {}),
        ("逻辑位的最高位", {
            "0" : "不可降叉臂",
            "1" : "可降叉臂"
        }),
    ]

    route_lang = [
        ("调度规划的线路", {}),
        ("当前待行驶线路", {}),
        ("A9卡住不发送给驱A的线路", {}),
    ]

    tc_lang = [
        ("阻塞类型", {
            '0': '无阻塞',
            '1': Color.fail('小车阻塞'),
            '2': Color.fail('区块阻塞'),
            '3': Color.fail('变量阻塞'),
        }),
        ("阻塞值", {}),
    ]

    @classmethod
    def on_script(cls, data):
        state = data[0].strip()
        LocalPointIndex = data[1].strip()
        LocalStopIndex = data[2].strip()
        m_ScriptTaskID = data[3].strip()
        TargetPointLength = data[4].strip()
        r = Report('模块1--script', cls.script_lang)
        r.append(state)
        r.append(LocalPointIndex)
        r.append(LocalStopIndex)
        r.append(m_ScriptTaskID)
        r.append(TargetPointLength)
        return r

    @classmethod
    def on_canopen(cls, data):
        DriverA = data[0][0]
        MotionDriver = data[0][1]
        DriverB = data[0][2]
        LiftDriver = data[0][3]
        WireDrawEncoder = data[0][4]

        r = Report('模块2--can', cls.canopen_lang)
        r.append(DriverA)
        r.append(MotionDriver)
        r.append(DriverB)
        r.append(LiftDriver)
        r.append(WireDrawEncoder)
        return r

    @classmethod
    def on_lift(cls, data):
        state = data[0].strip()
        Exception = data[1].strip()
        WorkState = data[2].strip()
        TargetHeight = data[3].strip()
        CurrentHeight = data[4].strip()
        ControlMode = data[5].strip()
        LiftCtrlError = data[6].strip()
        LiftMotorVoltage = data[7].strip()

        r = Report('模块3--举升任务相关数据(lift)', cls.lift_lang)
        r.append(state)
        r.append(Exception)
        r.append(WorkState)
        r.append(TargetHeight)
        r.append(CurrentHeight)
        r.append(ControlMode)
        r.append(LiftCtrlError)
        r.append(LiftMotorVoltage)
        return r

    @classmethod
    def on_basic(cls, data):
        state = data[0].strip()
        MapState = data[1].strip()
        EmergencyState = data[2].strip()
        knob = data[3].strip()

        r = Report('模块4--小车基本信息(basic)', cls.basic_lang)
        r.append(state)
        r.append(MapState)
        r.append(EmergencyState)
        r.append(knob)

        return r

    @classmethod
    def on_slam(cls, data):
        state = data[0].strip()

        r = Report('模块5--激光定位(slam)', cls.slam_lang)
        r.append(state)
        return r

    @classmethod
    def on_task(cls, data):
        TaskID = data[0].strip()
        TargetPointNumber = data[1].strip()
        OperationCode = data[2].strip()
        OperationValue1 = data[3].strip()
        OperationValue2 = data[4].strip()
        OperationValue3 = data[5].strip()
        OperationValue4 = data[6].strip()
        TargetPoint = data[7].strip()
        StopPoint = data[8].strip()
        AgvTaskStatus = data[9].strip()

        r = Report('模块6--任务模块(task)', cls.task_lang)
        r.append(TaskID)
        r.append(TargetPointNumber)
        r.append(OperationCode)
        r.append(OperationValue1)
        r.append(OperationValue2)
        r.append(OperationValue3)
        r.append(OperationValue4)
        r.append(TargetPoint)
        r.append(StopPoint)
        r.append(AgvTaskStatus)
        return r

    @classmethod
    def on_motion(cls, data):
        State = data[0].strip()
        Exception = data[1].strip()
        RunningState = data[2].strip()
        RouteValue1 = data[3].strip()
        RouteValue2 = data[4].strip()
        Bit31 = data[5].strip()

        r = Report('模块7--行走(motion)', cls.motion_lang)
        r.append(State)
        r.append(Exception)
        r.append(RunningState)
        r.append(RouteValue1)
        r.append(RouteValue2)
        r.append(Bit31)
        return r

    @classmethod
    def on_route(cls, data):
        m_routes = RouteNumbers = Blocklines = "None"
        pattern_m = 'm\\(([\d,]+)\\)'
        m = re.search(pattern_m, data)
        if m:
            m_routes = m.groups()[0]

        pattern_c = 'c\\(([\d,]+)\\)'
        m = re.search(pattern_c, data)
        if m:
            RouteNumbers = m.groups()[0]

        pattern_b = 'b\\(([\d,]+)\\)'
        m = re.search(pattern_b, data)
        if m:
            Blocklines = m.groups()[0]

        r = Report('模块8--路径状态(route)', cls.route_lang)
        r.append(m_routes)
        r.append(RouteNumbers)
        r.append(Blocklines)
        return r

    @classmethod
    def on_tc(cls, data):
        m_blocktype = data[0].strip()
        m_blockvalue= data[1].strip()

        r = Report('模块9--交通管制(tc)', cls.tc_lang)
        r.append(m_blocktype)
        r.append(m_blockvalue)
        return r

def parse_log_general(line):
    #line = '[I][2019-09-17 18:28:14.969][CH02]: script:ok,-9999, 0,183,  3759; can:55555; lift:idle, 0,2, 600, 603,   2,1,  0; basic:work,new,o,a; slam:ok; task:   183, 258#,  11, 600, 400,   0,   0, 258, 257,r; motion:li, 0,1, 188,98,0; route:m(201,188,413,411,),c(188,413,411,),b(),tc:0,0'
    #prefix_len = 36
    #line = line[prefix_len:]

    ret = ''
    #script
    pattern_script = "script:([\w ,-]+);"
    m = re.search(pattern_script, line)
    if m:
        script = m.groups()[0].split(',')
        ret += General.on_script( script ).dump()
    else:
        ret += "!!!!!!!!script missing"

    #can
    pattern_can = "can:([\w ,-]+);"
    m = re.search(pattern_can, line)
    if m:
        can = m.groups()[0].split(',')
        ret += General.on_canopen( can ).dump()
    else:
        ret += "!!!!!!!!can missing"
    # lift
    pattern_lift = "lift:([\w ,-]+);"
    m = re.search(pattern_lift, line)
    if m:
        lift = m.groups()[0].split(',')
        ret += General.on_lift( lift ).dump()
    else:
        ret += "!!!!!!!!lift missing"
    # basic
    pattern_basic = "basic:([\w ,-]+);"
    m = re.search(pattern_basic, line)
    if m:
        basic = m.groups()[0].split(',')
        ret += General.on_basic( basic ).dump()
    else:
        ret += "!!!!!!!!basic missing"
    # slam
    pattern_slam = "slam:([\w ,-]+);"
    m = re.search(pattern_slam, line)
    if m:
        slam = m.groups()[0].split(',')
        ret += General.on_slam( slam ).dump()
    else:
        ret += "!!!!!!!!slam missing"
    # task
    pattern_task = "task:([\w ,#-]+);"
    m = re.search(pattern_task, line)
    if m:
        task = m.groups()[0].split(',')
        ret += General.on_task( task ).dump()
    else:
        ret += "!!!!!!!!task missing"
    # motion
    pattern_motion = "motion:([\w ,-]+);"
    m = re.search(pattern_motion, line)
    if m:
        motion = m.groups()[0].split(',')
        ret += General.on_motion( motion ).dump()
    else:
        ret += "!!!!!!!!motion missing"
    # route
    pattern_route = "route:([\w() ,-]+)tc"
    m = re.search(pattern_route, line)
    if m:
        route = m.groups()[0]
        ret += General.on_route( route ).dump()
    else:
        ret += "!!!!!!!!route missing"
    # tc
    pattern_tc = "tc:([\d,-]+)"
    m = re.search(pattern_tc, line)
    if m:
        tc = m.groups()[0].split(',')
        ret += General.on_tc( tc ).dump()
    else:
        ret += "!!!!!!!!tc missing"

    return ret

class Motion:
    tag_lang = ("当前状态", {
        "100000" : Color.fail("停车"),
        "400000" : Color.fail("抱闸"),
        "500000" : Color.fail("手动模式")
         })

    debug_lang = [
        ("激光数据错误标志位", {
            "0": Color.normal("正常"),
            "1": Color.fail("错误")
        }),
        ("激光断线错误标志位", {
            "0": Color.normal("正常"),
            "1": Color.fail("错误")
        }),
        ("curtis电机驱动器数据错误标志位", {
            "0": Color.normal("正常"),
            "1": Color.fail("错误")
        }),
        ("总的错误码", {
            "0": Color.normal("正常"),
        }),
        ("拟合点状态", {
            "0": Color.high("没有点"),
            "1": Color.high("找到最近点，但没有下一个点"),
            "2": Color.normal("能找到最近的点和下一个点"),
            "3": Color.fail("异常点")
        }),
        ("应为0", {"0":"0"}),
        ("左避障", {}),
        ("右避障", {}),
        ("总避障", {
            '1' : '停车',
            '2' : '减速',
            '3' : '正常',
            '4' : '抱闸',
        }),
        ("应为0", {"0":"0"}),
    ]

    debug_lang2 = [
        ('X向偏差(0.01mm)', {}),
        ('Y向偏差(0.01mm)', {}),
        ('航向偏差(0.01度)', {}),
        ('给定速度(0.01mm/s)', {}),
        ('反馈速度(0.01mm/s)', {}),
        ('给定打角(0.01度)', {}),
        ('实际打角(0.01度)', {}),
        ('X向参考坐标(0.01mm)', {}),
        ('Y向参考坐标(0.01mm)', {}),
        ('参考航向角(0.01度)', {}),
        ('保留字段0', {}),
        ('保留字段1', {}),
        ('保留字段2', {}),
        ('保留字段3', {}),
        ('保留字段4', {}),
        ('保留字段5', {}),
        ('保留字段6', {}),
        ('保留字段7', {}),
        ('保留字段8', {}),
        ('保留字段9', {}),
    ]

    attitude_lang = [
        ("X向融合坐标(0.01mm)", {}),
        ("Y向融合坐标(0.01mm)", {}),
        ("融合航向角（0.01度）", {}),
        ("X向SLAM坐标(0.01mm)", {}),
        ("Y向SLAM坐标(0.01mm)", {}),
        ("SLAM航向角(0.01度)", {}),
        ("错误码", {}),
        ("线号1", {}),
        ("线号2", {}),
        ("线号3", {}),
        ("线数", {}),
    ]

    a9_lang = [
        ('电机速度(rpm)', {}),
        ('电机角度(0.01度)', {}),
        ('小车所在路径状态', {}),
        ('小车运行状态', {
            '1':Color.normal("走线"),
            '2':Color.fail("脱轨"),
            '3':Color.high("停车")
        }),
        ('避障状态', {
            'a:1':Color.high("停车"),
            'a:2':Color.high("减速"),
            'a:3':Color.normal("正常"),
            'a:4':Color.fail("抱闸")
        }),
        ("急停状态", {
            'e:1':Color.fail("抱闸"),
            'e:0':"松闸"
        }),
        ("脚本设置的减速比", {}),
        ("手自动信号", {
            'manual': Color.fail('手动'),
            'auto': Color.normal('自动'),
            'unknown': Color.fail('未知'),
        })
    ]

    @classmethod
    def on_debug(cls, data):
        if data[0] in cls.tag_lang[1]:
            lang = [cls.tag_lang] + cls.debug_lang
            r = Report('模块1--驱A上报数据(debug)', lang)
            r.append(data[0])
            r.append(data[1])
            r.append(data[2])
            r.append(data[3])
            r.append(data[4])
            r.append(data[5])
            r.append(data[6])

            #data[7] -> * 3
            full_data7 = "%03d" % int(data[7])
            r.append(full_data7[0])
            r.append(full_data7[1])
            r.append(full_data7[2])

            r.append(data[8])
            return r
        else:
            r = Report('模块1--驱A上报数据(debug)', cls.debug_lang2)
            for i in range(20):
                r.append(data[i])
            return r
    @classmethod
    def on_attitute(cls, data):
        r = Report('模块2--小车姿态(attitude)', cls.attitude_lang)
        for i in data:
            r.append(i)
        return r


    @classmethod
    def on_a9(cls, data):
        r = Report('模块3--A9数据(a9)', cls.a9_lang)

        Speed = data[0].strip()
        Angle = data[1].strip()
        RouteStatus = data[2].strip()
        RunningState = data[3].strip()
        AvoidanceInfo = data[4].strip()
        EmergencyStop = data[5].strip()
        DeceRatioSetByScript = data[6].strip()
        OperateMode = data[7].strip()

        r.append(Speed)
        r.append(Angle)
        r.append(RouteStatus)
        r.append(RunningState)
        r.append(AvoidanceInfo)
        r.append(EmergencyStop)
        r.append(DeceRatioSetByScript)
        r.append(OperateMode)

        return r

def parse_log_motion(line):
    line = line.split(',')[1:-1]
    # 20 个 驱A上报的调试数据
    debug = line[:20]
    attitute = line[20:31]
    line = line[31:]
    ret = Motion.on_debug(debug).dump()
    ret += Motion.on_attitute(attitute).dump()
    ret += Motion.on_a9(line).dump()

    return ret


if __name__ == "__main__":
    print( parse_log_motion(' ,110472,-1174,-51,30400,103143,-44,-25,56698,6020,27000,4,18,18,300,100,15,0,-44,0,45235,56686,6039,270510,56688,5694,270515,0,12,5,0,2,1393,-36,online:12-14%,1,a:3,e:0,-1,auto ,') )