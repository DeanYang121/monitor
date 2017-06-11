#encoding: utf-8
import gevent
from gevent import monkey;monkey.patch_all()
import time
from redisHelper import redisHelper
from server import serialize
from data2db import data2db
import alert_process


def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]

    return lst

class MonitorServer(object):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.redis = redisHelper()

    def send_monitor_items(self):
        serialize.flush_all_host_config_into_redis()


    def recive_msg(self):
        _cnt,_rt = 0,0
        msg = self.redis.subscribe()
        # print(msg)
        if msg["item"] == "cpu":
            del msg["item"]
            # {'steal': '0.0', 'nice': '0.9', 'user': '14.2', 'ip': b'192.168.196.136\n', 'idle': '71.9', 'iowait': '6.6', 'system': '6.0'}
            sorted_x = sorted(dict2list(msg), key=lambda x:x[0])
            #[('idle', '86.5'), ('iowait', '1.6'), ('ip', b'192.168.196.136\n'), \
            # ('nice', '0.2'), ('steal', '0.0'), ('system', '3.2'), ('user', '8.3')]
            _rt_items = []
            _rt_lists = []
            for i in range(len(sorted_x)):
                # print(sorted_x[i][1])
                _rt_items.append(sorted_x[i][0]) #['idle', 'iowait', 'ip', 'nice', 'steal', 'system', 'user']
                _rt_lists.append(sorted_x[i][1]) #['85.3', '2.6', '192.168.196.136', '0.3', '0.0', '2.8', '8.7']

            idle,iowait,ip,nice,steal,system,user = _rt_items[0],_rt_items[1],_rt_items[2],_rt_items[3],_rt_items[4],_rt_items[5],_rt_items[6]
            idle_v,iowait_v,ip_v,nice_v,steal_v,system_v,user_v = _rt_lists[0],_rt_lists[1],_rt_lists[2],_rt_lists[3],_rt_lists[4],_rt_lists[5],_rt_lists[6]
            _sql = "insert into cpu_info({0},{1},{2},{3},{4},{5},{6},time) value(%s,%s,%s,%s,%s,%s,%s,%s)".format(idle,iowait,ip,nice,steal,system,user)
            # _sql = "insert into cpu_info{0} value(%s,%s,%s,%s,%s,%s,%s)".format(_rt_items)
            _time = time.strftime('%Y-%m-%d %H:%M:%S')
            _args = (idle_v,iowait_v,ip_v,nice_v,steal_v,system_v,user_v,_time)
            _cnt,_rt = data2db(_sql,_args,fetch=False)
            if _cnt != 0:
                print("cpu信息成功存入数据库，存入数据{_cnt}条".format(_cnt=_cnt[0]))
            else:
                print("error 数据存入失败")
            alert_process.alert_cpu_jadge()
        elif msg["item"] == "memory":
            # print("来自于memory的信息！%s"%msg)
            del msg["item"]
            sorted_mem = sorted(dict2list(msg),key=lambda x:x[0])
            # print(sorted_mem) [('buffer', 88856.0), ('ip',121212),('mem_available', 1818784.0), ('mem_free', 719908.0), ('mem_total', 4026820.0)]
            _mem_items = []
            _mem_lists = []
            for i in range(len(sorted_mem)):
                _mem_items.append(sorted_mem[i][0])
                _mem_lists.append(sorted_mem[i][1])

            buffer,ip,mem_available,mem_free,mem_total=_mem_items[0],_mem_items[1],_mem_items[2],_mem_items[3],_mem_items[4]
            buffer_v,ip_v,mem_available_v,mem_free_v,mem_total_v = _mem_lists[0],_mem_lists[1],_mem_lists[2],_mem_lists[3],_mem_lists[4]
            _mem_sql = "insert into mem_info({0},{1},{2},{3},{4},time) value(%s,%s,%s,%s,%s,%s)".format(buffer,ip,mem_available,mem_free,mem_total)
            _time = time.strftime("%Y-%m-%d %H-%M-%S")
            _mem_args = (buffer_v,ip_v,mem_available_v,mem_free_v,mem_total_v,_time)
            _mem_cnt,_mem_rt = data2db(_mem_sql,_mem_args,fetch=False)
            if _mem_cnt != 0:
                print("memory 信息存入数据库成功，存入数据{_cnt}条".format(_cnt=_mem_cnt[0]))
            else:
                print("memory信息存入失败！！")
            alert_process.alert_memory_jadge(mem_available_v)

    def handle(self):
        while True:
            gevent.joinall([
                gevent.spawn(MonitorServer.recive_msg(self)),
            ])


    def run(self):
        print('---starting monitor server----')
        self.handle()

    def process(self):
        pass
if __name__=="__main__":
    s = MonitorServer('0.0.0.0','8000')
    s.run()

