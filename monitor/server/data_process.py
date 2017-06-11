#encoding: utf-8
from dbutil import dbutils
from functools import reduce
from warning_method.alert_email import send_126_mail
import threading

def str2int(s):
    def fn(x,y):
        return x*10 + y

    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    return reduce(fn,map(char2num,s))

"""
from functools import reduce

def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))
"""

def avg(*args,**kwargs):
    _sql = kwargs["sql"]
    _args = kwargs["args"]
    t = dbutils.Mysql_connection()
    _cnt,_rt = t.execute_sql(_sql,_args)
    _avg_value = _rt[0][0]

    if _avg_value <= kwargs["critical"]:
         # print(_avg_value)
         #告警
         # print("idle报警，发送邮件报警信息！级别：严重")
         subject = "CPU idle报警！"
         mail_msg = "idle报警，成功发送邮件报警信息！级别：严重,idle值：{0}".format(_avg_value)
         t = threading.Thread(target=send_126_mail, args=[subject, mail_msg])
         t.start()
    elif _avg_value <= kwargs["warning"]:
         #警告
         # print("idle报警，发送邮件报警信息！级别：警告")
         subject = "CPU idle报警！"
         mail_msg = "idle报警，成功发送邮件报警信息！级别：警告,idle值：{0}".format(_avg_value)
         t = threading.Thread(target=send_126_mail,args=[subject,mail_msg])
         t.start()
         #可以将报警的记录存入数据库

def hit(*args,**kwargs):
    #判断每一次传递过来的值是否超过cirtical值的次数是否大于3,如果大于3，并且判断最后一次是否大于3,如果是也报警
    _sql = kwargs["sql"]
    _args = kwargs["args"]
    _mem_available = kwargs["mem_available"]
    _hit_v = kwargs["hit"]
    _critical = kwargs["critical"]
    _warning = kwargs["warning"]
    t = dbutils.Mysql_connection()
    _cnt,_rt = t.execute_sql(_sql,_args)
    hit_c = 0
    hit_w = 0
    # print(_cnt,_rt[0][0],_rt[1][0])
    for i in range(_cnt):
        if str2int(_rt[i][0]) <= _critical:
           hit_c += 1
        elif str2int(_rt[i][0]) <= _warning:
           hit_w += 1
    if hit_c >= _hit_v:
        # print("内存报警！报警级别：严重")
        subject = "memory 可用内存不足报警！"
        mail_msg = "memory可用内存报警，成功发送邮件报警信息！级别：严重,hit值：{0}".format(hit_c)
        t = threading.Thread(target=send_126_mail,args=[subject,mail_msg])
        t.start()
    elif hit_w >= _hit_v+2:
        # print("内存报警！报警级别：警告")
        subject = "memory 可用内存不足报警！"
        mail_msg = "memory可用内存报警，成功发送邮件报警信息！级别：警告,hit值：{0}".format(hit_w)
        t = threading.Thread(target=send_126_mail,args=[subject,mail_msg])
        t.start()







def last(mins,operator):
    #获取最后一次的值
    pass

if __name__=="__main__":
    avg()

