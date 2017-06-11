#encoding:utf-8
import linux

t = linux.cpu()

def deal_warning_cpu(msg):
    avg = t.triggers["idle"]["func"]
    min = t.triggers["idle"]["minutes"]
    operator = t.triggers["idle"]["operator"]
    hit =  t.triggers["idle"]["hit"]
    warning = t.triggers["idle"]["warning"]
    critical = t.triggers["idle"]["critical"]
    datetype = t.triggers["idle"]["data_type"]
    #获取最近5分钟的cpu的idle的平均值
    avg_value = avg(min,operator,warning,critical)

def deal_warning_memory(msg):
    pass



